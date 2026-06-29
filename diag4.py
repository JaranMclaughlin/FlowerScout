import pathlib, re

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')

print("=== Line 25-32 (heading field) ===")
for i, l in enumerate(lines[24:32], 25):
    print(f"{i}: {l}")

print("\n=== Lines 640-650 (leftover s variable) ===")
for i, l in enumerate(lines[639:650], 640):
    print(f"{i}: {l}")