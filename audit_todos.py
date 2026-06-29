import pathlib, re

lib = pathlib.Path('lib')
results = []
for f in lib.rglob('*.dart'):
    txt = f.read_text(encoding='utf-8', errors='ignore')
    lines = txt.splitlines()
    for i,ln in enumerate(lines,1):
        s = ln.strip()
        # Find TODOs, FIXMEs, mock data, hardcoded IDs
        if any(x in s.upper() for x in ['TODO','FIXME','HACK','MOCK','PLACEHOLDER','HARDCODED']):
            results.append(f'{f.name}:{i}: {s[:120]}')

pathlib.Path('todos.txt').write_text('\n'.join(results), encoding='utf-8')
print(f'Found {len(results)} items')