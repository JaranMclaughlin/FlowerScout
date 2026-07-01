import pathlib
p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i, line in enumerate(lines[1395:1430], start=1396):
    print(f"{i}\t{repr(lines[i-1])}")