import pathlib

p = pathlib.Path('lib/shared/widgets/app_shell.dart')
text = p.read_text(encoding='utf-8')

old_import = "import '../../features/reports/presentation/reports_screen.dart';\nimport '../../features/analytics/presentation/analytics_screen.dart';"
new_import = "import '../../features/reports/presentation/reports_screen.dart';"
if old_import not in text:
    raise SystemExit("Import anchor not found - aborting, no changes made.")
text = text.replace(old_import, new_import, 1)

old_pages = """  static const _pages = [
    DashboardScreen(),
    ScoutingScreen(),
    MapsScreen(),
    ReportsScreen(),
    SettingsScreen(),
    AnalyticsScreen(),
  ];"""
new_pages = """  static const _pages = [
    DashboardScreen(),
    ScoutingScreen(),
    MapsScreen(),
    ReportsScreen(),
    SettingsScreen(),
  ];"""
if old_pages not in text:
    raise SystemExit("_pages anchor not found - aborting, no changes made.")
text = text.replace(old_pages, new_pages, 1)

old_nav = """    final all = [
      _NavItem(Icons.dashboard_rounded,  Icons.dashboard_outlined,  s.navDashboard, 0),
      _NavItem(Icons.grass_rounded,      Icons.grass_outlined,      s.navScouting,  1),
      _NavItem(Icons.map_rounded,        Icons.map_outlined,        s.navMaps,      2),
      _NavItem(Icons.bar_chart_rounded,  Icons.bar_chart_outlined,  s.navReports,   3),
      _NavItem(Icons.settings_rounded,   Icons.settings_outlined,   s.navSettings,  4),
      _NavItem(Icons.insights_rounded,   Icons.insights_outlined,   'Analytics',    5),
    ];"""
new_nav = """    final all = [
      _NavItem(Icons.dashboard_rounded,  Icons.dashboard_outlined,  s.navDashboard, 0),
      _NavItem(Icons.grass_rounded,      Icons.grass_outlined,      s.navScouting,  1),
      _NavItem(Icons.map_rounded,        Icons.map_outlined,        s.navMaps,      2),
      _NavItem(Icons.bar_chart_rounded,  Icons.bar_chart_outlined,  s.navReports,   3),
      _NavItem(Icons.settings_rounded,   Icons.settings_outlined,   s.navSettings,  4),
    ];"""
if old_nav not in text:
    raise SystemExit("Nav items anchor not found - aborting, no changes made.")
text = text.replace(old_nav, new_nav, 1)

p.write_text(text, encoding='utf-8')
print("app_shell.dart reverted: Analytics tab removed.")