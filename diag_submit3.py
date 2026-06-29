import pathlib

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')
print("=== Lines 194-235 (submit success block) ===")
for i, l in enumerate(lines[193:235], 194):
    print(f"{i}: {l}")