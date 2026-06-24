import pathlib
p = pathlib.Path('lib/shared/providers/analytics_data.dart')
lines = p.read_text(encoding='utf-8').splitlines()
out = []
for i,ln in enumerate(lines[27:95],28):
    out.append(f'{i}: {ln}')
pathlib.Path('analytics_data_fns.txt').write_text('\n'.join(out), encoding='utf-8')
print('done')