import pathlib
p = pathlib.Path('lib/shared/trail/data/trail_repository.dart')
lines = p.read_text(encoding='utf-8', errors='replace').splitlines()
for i,ln in enumerate(lines,1):
    print(f'{i}: {ln}')