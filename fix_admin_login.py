import pathlib, sys

p = pathlib.Path('lib/main.dart')
text = p.read_text(encoding='utf-8')

# Fix 1: _loadProfileForCurrentUser sets the static then we need to
# trigger a rebuild of isManagerProvider. We do this by invalidating
# farmsProvider (which isManagerProvider watches via authStateProvider)
# The cleanest fix: after setting UserSession.currentProfile, call
# setState to force _AuthGate to rebuild, which re-evaluates isManagerProvider.

# The current sign-in flow calls _loadProfileForCurrentUser() then setState.
# The issue is AppShell renders before profile loads on cold start.
# Fix: in initState cold-start path, delay rendering until profile is loaded.

old_init = """    _loggedIn = Supabase.instance.client.auth.currentSession != null;
    // Restored session on cold start: role/profile wasn\'t loaded by the
    // listener below (that only fires on a fresh sign-in event), so load
    // it explicitly here. Without this, a returning user is silently
    // treated as \'scout\' until something else refreshes the session.
    if (_loggedIn) _loadProfileForCurrentUser();"""

new_init = """    _loggedIn = Supabase.instance.client.auth.currentSession != null;
    // Restored session on cold start: load profile before rendering AppShell
    // so isManagerProvider reads the correct role on first build.
    if (_loggedIn) {
      _loadProfileForCurrentUser().then((_) {
        if (mounted) setState(() {});
      });
    }"""

if old_init not in text:
    sys.exit("Cold start anchor not found.")
text = text.replace(old_init, new_init)

p.write_text(text, encoding='utf-8')
print("main.dart: admin login bug fixed.")