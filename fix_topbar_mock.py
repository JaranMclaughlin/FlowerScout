import pathlib

p = pathlib.Path('lib/features/scouting/presentation/topbar_widgets.dart')
txt = p.read_text(encoding='utf-8', errors='replace')

# Fix duplicate label
txt = txt.replace(
    '                    label: s.feelsLike,\n                    label: s.feelsLike,',
    '                    label: s.feelsLike,'
)

# Revert mock notification strings - in field initializer, no ref available
txt = txt.replace("title: s.highSeverityAlert,", "title: 'High Severity Alert',")
txt = txt.replace("body: s.pestOutbreak,", "body: 'Potential pest outbreak detected',")
txt = txt.replace("title: s.inspectionDue,", "title: 'Inspection Due',")
txt = txt.replace("title: s.reportReady,", "title: 'Report Ready',")
txt = txt.replace("body: s.weeklySummaryReady,", "body: 'Weekly scouting summary is ready to view',")
txt = txt.replace("title: s.irrigationAlert,", "title: 'Irrigation Alert',")

p.write_text(txt, encoding='utf-8')
print('done')