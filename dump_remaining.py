import pathlib
p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i in [297,298,299, 313,314,315, 412,413,414, 416,417,418, 420,421,422,423, 650,651,652, 1208,1209,1210]:
    print(f"{i+1}\t{repr(lines[i])}")