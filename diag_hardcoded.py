import pathlib, re

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')

targets = ['APPEARANCE', 'THEME', 'DATE FORMAT', 'MAP DEFAULTS', 
           'DEFAULT VIEW', 'ABOUT', 'INSPECTION DEFAULTS', 
           'INVITE A NEW MEMBER', "'ROLE'", "'EMAIL'",
           'Satellite', 'Terrain', 'Street',
           "'scout'", "'viewer'", "'manager'",
           'DD/MM/YYYY', 'MM/DD/YYYY']

for i, line in enumerate(lines, 1):
    if any(t in line for t in targets):
        print(f"{i}: {line}")