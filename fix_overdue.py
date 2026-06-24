import pathlib

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
txt = p.read_text(encoding='utf-8')

txt = txt.replace(
    "_toggleRow('Overdue inspection reminder',\n            'Notify when a greenhouse passes its inspection date',",
    "_toggleRow(s.overdueReminder,\n            s.overdueDesc,"
)

p.write_text(txt, encoding='utf-8')
print('done')