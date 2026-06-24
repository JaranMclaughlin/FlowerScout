import pathlib
p = pathlib.Path('lib/features/analytics/presentation/analytics_screen.dart')
t = p.read_text(encoding='utf-8')

# 1. Remove duplicate AppStrings getter (s already defined in build via stringsProvider)
old1 = "  AppStrings get s => AppStrings.of(ref.read(localeProvider));\n\n  @override\n  Widget build(BuildContext context) {"
new1 = "  @override\n  Widget build(BuildContext context) {"
if old1 not in t: raise SystemExit('anchor 1 not found')
t = t.replace(old1, new1, 1)

# 2. Fix const Expanded containing s. references
old2 = """        Row(children: [
          const Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(s.findingsTrend, style: TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: _AP.ink)),
              SizedBox(height: 2),
              Text(s.findingsTrendSub, style: TextStyle(fontSize: 11, color: _AP.slate)),
            ]),
          ),"""
new2 = """        Row(children: [
          Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(s.findingsTrend, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: _AP.ink)),
              const SizedBox(height: 2),
              Text(s.findingsTrendSub, style: const TextStyle(fontSize: 11, color: _AP.slate)),
            ]),
          ),"""
if old2 not in t: raise SystemExit('anchor 2 not found')
t = t.replace(old2, new2, 1)

# 3. Fix _legend() - pass s as param and remove const
old3 = "  Widget _legend() => const Wrap(spacing: 16, children: [\n        _LegendDot(color: _AP.leaf, label: s.diseaseLegend),\n        _LegendDot(color: _AP.amber, label: s.pestsLegend),\n        _LegendDot(color: _AP.blue, label: s.waterLegend),\n      ]);"
new3 = "  Widget _legend(AppStrings s) => Wrap(spacing: 16, children: [\n        _LegendDot(color: _AP.leaf, label: s.diseaseLegend),\n        _LegendDot(color: _AP.amber, label: s.pestsLegend),\n        _LegendDot(color: _AP.blue, label: s.waterLegend),\n      ]);"
if old3 not in t: raise SystemExit('anchor 3 not found')
t = t.replace(old3, new3, 1)

# 4. Fix _legend() call site
t = t.replace('_legend(),', '_legend(s),')

# 5. Fix _chartType comparison - use label text not 'Bar'
old5 = "        SizedBox(height: 200, child: _chartType == 'Bar' ? _barChart(stats) : _lineChart(stats)),"
new5 = "        SizedBox(height: 200, child: _chartType == s.barLabel ? _barChart(stats) : _lineChart(stats)),"
if old5 not in t: raise SystemExit('anchor 5 not found')
t = t.replace(old5, new5, 1)

# 6. Add AppStrings import
if 'app_strings' not in t:
    old6 = "import '../../../shared/providers/locale_provider.dart';"
    new6 = "import '../../../shared/providers/locale_provider.dart';\nimport '../../../shared/l10n/app_strings.dart';"
    t = t.replace(old6, new6, 1)

p.write_text(t, encoding='utf-8')
print('analytics_screen.dart fixed.')