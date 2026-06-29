import pathlib

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')

print("=== Lines 168-180 (class name check) ===")
for i, l in enumerate(lines[167:180], 168):
    print(f"{i}: {l}")

print("\n=== Lines 720-740 (submit button end) ===")
for i, l in enumerate(lines[719:740], 720):
    print(f"{i}: {l}")