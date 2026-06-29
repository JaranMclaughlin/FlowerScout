import pathlib

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')

print("=== Lines 72-130 (initState) ===")
for i, l in enumerate(lines[71:130], 72):
    print(f"{i}: {l}")