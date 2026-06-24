import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
txt = p.read_text(encoding='utf-8')

txt = txt.replace(
    "factory _ReportStats.fromInspections(List<_Inspection> ins, String period) {",
    "factory _ReportStats.fromInspections(List<_Inspection> ins, String period, {String lang='en'}) {"
)

p.write_text(txt, encoding='utf-8')
print('done')