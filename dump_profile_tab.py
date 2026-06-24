import pathlib
p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i,ln in enumerate(lines[440:510],441):
    print(f'{i}: {ln}')