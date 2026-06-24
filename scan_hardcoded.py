import pathlib, re

lib = pathlib.Path('lib')
# Find quoted English strings that look like UI text
results = []
for f in lib.rglob('*.dart'):
    txt = f.read_text(encoding='utf-8', errors='ignore')
    lines = txt.splitlines()
    for i,ln in enumerate(lines,1):
        s = ln.strip()
        # Skip comments, imports, print statements, variable names
        if s.startswith('//') or s.startswith('import') or 'print(' in s:
            continue
        # Find single-quoted strings with spaces (likely UI text)
        matches = re.findall(r"'([A-Z][a-z]+ [^']{3,40})'", ln)
        for m in matches:
            results.append(f'{f}:{i}: {m}')

pathlib.Path('hardcoded_scan.txt').write_text('\n'.join(results), encoding='utf-8')
print(f'Found {len(results)} potential hardcoded strings')