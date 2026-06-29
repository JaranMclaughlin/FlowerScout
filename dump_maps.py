import pathlib
p = pathlib.Path('lib/features/maps/presentation/maps_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i in [248,249,250,251,252]:
    print(f"{i+1}\t{repr(lines[i])}")