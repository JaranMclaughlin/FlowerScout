import pathlib

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')
print("=== Lines 702-735 ===")
for i, l in enumerate(lines[701:735], 702):
    print(f"{i}: {repr(l)}")