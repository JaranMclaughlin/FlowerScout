import pathlib
p = pathlib.Path('lib/features/scouting/presentation/topbar_widgets.dart')
lines = p.read_text(encoding='utf-8', errors='replace').splitlines()
for i,ln in enumerate(lines[490:520],491):
    print(f'{i}: {ln}')
for i,ln in enumerate(lines[860:875],861):
    print(f'{i}: {ln}')