import pathlib

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')

for i, l in enumerate(lines, 1):
    if "'EMAIL'" in l or "'ROLE'" in l or "label: 'TEAM" in l:
        print(f"{i}: {l}")