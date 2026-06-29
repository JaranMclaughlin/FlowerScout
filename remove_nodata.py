import pathlib

p = pathlib.Path('lib/shared/l10n/app_strings.dart')
txt = p.read_text(encoding='utf-8', errors='replace')
txt = txt.replace(
    "  String get noData             => _t('No data',                'Hakuna data');\n",
    ""
)
p.write_text(txt, encoding='utf-8')
print('done')