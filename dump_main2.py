import pathlib
p = pathlib.Path('lib/main.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i, line in enumerate(lines[185:215], start=186):
    print(f"{i}\t{repr(line)}")