import pathlib
p = pathlib.Path('lib/features/auth/presentation/login_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i,ln in enumerate(lines[36:70],37):
    print(f'{i}: {ln}')