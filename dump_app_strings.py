import pathlib
p = pathlib.Path('lib/shared/l10n/app_strings.dart')
lines = p.read_text(encoding='utf-8').splitlines()
out = []
for i,ln in enumerate(lines,1):
    out.append(f'{i}: {ln}')
pathlib.Path('app_strings_dump.txt').write_text('\n'.join(out), encoding='utf-8')
print('done')