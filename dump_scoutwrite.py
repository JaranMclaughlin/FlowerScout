import pathlib
p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i, line in enumerate(lines, start=1):
    if "'scout_id'" in line or "'scout_name'" in line:
        for j in range(max(0,i-1), min(len(lines),i+2)):
            print(f"{j+1}\t{repr(lines[j])}")
        print("---")