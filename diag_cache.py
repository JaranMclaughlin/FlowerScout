import pathlib

p = pathlib.Path('lib/shared/providers/farm_repository.dart')
lines = p.read_text(encoding='utf-8').split('\n')

print("=== Lines 200-215 ===")
for i, l in enumerate(lines[199:215], 200):
    print(f"{i}: {l}")

print("\n=== Lines 248-260 ===")
for i, l in enumerate(lines[247:260], 248):
    print(f"{i}: {l}")