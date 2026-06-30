import pathlib

p = pathlib.Path('lib/main.dart')
lines = p.read_text(encoding='utf-8').split('\n')
print("=== Lines 1-30 (imports) ===")
for i, l in enumerate(lines[:30], 1):
    print(f"{i}: {l}")
print("\n=== Lines 225-290 ===")
for i, l in enumerate(lines[224:290], 225):
    print(f"{i}: {l}")