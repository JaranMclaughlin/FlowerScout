import pathlib
p = pathlib.Path('lib/features/maps/presentation/maps_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
out = []
for i,ln in enumerate(lines[0:120],1):
    out.append(f'{i}: {ln}')
print('\n'.join(out))