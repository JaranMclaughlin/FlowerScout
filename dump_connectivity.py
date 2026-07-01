import pathlib
p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i, line in enumerate(lines, start=1):
    if any(x in line for x in ['Connectivity', 'isOnline', 'offline', 'connectivity']):
        for j in range(max(0,i-2), min(len(lines),i+3)):
            print(f"{j+1}\t{repr(lines[j])}")
        print("---")