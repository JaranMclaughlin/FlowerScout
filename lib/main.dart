import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'core/theme/app_theme.dart';
import 'core/session/user_session.dart';
import 'features/auth/presentation/login_screen.dart';
import 'shared/widgets/app_shell.dart';
import 'shared/providers/farm_providers.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await dotenv.load(fileName: '.env');
  await Supabase.initialize(
    url:     dotenv.env['SUPABASE_URL']!,
    anonKey: dotenv.env['SUPABASE_ANON_KEY']!,
  );
  runApp(const ProviderScope(child: FlowerScoutApp()));
}

class FlowerScoutApp extends StatelessWidget {
  const FlowerScoutApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Flower Scout',
      theme: AppTheme.lightTheme,
      home: const _AuthGate(),
    );
  }
}

class _AuthGate extends StatefulWidget {
  const _AuthGate();
  @override
  State<_AuthGate> createState() => _AuthGateState();
}

class _AuthGateState extends State<_AuthGate> {
  @override
  void initState() {
    super.initState();
    Supabase.instance.client.auth.onAuthStateChange.listen((data) async {
      if (!mounted) return;
      final event = data.event;
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
            UserSession.currentUser = row['full_name'] as String? ?? '';
            UserSession.currentProfile = switch (role) {
              'system_admin' => UserProfile.systemAdmin,
              'manager'      => UserProfile.manager,
              _              => UserProfile.scout,
            };
          }
        } catch (_) {}
        if (!mounted) return;
        Navigator.of(context).pushAndRemoveUntil(
          MaterialPageRoute(builder: (_) => const AppShell()),
          (route) => false,
        );
      } else if (event == AuthChangeEvent.signedOut) {
        UserSession.currentProfile = UserProfile.scout;
        UserSession.currentUser = '';
        Navigator.of(context).pushAndRemoveUntil(
          MaterialPageRoute(builder: (_) => const LoginScreen()),
          (route) => false,
        );
      }
    });
  }
  @override
  Widget build(BuildContext context) {
    final session = Supabase.instance.client.auth.currentSession;
    if (session != null) return const AppShell();
    return const LoginScreen();
  }
}
