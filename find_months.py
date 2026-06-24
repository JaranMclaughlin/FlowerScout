import pathlib
p = pathlib.Path('lib/shared/providers/analytics_data.dart')
t = p.read_text(encoding='utf-8')

# Find exact months lines
for i,ln in enumerate(t.splitlines(),1):
    if 'Jan' in ln or ("months" in ln and 'month' in ln.lower()):
        print(f'{i}: {repr(ln)}')