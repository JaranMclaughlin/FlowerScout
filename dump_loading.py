import pathlib
p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i, line in enumerate(lines, start=1):
    if '_loadingMore' in line and ('bool' in line or 'false' in line):
        print(f"{i}\t{repr(line)}")