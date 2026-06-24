import pathlib
p = pathlib.Path('lib/shared/providers/analytics_data.dart')
lines = p.read_text(encoding='utf-8').splitlines()
out = []
for i,ln in enumerate(lines,1):
    s = ln.strip()
    if s.startswith('class ') or s.startswith('static ') or s.startswith('factory ') or s.startswith('Future') or 'lang' in s or 'AppStrings' in s:
        out.append(f'{i}: {ln.strip()[:100]}')
pathlib.Path('analytics_data_structure.txt').write_text('\n'.join(out), encoding='utf-8')
print('done')