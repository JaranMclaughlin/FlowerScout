import pathlib

for p in pathlib.Path('lib').rglob('*.dart'):
    text = p.read_text(encoding='utf-8', errors='ignore')
    if 'UserSession.currentUser' in text:
        lines = text.splitlines()
        for i, line in enumerate(lines, start=1):
            if 'UserSession.currentUser' in line:
                print(f"{p}:{i}\t{line.strip()}")