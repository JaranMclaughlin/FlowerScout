import pathlib

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')
print("=== Lines 726-742 ===")
for i, l in enumerate(lines[725:742], 726):
    print(f"{i}: {repr(l)}")