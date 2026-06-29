import pathlib

p = pathlib.Path('lib/shared/providers/farm_repository.dart')
lines = p.read_text(encoding='utf-8').split('\n')
for i, l in enumerate(lines[199:215], 200):
    print(f"{i}: {l}")
print("---")
for i, l in enumerate(lines[247:262], 248):
    print(f"{i}: {l}")