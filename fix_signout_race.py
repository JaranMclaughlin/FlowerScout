import pathlib, sys

# ── 1. app_shell.dart — remove manual navigation, just call signOut ───
p = pathlib.Path('lib/shared/widgets/app_shell.dart')
text = p.read_text(encoding='utf-8')

old = """          if (confirm == true) {
            await Supabase.instance.client.auth.signOut();
            if (!mounted) return;
            Navigator.of(context).pushAndRemoveUntil(
              MaterialPageRoute(builder: (_) => const LoginScreen()),
              (route) => false,
            );"""

new = """          if (confirm == true) {
            // AuthGate's onAuthStateChange listener owns navigation after
            // sign-out — pushing here as well caused a race that froze
            // the screen. Just sign out and let the gate handle the rest.
            await Supabase.instance.client.auth.signOut();"""

if old not in text:
    sys.exit("app_shell.dart anchor not found.")
text = text.replace(old, new, 1)
p.write_text(text, encoding='utf-8')
print("app_shell.dart: manual navigation removed, signOut() only.")

# ── 2. settings_screen.dart — remove the entire sign-out row + dialog ─
p2 = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
text2 = p2.read_text(encoding='utf-8')

old_row = """        _divider(),
        _settingRow(
          label: _s.signOutLabel,
          subtitle: _s.logOut,
          labelColor: const Color(0xFFD32F2F),
          trailing: const Icon(Icons.logout_rounded,
              color: Color(0xFFD32F2F), size: 18),
          onTap: _confirmSignOut,
        ),"""

if old_row not in text2:
    sys.exit("settings_screen.dart row anchor not found.")
text2 = text2.replace(old_row, "        _divider(),", 1)
p2.write_text(text2, encoding='utf-8')
print("settings_screen.dart: sign-out row removed from settings list.")