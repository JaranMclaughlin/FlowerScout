import pathlib
p = pathlib.Path('lib/shared/providers/analytics_data.dart')
t = p.read_text(encoding='utf-8')

# Fix months - exact two-line format
old1 = "        const months = ['Jan','Feb','Mar','Apr','May','Jun',\n                        'Jul','Aug','Sep','Oct','Nov','Dec'];"
new1 = "        final months = AppStrings.of(lang).monthsShort;"
if old1 in t:
    t = t.replace(old1, new1, 1)
    print('months fixed')
else:
    print('MISSED - trying alternate')
    # Try finding the function signature to understand lang param
    for i,ln in enumerate(t.splitlines(),1):
        if 'factory' in ln or 'static' in ln or 'Future' in ln or 'fromRow' in ln or 'def ' in ln:
            print(f'{i}: {ln.strip()[:100]}')

p.write_text(t, encoding='utf-8')