import pathlib

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')
print("=== Lines 290-350 (submit success + reset) ===")
for i, l in enumerate(lines[289:355], 290):
    print(f"{i}: {l}")