import pathlib

p = pathlib.Path('lib/main.dart')

content = """import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'core/theme/app_theme.dart';
import 'core/session/user_session.dart';
import 'features/auth/presentation/login_screen.dart';
import 'shared/widgets/app_shell.dart';
import 'shared/providers/locale_provider.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const _Bootstrap());
}

// ── Bootstrap ─────────────────────────────────────────────────────────────
// Renders a splash immediately instead of leaving the user on a blank
// screen while dotenv / Supabase / locale init run. Has a timeout and a
// retry path so a slow or failed network doesn't hang the app forever.
class _Bootstrap extends StatefulWidget {
  const _Bootstrap();
  @override
  State<_Bootstrap> createState() => _BootstrapState();
}

class _BootstrapState extends State<_Bootstrap> {
  Future<void>? _initFuture;

  @override
  void initState() {
    super.initState();
    _initFuture = _init();
  }

  void _retry() {
    setState(() {
      _initFuture = _init();
    });
  }

  Future<void> _init() async {
    final sw = Stopwatch()..start();
    try {
      final dotenvFuture = dotenv.load(fileName: '.env');
      final localeFuture = initLocale();

      await dotenvFuture.timeout(const Duration(seconds: 10));
      debugPrint('[startup] dotenv loaded at \${sw.elapsedMilliseconds}ms');

      await Supabase.initialize(
        url:     dotenv.env['SUPABASE_URL']!,
        anonKey: dotenv.env['SUPABASE_ANON_KEY']!,
      ).timeout(const Duration(seconds: 15));
      debugPrint('[startup] Supabase initialized at \${sw.elapsedMilliseconds}ms');

      await localeFuture.timeout(const Duration(seconds: 10));
      debugPrint('[startup] locale ready at \${sw.elapsedMilliseconds}ms');
    } catch (e, st) {
      debugPrint('[startup] init failed after \${sw.elapsedMilliseconds}ms: \$e');
      if (kDebugMode) debugPrintStack(stackTrace: st);
      rethrow;
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Flower Scout',
      theme: AppTheme.lightTheme,
      home: FutureBuilder<void>(
        future: _initFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState != ConnectionState.done) {
            return const _SplashScreen();
          }
          if (snapshot.hasError) {
            return _SplashErrorScreen(
              error: snapshot.error.toString(),
              onRetry: _retry,
            );
          }
          return ProviderScope(
            overrides: [
              localeProvider.overrideWith(() => LocaleNotifier.withInitial(initialLocale)),
            ],
            child: const FlowerScoutApp(),
          );
        },
      ),
    );
  }
}

class _SplashScreen extends StatelessWidget {
  const _SplashScreen();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F4EF),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 96, height: 96,
              decoration: BoxDecoration(
                color: const Color(0xFFD4AF37).withValues(alpha: 0.15),
                shape: BoxShape.circle,
              ),
              child: const Icon(Icons.local_florist, size: 52, color: Color(0xFF2E7D32)),
            ),
            const SizedBox(height: 24),
            const SizedBox(
              width: 26, height: 26,
              child: CircularProgressIndicator(strokeWidth: 2.5, color: Color(0xFF2E7D32)),
            ),
          ],
        ),
      ),
    );
  }
}

class _SplashErrorScreen extends StatelessWidget {
  final String error;
  final VoidCallback onRetry;
  const _SplashErrorScreen({required this.error, required this.onRetry});
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F4EF),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(28),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.wifi_off_rounded, size: 40, color: Color(0xFFB53030)),
              const SizedBox(height: 14),
              const Text('Could not start the app',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700, color: Color(0xFF2C2C2A))),
              const SizedBox(height: 6),
              Text(error, textAlign: TextAlign.center,
                  style: const TextStyle(fontSize: 12, color: Color(0xFF7A8C7E))),
              const SizedBox(height: 20),
              ElevatedButton.icon(
                onPressed: onRetry,
                icon: const Icon(Icons.refresh_rounded, size: 18),
                label: const Text('Retry'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF2E7D32),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
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
    // Restored session on cold start: role/profile wasn't loaded by the
    // listener below (that only fires on a fresh sign-in event), so load
    // it explicitly here. Without this, a returning user is silently
    // treated as 'scout' until something else refreshes the session.
    if (_loggedIn) _loadProfileForCurrentUser();

    Supabase.instance.client.auth.onAuthStateChange.listen((data) async {
      if (!mounted) return;
      final event   = data.event;
      final session = data.session;
      if (session != null &&
          (event == AuthChangeEvent.signedIn ||
           event == AuthChangeEvent.userUpdated ||
           event == AuthChangeEvent.passwordRecovery)) {
        await _loadProfileForCurrentUser();
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

  Future<void> _loadProfileForCurrentUser() async {
    try {
      final uid = Supabase.instance.client.auth.currentUser?.id;
      if (uid == null) return;
      final row = await Supabase.instance.client
          .from('user_profiles')
          .select('role, full_name')
          .eq('id', uid)
          .single()
          .timeout(const Duration(seconds: 10));
      final role = row['role'] as String? ?? 'scout';
      UserSession.currentUser    = row['full_name'] as String? ?? '';
      UserSession.currentProfile = switch (role) {
        'system_admin' => UserProfile.systemAdmin,
        'manager'      => UserProfile.manager,
        _              => UserProfile.scout,
      };
    } catch (e) {
      // Don't crash the auth flow over a failed profile lookup, but don't
      // pretend it succeeded either - this is worth knowing about in logs.
      debugPrint('[auth] failed to load user profile: \$e');
    }
  }

  @override
  Widget build(BuildContext context) {
    ref.watch(localeProvider);
    return _loggedIn ? const AppShell() : const LoginScreen();
  }
}
"""

p.write_text(content, encoding='utf-8')
print(f"Rewrote {p} ({len(content)} chars)")