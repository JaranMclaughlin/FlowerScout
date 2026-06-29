import pathlib

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')

print("=== Lines 168-260 (_submitReport method) ===")
for i, l in enumerate(lines[167:260], 168):
    print(f"{i}: {l}")