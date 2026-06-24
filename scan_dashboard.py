import pathlib
for fname in [
    'lib/features/dashboard/presentation/dashboard_screen.dart',
]:
    p = pathlib.Path(fname)
    if not p.exists(): continue
    lines = p.read_text(encoding='utf-8').splitlines()
    out = []
    for i,ln in enumerate(lines,1):
        s = ln.strip()
        if any(w in s for w in ['Greenhouse Activation','Excellent','Farm Overview','Quick Actions','Report Summary','Total plants','Varieties in use','Active greenhouses','New Report','Open Maps','inactive','Active','Farms','Greenhouses','Plantings','Varieties']):
            out.append(f'{i}: {s[:120]}')
    pathlib.Path('dashboard_hardcoded.txt').write_text('\n'.join(out), encoding='utf-8')
print('done')