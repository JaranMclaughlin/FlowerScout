import pathlib
p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i in [229,230,231,232,233, 306,307,308,309,310]:
    print(f"{i+1}\t{repr(lines[i])}")