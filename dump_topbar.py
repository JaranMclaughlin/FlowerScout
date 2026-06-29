import pathlib
p = pathlib.Path('lib/features/scouting/presentation/topbar_widgets.dart')
lines = p.read_text(encoding='utf-8', errors='replace').splitlines()
for i,ln in enumerate(lines[0:50],1):
    print(f'{i}: {ln}')