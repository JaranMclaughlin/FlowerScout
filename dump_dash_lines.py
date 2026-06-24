import pathlib
p = pathlib.Path('lib/features/dashboard/presentation/dashboard_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
out = []
for i in [88,96,140,148,153,160,288,296,327,335,394,402,434,442,516,524]:
    if i <= len(lines):
        out.append(f'{i}: {lines[i-1]}')
pathlib.Path('dash_lines.txt').write_text('\n'.join(out), encoding='utf-8')
print('done')