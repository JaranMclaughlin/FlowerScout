import pathlib
p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i in [983,984,985,986,987,988, 1001,1002,1003,1004,1005,1006,1007, 1028,1029,1030,1031,1032,1033, 941,942,943,944,945]:
    print(f"{i+1}\t{repr(lines[i])}")