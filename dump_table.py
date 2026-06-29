import pathlib
p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i, line in enumerate(lines, start=1):
    if any(x in line for x in ['inspectorId', 'inspector', 'r.date', 'r.gh', 'r.variety', 'r.category', 'r.severity', 'buildTableRow', '_buildTableRow', 'headers']):
        for j in range(max(0,i-1), min(len(lines),i+3)):
            print(f"{j+1}\t{repr(lines[j])}")
        print("---")