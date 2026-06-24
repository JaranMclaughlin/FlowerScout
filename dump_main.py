import pathlib
p = pathlib.Path('lib/main.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i,ln in enumerate(lines[80:110],81):
    print(f'{i}: {ln}')