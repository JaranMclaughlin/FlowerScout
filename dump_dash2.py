import pathlib
p = pathlib.Path('lib/features/dashboard/presentation/dashboard_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i, line in enumerate(lines[:15], start=1):
    print(f"{i}\t{repr(line)}")