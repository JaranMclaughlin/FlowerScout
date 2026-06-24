import pathlib
p = pathlib.Path('lib/features/dashboard/presentation/dashboard_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
out = []
for i,ln in enumerate(lines,1):
    s = ln.strip()
    if s.startswith('class ') or 'Widget build' in s or 's.farm' in s or 's.green' in s or 's.quick' in s or 's.report' in s or 's.total' in s or 's.active' in s or 's.inactive' in s or 's.new' in s or 's.open' in s or 's.varieties' in s or 's.planting' in s or 's.ghAct' in s or 's.excellent' in s or 's.noFarms' in s or 's.check' in s:
        out.append(f'{i}: {ln.strip()[:100]}')
pathlib.Path('dash_classes.txt').write_text('\n'.join(out), encoding='utf-8')
print('done')