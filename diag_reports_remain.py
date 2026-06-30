import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')
for i, l in enumerate(lines, 1):
    if 'export failed' in l.lower() or "Text('Retry')" in l or "'Retry'" in l or "Error:" in l:
        print(f"{i}: {repr(l.strip())}")