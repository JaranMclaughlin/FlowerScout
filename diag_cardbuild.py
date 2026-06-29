import pathlib

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')

print("=== Lines 960-1010 (finding card build method) ===")
for i, l in enumerate(lines[959:1010], 960):
    print(f"{i}: {l}")