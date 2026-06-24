import pathlib
p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
out = []
for i,ln in enumerate(lines[155:180],156):
    out.append(f'{i}: {ln}')
print('\n'.join(out))