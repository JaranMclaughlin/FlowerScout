import pathlib

# Fix analytics_screen No data
p = pathlib.Path('lib/features/analytics/presentation/analytics_screen.dart')
txt = p.read_text(encoding='utf-8')
txt = txt.replace("'No data'", "s.noData")
p.write_text(txt, encoding='utf-8')
print('analytics done')

# Fix reports No data
p2 = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
txt2 = p2.read_text(encoding='utf-8')
txt2 = txt2.replace("'No data'", "s.noData")
p2.write_text(txt2, encoding='utf-8')
print('reports done')

# Fix location_permission_screen
p3 = pathlib.Path('lib/features/auth/presentation/location_permission_screen.dart')
txt3 = p3.read_text(encoding='utf-8')
txt3 = txt3.replace("'Location blocked'", "s.locationBlocked")
txt3 = txt3.replace("'Continue anyway'", "s.continueAnyway")
txt3 = txt3.replace("'Open settings'", "s.openAppSettings")
txt3 = txt3.replace("'Allow location access'", "s.allowLocationAccess")
txt3 = txt3.replace("'Records your walking trail across the farm'", "s.recordsTrail")
txt3 = txt3.replace("'Tracks which farm zones are covered or missed'", "s.tracksZones")
txt3 = txt3.replace("'Powers distance and coverage analytics'", "s.powersAnalytics")
txt3 = txt3.replace("'Allow while using app'", "s.allowWhileUsing")
txt3 = txt3.replace("'Not now'", "s.notNow")
p3.write_text(txt3, encoding='utf-8')
print('location done')

# Fix topbar_widgets
p4 = pathlib.Path('lib/features/scouting/presentation/topbar_widgets.dart')
txt4 = p4.read_text(encoding='utf-8')
txt4 = txt4.replace("'Just now'", "s.justNow")
txt4 = txt4.replace("'Partly Cloudy'", "s.partlyCloudy")
txt4 = txt4.replace("'Feels like'", "s.feelsLike")
txt4 = txt4.replace("'High Severity Alert'", "s.highSeverityAlert")
txt4 = txt4.replace("'Potential pest outbreak detected'", "s.pestOutbreak")
txt4 = txt4.replace("'Inspection Due'", "s.inspectionDue")
txt4 = txt4.replace("'Report Ready'", "s.reportReady")
txt4 = txt4.replace("'Weekly scouting summary is ready to view'", "s.weeklySummaryReady")
txt4 = txt4.replace("'Irrigation Alert'", "s.irrigationAlert")
txt4 = txt4.replace("'Mark all read'", "s.markAllRead")
txt4 = txt4.replace("'All caught up!'", "s.allCaughtUp")
txt4 = txt4.replace("'No new notifications'", "s.noNewNotifications")
p4.write_text(txt4, encoding='utf-8')
print('topbar done')

# Fix chartLabels30Days to use full names
p5 = pathlib.Path('lib/shared/l10n/app_strings.dart')
txt5 = p5.read_text(encoding='utf-8')
txt5 = txt5.replace(
    "  List<String> get chartLabels30Days  => ['W1','W2','W3','W4','W5'];",
    "  List<String> get chartLabels30Days  => languageCode=='sw'\n    ? ['Wiki 1','Wiki 2','Wiki 3','Wiki 4','Wiki 5']\n    : ['Week 1','Week 2','Week 3','Week 4','Week 5'];"
)
p5.write_text(txt5, encoding='utf-8')
print('chart labels done')