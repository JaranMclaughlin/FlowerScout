import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
t = p.read_text(encoding='utf-8')

for field in ['canopy', 'mint', 'blueBg']:
    old = f'  static const {field}    ='
    new = f'  // ignore: unused_field\n  static const {field}    ='
    if old in t:
        t = t.replace(old, new, 1)
        print(f"OK: suppressed {field}")
    else:
        # try with varying spaces
        import re
        pattern = f'  static const {field}\\s+='
        match = re.search(pattern, t)
        if match:
            t = t[:match.start()] + f'  // ignore: unused_field\n' + t[match.start():]
            print(f"OK (regex): suppressed {field}")
        else:
            print(f"MISS: {field} not found")

p.write_text(t, encoding='utf-8')