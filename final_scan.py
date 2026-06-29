import pathlib, re

lib = pathlib.Path('lib')
results = []
skip_files = ['app_strings.dart']
for f in lib.rglob('*.dart'):
    if f.name in skip_files:
        continue
    txt = f.read_text(encoding='utf-8', errors='ignore')
    lines = txt.splitlines()
    for i,ln in enumerate(lines,1):
        s = ln.strip()
        if s.startswith('//') or s.startswith('import') or 'print(' in s:
            continue
        matches = re.findall(r"'([A-Z][a-z]+(?: [A-Za-z]+){1,6})'", ln)
        for m in matches:
            if len(m) > 4:
                results.append(f'{f.name}:{i}: {m}')

pathlib.Path('final_scan.txt').write_text('\n'.join(sorted(set(results))), encoding='utf-8')
print(f'Found {len(set(results))} potential hardcoded strings')