import pathlib
p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i in [1123,1124,1125,1132,1133,1134,1135,1136,1159,1160,1163,1164]:
    print(f"{i+1}\t{repr(lines[i])}")