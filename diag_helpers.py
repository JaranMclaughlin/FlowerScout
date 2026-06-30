import pathlib

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')

# Find _themeLabel and _labeledDropdown to inject after
for i, l in enumerate(lines, 1):
    if '_themeLabel' in l or '_mapKeys' in l or '_dateKeys' in l or '_roleKeys' in l:
        print(f"{i}: {l}")