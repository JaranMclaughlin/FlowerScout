import pathlib
p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
out = [f'{i}: {ln}' for i,ln in enumerate(lines[184:198],185)]
pathlib.Path('settings_line190.txt').write_text('\n'.join(out), encoding='utf-8')
print('done')