import pathlib
p = pathlib.Path('lib/features/analytics/presentation/analytics_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
out = []
for i,ln in enumerate(lines,1):
    s = ln.strip()
    if s.startswith('Widget ') or s.startswith('Future ') or 'ref.watch(stringsProvider)' in s or 'final s =' in s:
        out.append(f'{i}: {ln}')
pathlib.Path('analytics_structure.txt').write_text('\n'.join(out), encoding='utf-8')
print('done')