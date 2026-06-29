import pathlib
p = pathlib.Path('lib/features/auth/presentation/location_permission_screen.dart')
lines = p.read_text(encoding='utf-8', errors='replace').splitlines()
for i,ln in enumerate(lines[0:15],1):
    print(f'{i}: {ln}')