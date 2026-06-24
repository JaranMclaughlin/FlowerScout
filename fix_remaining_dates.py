import pathlib

# 1. Fix reports_screen.dart remaining hardcoded labels
p1 = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
t1 = p1.read_text(encoding='utf-8')

old1 = "    chartLabels:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], // default; overridden at runtime"
new1 = "    chartLabels:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],"
t1 = t1.replace(old1, new1, 1)

old2 = "    else { labels=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']; n=7; }"
new2 = "    else { labels=AppStrings.of(lang).chartLabelsWeek; n=7; }"
if old2 not in t1: raise SystemExit('anchor 2 not found')
t1 = t1.replace(old2, new2, 1)

p1.write_text(t1, encoding='utf-8')
print('reports_screen.dart fixed.')

# 2. Fix analytics_data.dart
p2 = pathlib.Path('lib/shared/providers/analytics_data.dart')
t2 = p2.read_text(encoding='utf-8')

# Check imports
if 'app_strings' not in t2:
    # Add import at top
    first_import = t2.index('import ')
    end_of_line = t2.index('\n', first_import)
    t2 = t2[:end_of_line+1] + "import '../l10n/app_strings.dart';\n" + t2[end_of_line+1:]

# Fix months array
old3 = "    const months = ['Jan','Feb','Mar','Apr','May','Jun',\n'Jul','Aug','Sep','Oct','Nov','Dec'];"
if old3 not in t2:
    old3 = "    const months = ['Jan','Feb','Mar','Apr','May','Jun',\n        'Jul','Aug','Sep','Oct','Nov','Dec'];"
new3 = "    final months = AppStrings.of(lang).monthsShort;"
if old3 in t2:
    t2 = t2.replace(old3, new3, 1)
else:
    print('MISSED months in analytics_data - searching...')
    for i,ln in enumerate(t2.splitlines(),1):
        if 'Jan' in ln or 'months' in ln: print(f'{i}: {repr(ln)}')

# Fix default chartLabels
old4 = "    chartLabels: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],"
new4 = "    chartLabels: AppStrings.of(lang).chartLabelsWeek,"
t2 = t2.replace(old4, new4)

# Fix labels in fromFilter
old5 = "    labels = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']; n = 7;"
new5 = "    labels = AppStrings.of(lang).chartLabelsWeek; n = 7;"
t2 = t2.replace(old5, new5)

p2.write_text(t2, encoding='utf-8')
print('analytics_data.dart fixed.')