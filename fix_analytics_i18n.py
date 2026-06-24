import pathlib

p = pathlib.Path('lib/features/analytics/presentation/analytics_screen.dart')
t = p.read_text(encoding='utf-8')

# Check if stringsProvider is already imported/used
has_strings = 'stringsProvider' in t or 'AppStrings' in t

replacements = [
    # Header
    ("const Text('Analytics',", "Text(s.analytics,"),
    ("const Text('Farm-wide performance and trends',", "Text(s.analyticsSubtitle,"),
    ("'All Farms': null", "s.allFarms: null"),
    ("'Today': 'today', 'Last 7 Days': '7days',", "s.today: 'today', s.last7Days: '7days',"),
    ("'Last 30 Days': '30days', 'Last 3 Months': '3months',", "s.last30Days: '30days', s.last3Months: '3months',"),
    ("'Period',", "s.period,"),
    ("'Farm',", "s.farmFilter,"),
    # Trend card
    ("Text('Findings Trend', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: _AP.ink)),", 
     "Text(s.findingsTrend, style: TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: _AP.ink)),"),
    ("Text('By category over period', style: TextStyle(fontSize: 11, color: _AP.slate)),",
     "Text(s.findingsTrendSub, style: TextStyle(fontSize: 11, color: _AP.slate)),"),
    # Segmented bar/line
    ("Widget _segmented() => Row(children: ['Bar', 'Line'].map((t) {",
     "Widget _segmented(AppStrings s) => Row(children: [s.barLabel, s.lineLabel].map((t) {"),
    ("String _chartType = 'Bar';", "String _chartType = 'bar';"),
    # Legends
    ("_LegendDot(color: _AP.leaf, label: 'Disease'),", "_LegendDot(color: _AP.leaf, label: s.diseaseLegend),"),
    ("_LegendDot(color: _AP.amber, label: 'Pests'),", "_LegendDot(color: _AP.amber, label: s.pestsLegend),"),
    ("_LegendDot(color: _AP.blue, label: 'Water'),", "_LegendDot(color: _AP.blue, label: s.waterLegend),"),
    # Severity
    ("const Text('Severity Breakdown', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: _AP.ink)),",
     "Text(s.severityBreakdown, style: TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: _AP.ink)),"),
    ("('Critical', pct('Critical'), const Color(0xFF7A1F1F)),", "(s.criticalLabel, pct('Critical'), const Color(0xFF7A1F1F)),"),
    ("('High', pct('High'), _AP.red),", "(s.highLabel, pct('High'), _AP.red),"),
    ("('Medium', pct('Medium'), _AP.amber),", "(s.mediumLabel, pct('Medium'), _AP.amber),"),
    # Top GH
    ("const Text('Top Greenhouses', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: _AP.ink)),",
     "Text(s.topGreenhouses, style: TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: _AP.ink)),"),
    # Category
    ("const Text('Findings by Category', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: _AP.ink)),",
     "Text(s.findingsByCategory, style: TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: _AP.ink)),"),
]

failed = []
for old, new in replacements:
    if old in t:
        t = t.replace(old, new, 1)
    else:
        failed.append(old[:60])

# Add stringsProvider watch if not present
if 'stringsProvider' not in t:
    old_build = "Widget build(BuildContext context) {"
    new_build = "Widget build(BuildContext context) {\n    final s = ref.watch(stringsProvider);"
    if old_build in t:
        t = t.replace(old_build, new_build, 1)

# Add import if missing
if "locale_provider" not in t:
    old_imp = "import 'package:flutter_riverpod/flutter_riverpod.dart';"
    new_imp = "import 'package:flutter_riverpod/flutter_riverpod.dart';\nimport '../../../shared/providers/locale_provider.dart';"
    if old_imp in t:
        t = t.replace(old_imp, new_imp, 1)

p.write_text(t, encoding='utf-8')
print('analytics_screen.dart updated.')
if failed: print('MISSED:', failed)