import pathlib
p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
out = []
for i,ln in enumerate(lines,1):
    s = ln.strip()
    if s.startswith('class ') or ('Widget build' in s) or ('stringsProvider' in s) or ('final s =' in s):
        out.append(f'{i}: {ln.strip()[:100]}')
pathlib.Path('scouting_structure.txt').write_text('\n'.join(out), encoding='utf-8')
print('done')