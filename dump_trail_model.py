import pathlib
p = pathlib.Path('lib/shared/trail/models/scout_trail.dart')
lines = p.read_text(encoding='utf-8', errors='replace').splitlines()
for i,ln in enumerate(lines,1):
    print(f'{i}: {ln}')