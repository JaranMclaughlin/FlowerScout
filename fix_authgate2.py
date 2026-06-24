import pathlib

p = pathlib.Path('lib/main.dart')
txt = p.read_text(encoding='utf-8')
txt = txt.replace(
    'return _loggedIn ? const AppShell() : const LoginScreen();',
    'return _loggedIn ? const AppShell() : const LoginScreen();'
)

# The real fix: _AuthGate.build must watch localeProvider so it rebuilds
old = """  @override
  Widget build(BuildContext context) {
    return _loggedIn ? const AppShell() : const LoginScreen();
  }"""

new = """  @override
  Widget build(BuildContext context) {
    ref.watch(localeProvider); // rebuild shell when language changes
    return _loggedIn ? const AppShell() : const LoginScreen();
  }"""

if old in txt:
    txt = txt.replace(old, new)
    print('Fixed: _AuthGate now watches localeProvider')
else:
    print('Pattern not found')

p.write_text(txt, encoding='utf-8')