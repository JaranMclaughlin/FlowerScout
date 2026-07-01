import pathlib
p = pathlib.Path('lib/shared/l10n/app_strings.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i, line in enumerate(lines, start=1):
    if 'chartLabelsWeek' in line:
        for j in range(max(0,i-2), min(len(lines),i+8)):
            print(f"{j+1}\t{repr(lines[j])}")
        print("---")