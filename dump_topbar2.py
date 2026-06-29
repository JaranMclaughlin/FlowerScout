import pathlib
p = pathlib.Path('lib/features/scouting/presentation/topbar_widgets.dart')
lines = p.read_text(encoding='utf-8', errors='replace').splitlines()
for i,ln in enumerate(lines[340:365],341):
    print(f'{i}: {ln}')
for i,ln in enumerate(lines[718:800],719):
    print(f'{i}: {ln}')