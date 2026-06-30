import pathlib, shutil

# ── Fix 1: main.dart - wire onboarding into auth gate ────────────────────────
p = pathlib.Path('lib/main.dart')
shutil.copy(p, p.with_suffix('.dart.bak2'))
t = p.read_text(encoding='utf-8')

# Add onboarding import
old_import = "import 'features/auth/presentation/login_screen.dart';"
new_import = """import 'features/auth/presentation/login_screen.dart';
import 'features/onboarding/presentation/onboarding_screen.dart';"""
if old_import in t and 'onboarding_screen' not in t:
    t = t.replace(old_import, new_import, 1)
    print("Fix 1a: added onboarding import")

# Add _seenOnboarding state field
old_field = "  bool _loggedIn = false;"
new_field = """  bool _loggedIn = false;
  bool _seenOnboarding = true; // assume seen until async check completes"""
if old_field in t:
    t = t.replace(old_field, new_field, 1)
    print("Fix 1b: added _seenOnboarding field")

# Check onboarding in initState
old_initstate = """    _loggedIn = Supabase.instance.client.auth.currentSession != null;
    // Restored session on cold start: role/profile wasn't loaded by the"""
new_initstate = """    _loggedIn = Supabase.instance.client.auth.currentSession != null;
    // Check if user has seen onboarding
    hasSeenOnboarding().then((seen) {
      if (mounted) setState(() => _seenOnboarding = seen);
    });
    // Restored session on cold start: role/profile wasn't loaded by the"""
if old_initstate in t:
    t = t.replace(old_initstate, new_initstate, 1)
    print("Fix 1c: onboarding check wired into initState")

# Fix build to show onboarding when not seen and not logged in
old_build = """  @override
  Widget build(BuildContext context) {
    ref.watch(localeProvider);
    return _loggedIn ? const AppShell() : const LoginScreen();
  }"""
new_build = """  @override
  Widget build(BuildContext context) {
    ref.watch(localeProvider);
    if (!_loggedIn) {
      return _seenOnboarding ? const LoginScreen() : const OnboardingScreen();
    }
    return const AppShell();
  }"""
if old_build in t:
    t = t.replace(old_build, new_build, 1)
    print("Fix 1d: build routes through onboarding correctly")
else:
    print("ERROR: build anchor not found"); raise SystemExit(1)

p.write_text(t, encoding='utf-8')

# ── Fix 2: app_shell.dart - capture context before async gap ─────────────────
p2 = pathlib.Path('lib/shared/widgets/app_shell.dart')
t2 = p2.read_text(encoding='utf-8')

old_signout = """        onTap: () async {
          final confirm = await showDialog<bool>(
            context: context,
            builder: (_) => AlertDialog("""
new_signout = """        onTap: () async {
          final nav = Navigator.of(context); // capture before async gap
          final confirm = await showDialog<bool>(
            context: context,
            builder: (_) => AlertDialog("""
if old_signout in t2:
    t2 = t2.replace(old_signout, new_signout, 1)
    print("Fix 2a: captured Navigator before async gap")
else:
    print("ERROR: signout onTap anchor not found"); raise SystemExit(1)

# Use captured nav instead of Navigator.of(context)
old_nav = """            if (!mounted) return;
            Navigator.of(context).pushAndRemoveUntil(
              MaterialPageRoute(builder: (_) => const LoginScreen()),
              (route) => false,
            );"""
new_nav = """            if (!mounted) return;
            nav.pushAndRemoveUntil(
              MaterialPageRoute(builder: (_) => const LoginScreen()),
              (route) => false,
            );"""
if old_nav in t2:
    t2 = t2.replace(old_nav, new_nav, 1)
    print("Fix 2b: using captured Navigator for post-signout navigation")
else:
    print("ERROR: Navigator anchor not found"); raise SystemExit(1)

p2.write_text(t2, encoding='utf-8')
print("\nDone.")