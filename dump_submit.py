import pathlib
p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i, line in enumerate(lines[170:330], start=171):
    print(f"{i}\t{repr(lines[i-1])}")