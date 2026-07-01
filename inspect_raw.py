import pathlib
p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
print("LINE 1115 RAW BYTES:")
print(lines[1114].encode('unicode_escape'))
print()
print("LINE 1309 RAW BYTES:")
print(lines[1308].encode('unicode_escape'))