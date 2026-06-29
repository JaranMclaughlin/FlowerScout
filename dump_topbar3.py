import pathlib
p = pathlib.Path('lib/features/scouting/presentation/topbar_widgets.dart')
lines = p.read_text(encoding='utf-8', errors='replace').splitlines()
for i,ln in enumerate(lines[440:480],441):
    print(f'{i}: {ln}')
for i,ln in enumerate(lines[530:560],531):
    print(f'{i}: {ln}')