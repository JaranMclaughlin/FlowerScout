import pathlib
p = pathlib.Path('lib/shared/l10n/app_strings.dart')
text = p.read_text(encoding='utf-8')
import re
for m in re.finditer(r'chartLabelsWeek\w*\s*=>\s*\[[^\]]*\]', text):
    print(m.group(0))
    print('---')