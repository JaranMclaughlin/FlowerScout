import pathlib, re

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')

print("=== State class definitions ===")
for i, l in enumerate(lines, 1):
    if re.match(r'class \w+ extends (ConsumerState|State)', l):
        print(f"  {i}: {l}")