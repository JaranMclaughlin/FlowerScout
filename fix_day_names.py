import pathlib

p = pathlib.Path('lib/shared/l10n/app_strings.dart')
txt = p.read_text(encoding='utf-8')

txt = txt.replace(
    "  List<String> get chartLabelsWeek    => languageCode=='sw'\n    ? ['Jtt','Jma','Jtn','Alh','Iju','Jum','Jmsi']\n    : ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];",
    "  List<String> get chartLabelsWeek    => languageCode=='sw'\n    ? ['Jumatatu','Jumanne','Jumatano','Alhamisi','Ijumaa','Jumamosi','Jumapili']\n    : ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];"
)

p.write_text(txt, encoding='utf-8')
print('done')