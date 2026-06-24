import pathlib
p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
t = p.read_text(encoding='utf-8')

old = '                    color:medals[(rank-1).clamp(0,2)]))),\n'
new = '                    color:medals[(rank-1).clamp(0,2)])))),\n'

if old not in t: raise SystemExit('anchor not found')
t = t.replace(old, new, 1)
p.write_text(t, encoding='utf-8')
print('Fixed: restored missing closing paren.')