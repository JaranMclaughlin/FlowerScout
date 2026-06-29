import pathlib

lib = pathlib.Path('lib')
results = []
for f in lib.rglob('*.dart'):
    txt = f.read_text(encoding='utf-8', errors='ignore')
    lines = txt.splitlines()
    for i,ln in enumerate(lines,1):
        s = ln.strip()
        # Find fake/mock/stub patterns
        if any(x in s.lower() for x in ['// fake','// stub','fake data','mock data','dummy','sample data','test data','placeholder','todo','fixme']):
            results.append(f'{f.name}:{i}: {s[:120]}')

pathlib.Path('fakes.txt').write_text('\n'.join(results), encoding='utf-8')
print(f'Found {len(results)} items')