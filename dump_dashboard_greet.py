import pathlib
p = pathlib.Path('lib/features/dashboard/presentation/dashboard_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i,ln in enumerate(lines[268:290],269):
    print(f'{i}: {ln}')
for i,ln in enumerate(lines[545:560],546):
    print(f'{i}: {ln}')