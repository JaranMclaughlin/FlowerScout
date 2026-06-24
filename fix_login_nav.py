import pathlib

p = pathlib.Path('lib/features/auth/presentation/login_screen.dart')
txt = p.read_text(encoding='utf-8')

txt = txt.replace(
    '      if (!mounted) return;\n      setState(() => _loading = false);\n      Navigator.of(context).pushReplacement(\n        MaterialPageRoute(builder: (_) => const AppShell()),\n      );',
    '      if (!mounted) return;\n      setState(() => _loading = false);'
)

p.write_text(txt, encoding='utf-8')
print('done')