import pathlib

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')

print("=== Lines 55-75 (_theme field + class context) ===")
for i, l in enumerate(lines[54:75], 55):
    print(f"{i}: {l}")

print("\n=== Lines 670-695 (theme dropdown block) ===")
for i, l in enumerate(lines[669:695], 670):
    print(f"{i}: {l}")

print("\n=== Lines 808-825 (_themeKeys + _themeLabel) ===")
for i, l in enumerate(lines[807:825], 808):
    print(f"{i}: {l}")

print("\n=== Lines 925-950 (async context area) ===")
for i, l in enumerate(lines[924:950], 925):
    print(f"{i}: {l}")