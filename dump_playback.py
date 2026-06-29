import pathlib
p = pathlib.Path('lib/features/maps/presentation/maps_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i,ln in enumerate(lines[285:360],286):
    print(f'{i}: {ln}')