import pathlib
p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
lines = p.read_text(encoding='utf-8', errors='replace').splitlines()
for i,ln in enumerate(lines[28:45],29):
    print(f'{i}: {ln}')