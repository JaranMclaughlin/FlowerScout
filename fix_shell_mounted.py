import pathlib, shutil

p = pathlib.Path('lib/shared/widgets/app_shell.dart')
shutil.copy(p, p.with_suffix('.dart.bak'))
text = p.read_text(encoding='utf-8')

old_signout = """          if (confirm == true) {
            await Supabase.instance.client.auth.signOut();
            if (mounted) {
              Navigator.of(context).pushAndRemoveUntil(
                MaterialPageRoute(builder: (_) => const LoginScreen()),
                (route) => false,
              );
            }
          }"""

new_signout = """          if (confirm == true) {
            await Supabase.instance.client.auth.signOut();
            if (!mounted) return;
            Navigator.of(context).pushAndRemoveUntil(
              MaterialPageRoute(builder: (_) => const LoginScreen()),
              (route) => false,
            );
          }"""

if old_signout in text:
    text = text.replace(old_signout, new_signout, 1)
    p.write_text(text, encoding='utf-8')
    print("Fixed: mounted check before Navigator in sign-out")
else:
    print("ERROR: sign-out anchor not found")