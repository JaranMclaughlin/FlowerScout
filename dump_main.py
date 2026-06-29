import pathlib
p = pathlib.Path('lib/main.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i, line in enumerate(lines[:20], start=1):
    print(f"{i}\t{repr(line)}")