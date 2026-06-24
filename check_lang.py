import pathlib, re

p = pathlib.Path('lib/features/auth/presentation/login_screen.dart')
txt = p.read_text(encoding='utf-8')

matches = re.findall(r'setLanguage\([^)]+\)', txt)
for m in matches:
    print('Found:', repr(m))
    print('Hex:  ', m.encode('utf-8').hex())