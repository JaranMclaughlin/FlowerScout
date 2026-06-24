import pathlib

# ── Fix analytics_screen.dart ─────────────────────────────────────────────────
p = pathlib.Path('lib/features/analytics/presentation/analytics_screen.dart')
t = p.read_text(encoding='utf-8')

# Add import
if 'locale_provider' not in t:
    old = "import 'package:flutter_riverpod/flutter_riverpod.dart';"
    new = "import 'package:flutter_riverpod/flutter_riverpod.dart';\nimport '../../../shared/providers/locale_provider.dart';\nimport '../../../shared/l10n/app_strings.dart';"
    t = t.replace(old, new, 1)

# Add s getter to state class
old = "  @override\n  Widget build(BuildContext context) {"
new = "  AppStrings get s => AppStrings.of(ref.read(localeProvider));\n\n  @override\n  Widget build(BuildContext context) {"
if old in t:
    t = t.replace(old, new, 1)

# Fix _segmented call site - add s argument
t = t.replace('_segmented(),', '_segmented(s),')

# Fix const Text issues with s.
t = t.replace('const Text(s.', 'Text(s.')
t = t.replace('const Text(s.analytics,', 'Text(s.analytics,')
t = t.replace('const Text(s.analyticsSubtitle,', 'Text(s.analyticsSubtitle,')
t = t.replace('const Text(s.findingsTrend,', 'Text(s.findingsTrend,')
t = t.replace('const Text(s.severityBreakdown,', 'Text(s.severityBreakdown,')
t = t.replace('const Text(s.topGreenhouses,', 'Text(s.topGreenhouses,')
t = t.replace('const Text(s.findingsByCategory,', 'Text(s.findingsByCategory,')

# Fix _LegendDot const issues
t = t.replace('const _LegendDot(color: _AP.leaf, label: s.diseaseLegend)', '_LegendDot(color: _AP.leaf, label: s.diseaseLegend)')
t = t.replace('const _LegendDot(color: _AP.amber, label: s.pestsLegend)', '_LegendDot(color: _AP.amber, label: s.pestsLegend)')
t = t.replace('const _LegendDot(color: _AP.blue, label: s.waterLegend)', '_LegendDot(color: _AP.blue, label: s.waterLegend)')

p.write_text(t, encoding='utf-8')
print('analytics_screen.dart fixed.')

# ── Fix reports_screen.dart ───────────────────────────────────────────────────
p2 = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
t2 = p2.read_text(encoding='utf-8')

# _buildTableRows needs s param
old2 = "Widget _buildTableRows(List<_Inspection> rows) {"
new2 = "Widget _buildTableRows(List<_Inspection> rows, AppStrings s) {"
if old2 in t2:
    t2 = t2.replace(old2, new2, 1)

# Fix call site of _buildTableRows - find and add s
t2 = t2.replace('_buildTableRows(displayRows),', '_buildTableRows(displayRows, s),')

p2.write_text(t2, encoding='utf-8')
print('reports_screen.dart fixed.')

# ── Fix settings_screen.dart const issue ─────────────────────────────────────
p3 = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
t3 = p3.read_text(encoding='utf-8')
t3 = t3.replace('const _settingRow(', '_settingRow(')
t3 = t3.replace('const _toggleRow(', '_toggleRow(')
p3.write_text(t3, encoding='utf-8')
print('settings_screen.dart fixed.')