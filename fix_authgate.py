import pathlib

p = pathlib.Path('lib/shared/providers/locale_provider.dart')
p.write_text(r"""
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../l10n/app_strings.dart';

const _kLangKey = 'flowerscout_language';

SharedPreferences? _prefsInstance;

class LocaleNotifier extends Notifier<String> {
  @override
  String build() {
    final saved = _prefsInstance?.getString(_kLangKey) ?? 'en';
    return saved;
  }

  Future<void> setLanguage(String code) async {
    // Update state immediately so UI rebuilds now
    state = code;
    // Persist
    _prefsInstance ??= await SharedPreferences.getInstance();
    await _prefsInstance!.setString(_kLangKey, code);
  }
}

final localeProvider = NotifierProvider<LocaleNotifier, String>(
  LocaleNotifier.new,
);

final stringsProvider = Provider<AppStrings>((ref) {
  final code = ref.watch(localeProvider);
  return AppStrings.of(code);
});

Future<void> initLocale() async {
  _prefsInstance = await SharedPreferences.getInstance();
}
""".lstrip(), encoding='utf-8')
print('Cleaned locale_provider.dart')

# The REAL fix: _AuthGate must be a ConsumerWidget so it watches localeProvider
# and AppShell is built after locale is known. Also the navigation must preserve
# the provider state by not using pushAndRemoveUntil with a new MaterialPageRoute
# Instead we use the _AuthGate state itself to switch screens

main = pathlib.Path('lib/main.dart')
main.write_text(r"""
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'core/theme/app_theme.dart';
import 'core/session/user_session.dart';
import 'features/auth/presentation/login_screen.dart';
import 'shared/widgets/app_shell.dart';
import 'shared/providers/locale_provider.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await dotenv.load(fileName: '.env');
  await initLocale();
  await Supabase.initialize(
    url:     dotenv.env['SUPABASE_URL']!,
    anonKey: dotenv.env['SUPABASE_ANON_KEY']!,
  );
  runApp(const ProviderScope(child: FlowerScoutApp()));
}

class FlowerScoutApp extends ConsumerWidget {
  const FlowerScoutApp({super.key});
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    ref.watch(localeProvider); // force rebuild on language change
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Flower Scout',
      theme: AppTheme.lightTheme,
      home: const _AuthGate(),
    );
  }
}

// Use a ConsumerStatefulWidget so the auth gate also rebuilds on locale change
class _AuthGate extends ConsumerStatefulWidget {
  const _AuthGate();
  @override
  ConsumerState<_AuthGate> createState() => _AuthGateState();
}

class _AuthGateState extends ConsumerState<_AuthGate> {
  bool _loggedIn = false;

  @override
  void initState() {
    super.initState();
    // Set initial state from current session
    _loggedIn = Supabase.instance.client.auth.currentSession != null;

    Supabase.instance.client.auth.onAuthStateChange.listen((data) async {
      if (!mounted) return;
      final event   = data.event;
      final session = data.session;

      if (session != null &&
          (event == AuthChangeEvent.signedIn ||
           event == AuthChangeEvent.userUpdated ||
           event == AuthChangeEvent.passwordRecovery)) {
        try {
          final uid = Supabase.instance.client.auth.currentUser?.id;
          if (uid != null) {
            final row = await Supabase.instance.client
                .from('user_profiles')
                .select('role, full_name')
                .eq('id', uid)
                .single();
            final role = row['role'] as String? ?? 'scout';
            UserSession.currentUser    = row['full_name'] as String? ?? '';
            UserSession.currentProfile = switch (role) {
              'system_admin' => UserProfile.systemAdmin,
              'manager'      => UserProfile.manager,
              _              => UserProfile.scout,
            };
          }
        } catch (_) {}
        if (!mounted) return;
        setState(() => _loggedIn = true);
      } else if (event == AuthChangeEvent.signedOut) {
        UserSession.currentProfile = UserProfile.scout;
        UserSession.currentUser    = '';
        if (!mounted) return;
        setState(() => _loggedIn = false);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return _loggedIn ? const AppShell() : const LoginScreen();
  }
}
""".lstrip(), encoding='utf-8')
print('Rewrote main.dart - AuthGate now uses setState instead of Navigator')