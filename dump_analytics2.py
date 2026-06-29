import pathlib
p = pathlib.Path('lib/shared/providers/analytics_data.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i, line in enumerate(lines[10:30], start=11):
    print(f"{i}\t{repr(line)}")