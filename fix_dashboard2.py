import pathlib
p = pathlib.Path('lib/features/dashboard/presentation/dashboard_screen.dart')
t = p.read_text(encoding='utf-8')

# Fix isPrimary check
old1 = "final isPrimary = a.$2 == 'New Report';"
new1 = "final isPrimary = a.$2 == s.newReport;"
if old1 in t:
    t = t.replace(old1, new1, 1)
else:
    print('MISSED isPrimary - searching...')
    for i,ln in enumerate(t.splitlines(),1):
        if 'isPrimary' in ln: print(f'{i}: {repr(ln)}')

# Fix inactive GH badge
old2 = "child: Text('${g.code} inactive', style: TextStyle(fontSize: 11,"
new2 = "child: Text('${g.code} ${s.inactive}', style: TextStyle(fontSize: 11,"
if old2 in t:
    t = t.replace(old2, new2, 1)
else:
    print('MISSED inactive - searching...')
    for i,ln in enumerate(t.splitlines(),1):
        if 'inactive' in ln and 'g.code' in ln: print(f'{i}: {repr(ln)}')

p.write_text(t, encoding='utf-8')
print('done')