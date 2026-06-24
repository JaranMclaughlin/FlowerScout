import pathlib
p = pathlib.Path('lib/features/dashboard/presentation/dashboard_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
out = []
# Get ranges around the error lines
for start,end in [(150,165),(285,300),(325,340),(388,410),(430,445),(512,535)]:
    out.append(f'--- {start}-{end} ---')
    for i,ln in enumerate(lines[start-1:end],start):
        out.append(f'{i}: {ln}')
pathlib.Path('dash_ctx.txt').write_text('\n'.join(out), encoding='utf-8')
print('done')