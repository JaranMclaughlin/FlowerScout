import pathlib
p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i, line in enumerate(lines, start=1):
    if any(x in line for x in ['_fetchInspections', 'select(', 'scout_name', 'greenhouse_code', 'inspection_findings']):
        for j in range(max(0,i-1), min(len(lines),i+4)):
            print(f"{j+1}\t{repr(lines[j])}")
        print("---")