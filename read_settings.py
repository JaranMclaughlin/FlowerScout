import pathlib
text = pathlib.Path('lib/features/settings/presentation/settings_screen.dart').read_text(encoding='utf-8')
lines = text.splitlines()
for i,ln in enumerate(lines[120:260],121):
    s = ln.strip()
    if s: print(f'{i}: {s[:100]}')