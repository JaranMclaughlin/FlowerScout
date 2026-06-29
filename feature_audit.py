import pathlib

lib = pathlib.Path('lib')
results = {}

for f in lib.rglob('*.dart'):
    txt = f.read_text(encoding='utf-8', errors='ignore')
    lines = txt.splitlines()
    for i,ln in enumerate(lines,1):
        s = ln.strip()
        # Export features
        if 'exportPdf' in s or 'exportExcel' in s or 'Export' in s:
            results.setdefault('EXPORT', []).append(f'{f.name}:{i}: {s[:100]}')
        # AI insight
        if 'aiInsight' in s or 'AI Insight' in s or 'ai_insight' in s:
            results.setdefault('AI', []).append(f'{f.name}:{i}: {s[:100]}')
        # Push notifications real impl
        if 'firebase' in s.lower() or 'fcm' in s.lower() or 'push_notification' in s.lower():
            results.setdefault('PUSH_NOTIF', []).append(f'{f.name}:{i}: {s[:100]}')
        # Weather API key
        if '_apiKey' in s or 'WEATHER' in s.upper() or 'openweather' in s.lower():
            results.setdefault('WEATHER', []).append(f'{f.name}:{i}: {s[:100]}')
        # Error handling gaps
        if 'catch (_)' in s or 'catch (e)' in s:
            results.setdefault('ERROR_HANDLING', []).append(f'{f.name}:{i}: {s[:100]}')
        # Unimplemented buttons
        if 'onPressed: ()' in s or 'onTap: ()' in s:
            results.setdefault('EMPTY_HANDLERS', []).append(f'{f.name}:{i}: {s[:100]}')

out = []
for k,v in results.items():
    out.append(f'\n=== {k} ({len(v)}) ===')
    out.extend(v)

pathlib.Path('feature_audit.txt').write_text('\n'.join(out), encoding='utf-8')
print('done')