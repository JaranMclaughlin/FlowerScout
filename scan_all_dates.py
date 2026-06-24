import pathlib

files = list(pathlib.Path('lib').rglob('*.dart'))
out = []
for f in sorted(files):
    if 'app_strings' in f.name: continue
    text = f.read_text(encoding='utf-8')
    hits = []
    for i,ln in enumerate(text.splitlines(),1):
        s = ln.strip()
        if any(w in s for w in ["'Mon'","'Tue'","'Wed'","'Thu'","'Fri'","'Sat'","'Sun'",
                                  "'Jan'","'Feb'","'Mar'","'Apr'","'May'","'Jun'",
                                  "'Jul'","'Aug'","'Sep'","'Oct'","'Nov'","'Dec'"]):
            hits.append(f'  {i}: {s[:120]}')
    if hits:
        out.append(f'\n=== {f} ===')
        out.extend(hits)

pathlib.Path('all_dates.txt').write_text('\n'.join(out), encoding='utf-8')
print('done')