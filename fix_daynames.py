import pathlib
p = pathlib.Path('lib/shared/l10n/app_strings.dart')
t = p.read_text(encoding='utf-8')

# Fix Swahili weekday abbreviations to proper standard
old = "  List<String> get chartLabelsWeek    => languageCode=='sw'\n    ? ['Jtt','Jmo','Jtn','Alh','Ijm','Jum','Jps']\n    : ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];"
new = "  List<String> get chartLabelsWeek    => languageCode=='sw'\n    ? ['Jtt','Jma','Jtn','Alh','Iju','Jum','Jmsi']\n    : ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];\n\n  // Full day names\n  List<String> get weekdaysFull => languageCode=='sw'\n    ? ['Jumatatu','Jumanne','Jumatano','Alhamisi','Ijumaa','Jumamosi','Jumapili']\n    : ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];\n\n  // Full month names\n  List<String> get monthsFull => languageCode=='sw'\n    ? ['Januari','Februari','Machi','Aprili','Mei','Juni','Julai','Agosti','Septemba','Oktoba','Novemba','Desemba']\n    : ['January','February','March','April','May','June','July','August','September','October','November','December'];"
if old not in t: raise SystemExit('anchor not found')
t = t.replace(old, new, 1)
p.write_text(t, encoding='utf-8')
print('Day/month names updated.')