import pathlib
p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
out = []
for i,ln in enumerate(lines,1):
    s = ln.strip()
    if any(w in s for w in [
        'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec',
        'Mon','Tue','Wed','Thu','Fri','Sat','Sun',
        'Today','Yesterday','ago','hour','minute','second',
        'AM','PM','am','pm','duration','Duration',
        "'s.'", "= '", "Text('", "title:'", "label:'",
    ]) and 's.' not in s and '_t(' not in s and not s.startswith('//'):
        out.append(f'{i}: {s[:120]}')
pathlib.Path('scouting_hardcoded.txt').write_text('\n'.join(out), encoding='utf-8')
print('done')