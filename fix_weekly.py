import pathlib
p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
t = p.read_text(encoding='utf-8')
old = "            'Every Monday 7 AM \u2014 farm health digest',"
new = "            s.weeklyDescFull,"
if old not in t: raise SystemExit('anchor not found')
t = t.replace(old, new, 1)
p.write_text(t, encoding='utf-8')
print('Fixed weekly digest string.')