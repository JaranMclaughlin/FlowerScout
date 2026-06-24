import pathlib
p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
t = p.read_text(encoding='utf-8')

old2 = '                decoration:BoxDecoration(color:medals[rank-1].withValues(alpha:0.15),'
new2 = '                decoration:BoxDecoration(color:medals[(rank-1).clamp(0,2)].withValues(alpha:0.15),'
old3 = '                    color:medals[rank-1])))),\n'
new3 = '                    color:medals[(rank-1).clamp(0,2)]))),\n'

if old2 not in t: raise SystemExit('anchor 2 not found')
if old3 not in t: raise SystemExit('anchor 3 not found')
t = t.replace(old2, new2, 1).replace(old3, new3, 1)
p.write_text(t, encoding='utf-8')
print('Fixed: medals index clamped.')