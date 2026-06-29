import pathlib

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')

print("=== Lines 826-880 (issue field + card closing) ===")
for i, l in enumerate(lines[825:880], 826):
    print(f"{i}: {l}")