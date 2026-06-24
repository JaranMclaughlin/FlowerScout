import pathlib
p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()
out = []
for i,ln in enumerate(lines,1):
    s = ln.strip()
    if 'notif' in s.lower() or 'alert' in s.lower() or 'overdue' in s.lower() or 'push' in s.lower() or 'sms' in s.lower() or 'delivery' in s.lower() or 'inspection alert' in s.lower() or 'weekly' in s.lower():
        out.append(f'{i}: {ln.strip()[:120]}')
pathlib.Path('settings_notif.txt').write_text('\n'.join(out), encoding='utf-8')
print('done')