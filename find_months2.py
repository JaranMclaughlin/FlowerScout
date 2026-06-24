import pathlib
p = pathlib.Path('lib/shared/providers/analytics_data.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i,ln in enumerate(lines[33:45],34):
    print(f'{i}: {repr(ln)}')