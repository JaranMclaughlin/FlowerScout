import pathlib
p = pathlib.Path('lib/shared/providers/farm_repository.dart')
lines = p.read_text(encoding='utf-8', errors='replace').splitlines()
for i,ln in enumerate(lines[280:310],281):
    print(f'{i}: {ln}')