import pathlib
p = pathlib.Path('lib/main.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i, line in enumerate(lines[220:270], start=221):
    print(f"{i}\t{repr(lines[i-1])}")