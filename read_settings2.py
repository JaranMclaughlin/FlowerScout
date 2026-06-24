import pathlib
text = pathlib.Path('lib/features/settings/presentation/settings_screen.dart').read_text(encoding='utf-8')
lines = text.splitlines()
out = []
for i,ln in enumerate(lines[120:260],121):
    s = ln.strip()
    if s: out.append(f'{i}: {s[:100]}')
pathlib.Path('settings_dump.txt').write_text('\n'.join(out[:50]), encoding='utf-8')
print('done')