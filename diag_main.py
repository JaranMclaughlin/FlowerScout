import pathlib

p = pathlib.Path('lib/main.dart')
lines = p.read_text(encoding='utf-8').split('\n')
for i, l in enumerate(lines, 1):
    print(f"{i}: {l}")