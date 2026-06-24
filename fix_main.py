import pathlib

main_content = """import 'package:flutter/material.dart';
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
  await initLocale(); // reads SharedPreferences -> sets initialLocale
  await Supabase.initialize(
    url:     dotenv.env['SUPABASE_URL']!,
    anonKey: dotenv.env['SUPABASE_ANON_KEY']!,
  );
  runApp(
    ProviderScope(
      // Seed the notifier with the saved locale BEFORE first build
      overrides: [
        localeProvider.overrideWith(() => LocaleNotifier.withInitial(initialLocale)),
      ],
      child: const FlowerScoutApp(),
    ),
  );
}

class FlowerScoutApp extends ConsumerWidget {
  const FlowerScoutApp({super.key});
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    ref.watch(localeProvider);
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Flower Scout',
      theme: AppTheme.lightTheme,
      home: const _AuthGate(),
    );
  }
}

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
    ref.watch(localeProvider);
    return _loggedIn ? const AppShell() : const LoginScreen();
  }
}
"""

pathlib.Path('lib/main.dart').write_text(main_content, encoding='utf-8')
print('main.dart done')