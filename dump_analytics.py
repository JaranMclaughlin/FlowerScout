import pathlib
p = pathlib.Path('lib/features/analytics/presentation/analytics_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
# Show imports and key lines
ranges = [(1,15),(44,52),(238,282),(254,272)]
out = []
for start,end in ranges:
    out.append(f'--- lines {start}-{end} ---')
    for i,ln in enumerate(lines[start-1:end],start):
        out.append(f'{i}: {ln}')
pathlib.Path('analytics_dump.txt').write_text('\n'.join(out), encoding='utf-8')
print('done')