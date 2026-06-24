import pathlib
p = pathlib.Path('lib/features/dashboard/presentation/dashboard_screen.dart')
t = p.read_text(encoding='utf-8')

# Fix constructors missing s
t = t.replace(
    "  const _ReportSummaryCard({required this.stats, required this.ref});",
    "  const _ReportSummaryCard({required this.stats, required this.ref, required this.s});")
t = t.replace(
    "  const _HealthCard({required this.stats});",
    "  const _HealthCard({required this.stats, required this.s});")
t = t.replace(
    "  const _StatsGrid({required this.stats});",
    "  const _StatsGrid({required this.stats, required this.s});")
t = t.replace(
    "  const _FarmTile({required this.farm});",
    "  const _FarmTile({required this.farm, required this.s});")

# Fix _QuickActions - add s via stringsProvider
old_qa = "  Widget build(BuildContext context, WidgetRef ref) {\n    final actions = [\n      (Icons.add_circle_outline_rounded, s.newReport, 1),"
new_qa = "  Widget build(BuildContext context, WidgetRef ref) {\n    final s = ref.watch(stringsProvider);\n    final actions = [\n      (Icons.add_circle_outline_rounded, s.newReport, 1),"
if old_qa in t: t = t.replace(old_qa, new_qa, 1)
else: print('MISSED _QuickActions build')

# Fix remaining hardcoded condition labels in _HealthCard
t = t.replace("        : score >= 60 ? 'Good condition'", "        : score >= 60 ? s.goodCond")
t = t.replace("        : score >= 40 ? 'Needs attention'", "        : score >= 40 ? s.needsAttention")
t = t.replace("        : 'Critical \u2014 action required';", "        : s.criticalAction;")

# Fix Settings hardcoded in quick actions
t = t.replace("(Icons.settings_outlined,          'Settings',   4),",
              "(Icons.settings_outlined,          s.settings,   4),")

# Now fix all call sites to pass s:
# Find _ReportSummaryCard, _HealthCard, _StatsGrid, _FarmTile instantiations
t = t.replace("_ReportSummaryCard(stats: stats, ref: ref)",
              "_ReportSummaryCard(stats: stats, ref: ref, s: s)")
t = t.replace("_HealthCard(stats: stats)",
              "_HealthCard(stats: stats, s: s)")
t = t.replace("_StatsGrid(stats: stats)",
              "_StatsGrid(stats: stats, s: s)")
# _FarmTile is likely in a map - replace all
t = t.replace("_FarmTile(farm: farm)",  "_FarmTile(farm: farm, s: s)")
t = t.replace("_FarmTile(farm: f)",     "_FarmTile(farm: f, s: s)")
# _EmptyFarmsCard already has required this.s - find call sites
t = t.replace("const _EmptyFarmsCard()", "_EmptyFarmsCard(s: s)")

p.write_text(t, encoding='utf-8')
print('Dashboard constructors fixed.')