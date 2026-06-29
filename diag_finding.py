import pathlib

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')

print("=== Lines 1-45 (imports + FindingData class) ===")
for i, l in enumerate(lines[0:45], 1):
    print(f"{i}: {l}")

print("\n=== Lines 754-830 (_FindingCardState) ===")
for i, l in enumerate(lines[753:830], 754):
    print(f"{i}: {l}")