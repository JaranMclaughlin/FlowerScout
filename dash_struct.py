import pathlib
p = pathlib.Path('lib/features/dashboard/presentation/dashboard_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
out = []
for i,ln in enumerate(lines,1):
    s = ln.strip()
    if 'stringsProvider' in s or 'final s =' in s or 'Widget build' in s or 'AppStrings' in s or 'localeProvider' in s:
        out.append(f'{i}: {ln}')
pathlib.Path('dash_structure.txt').write_text('\n'.join(out), encoding='utf-8')
print('done')