import pathlib

p = pathlib.Path('lib/features/analytics/presentation/analytics_screen.dart')
p.parent.mkdir(parents=True, exist_ok=True)

content = """import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../shared/providers/farm_providers.dart';
import '../../../shared/providers/farm_repository.dart';
import '../../../shared/providers/analytics_data.dart';

class _AP {
  static const bg       = Color(0xFFF5F6F8);
  static const surface  = Color(0xFFFFFFFF);
  static const border   = Color(0xFFE8ECE8);
  static const ink      = Color(0xFF0F1F12);
  static const graphite = Color(0xFF3D4F42);
  static const slate    = Color(0xFF7A8C7E);
  static const forest   = Color(0xFF1B4332);
  static const leaf     = Color(0xFF40916C);
  static const mist     = Color(0xFFD8F3DC);
  static const red      = Color(0xFFB53030);
  static const redBg    = Color(0xFFFDF0F0);
  static const amber    = Color(0xFF9A5C00);
  static const amberBg  = Color(0xFFFFF8ED);
  static const blue     = Color(0xFF1565C0);
  static const divider  = Color(0xFFEDF1ED);
}

class AnalyticsScreen extends ConsumerStatefulWidget {
  const AnalyticsScreen({super.key});
  @override
  ConsumerState<AnalyticsScreen> createState() => _AnalyticsScreenState();
}

class _AnalyticsScreenState extends ConsumerState<AnalyticsScreen> {
  String _period = '7days';
  String? _farmId;
  String _chartType = 'Bar';

  BoxDecoration _card() => BoxDecoration(
        color: _AP.surface,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: _AP.border),
        boxShadow: [
          BoxShadow(color: Colors.black.withValues(alpha: 0.03), blurRadius: 8, offset: const Offset(0, 2)),
        ],
      );

  @override
  Widget build(BuildContext context) {
    final farmsAsync = ref.watch(farmsProvider);
    return Container(
      color: _AP.bg,
      child: farmsAsync.when(
        loading: () => const Center(child: CircularProgressIndicator(color: _AP.leaf)),
        error: (e, _) => Center(child: Text('Error: \$e')),
        data: (farms) {
          final filter = AnalyticsFilter(period: _period, farmId: _farmId);
          final statsAsync = ref.watch(reportStatsProvider(filter));
          return RefreshIndicator(
            color: _AP.leaf,
            onRefresh: () async => ref.invalidate(reportStatsProvider(filter)),
            child: SingleChildScrollView(
              physics: const AlwaysScrollableScrollPhysics(),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _buildHeader(farms),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 24),
                    child: statsAsync.when(
                      loading: () => _buildSkeleton(),
                      error: (e, _) => _buildError(e.toString()),
                      data: (stats) => Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const SizedBox(height: 8),
                          _buildKpiRow(stats),
                          const SizedBox(height: 24),
                          _buildChartCard(stats),
                          const SizedBox(height: 24),
                          Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Expanded(flex: 5, child: _buildSeverityCard(stats)),
                              const SizedBox(width: 16),
                              Expanded(flex: 5, child: _buildTopGhCard(stats)),
                            ],
                          ),
                          const SizedBox(height: 24),
                          _buildCategoryCard(stats),
                          const SizedBox(height: 40),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  // ── Header ──────────────────────────────────────────────
  Widget _buildHeader(List<FarmModel> farms) {
    final farmItems = <String, String?>{'All Farms': null};
    for (final f in farms) {
      farmItems[f.name] = f.id;
    }
    final periodItems = {
      'Today': 'today', 'Last 7 Days': '7days',
      'Last 30 Days': '30days', 'Last 3 Months': '3months',
    };

    return Container(
      color: _AP.surface,
      padding: const EdgeInsets.fromLTRB(24, 24, 24, 20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Analytics',
              style: TextStyle(fontSize: 26, fontWeight: FontWeight.w800,
                  color: _AP.ink, letterSpacing: -0.5)),
          const SizedBox(height: 4),
          const Text('Farm-wide performance and trends',
              style: TextStyle(fontSize: 13, color: _AP.slate)),
          const SizedBox(height: 20),
          const Divider(height: 1, color: _AP.divider),
          const SizedBox(height: 16),
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(
              children: [
                _filterPill(
                  'Period',
                  periodItems.entries
                      .firstWhere((e) => e.value == _period,
                          orElse: () => periodItems.entries.first)
                      .key,
                  periodItems.keys.toList(),
                  (v) => setState(() => _period = periodItems[v]!),
                ),
                const SizedBox(width: 10),
                _filterPill(
                  'Farm',
                  farmItems.entries
                      .firstWhere((e) => e.value == _farmId,
                          orElse: () => farmItems.entries.first)
                      .key,
                  farmItems.keys.toList(),
                  (v) => setState(() => _farmId = farmItems[v]),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _filterPill(String label, String value, List<String> items,
          ValueChanged<String?> onChanged) =>
      Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
        decoration: BoxDecoration(
          color: _AP.bg,
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: _AP.border),
        ),
        child: DropdownButtonHideUnderline(
          child: DropdownButton<String>(
            value: items.contains(value) ? value : items.first,
            isDense: true,
            style: const TextStyle(fontSize: 12, color: _AP.ink, fontWeight: FontWeight.w500),
            icon: const Icon(Icons.keyboard_arrow_down_rounded, size: 16, color: _AP.slate),
            items: items.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
            onChanged: onChanged,
          ),
        ),
      );

  // ── KPI row ──────────────────────────────────────────────
  Widget _buildKpiRow(ReportStats stats) {
    final kpis = [
      ('Inspections', stats.total, Icons.assignment_outlined, _AP.forest, _AP.mist),
      ('Disease', stats.disease, Icons.coronavirus_outlined, _AP.red, _AP.redBg),
      ('Pests', stats.pest, Icons.bug_report_outlined, _AP.amber, _AP.amberBg),
      ('Critical', stats.critical, Icons.warning_amber_rounded,
          const Color(0xFF7A1F1F), const Color(0xFFFDE8E8)),
    ];
    return LayoutBuilder(builder: (_, con) {
      final cross = con.maxWidth > 600 ? 4 : 2;
      return GridView.count(
        crossAxisCount: cross,
        shrinkWrap: true,
        physics: const NeverScrollableScrollPhysics(),
        crossAxisSpacing: 12,
        mainAxisSpacing: 12,
        childAspectRatio: cross == 4 ? 1.6 : 1.8,
        children: kpis.map((k) => _kpiCard(k.\$1, k.\$2, k.\$3, k.\$4, k.\$5)).toList(),
      );
    });
  }

  Widget _kpiCard(String label, int value, IconData icon, Color color, Color bg) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: _AP.surface,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: _AP.border),
        boxShadow: [BoxShadow(color: Colors.black.withValues(alpha: 0.03), blurRadius: 6, offset: const Offset(0, 2))],
      ),
      child: Row(children: [
        Container(
          width: 40, height: 40,
          decoration: BoxDecoration(color: bg, borderRadius: BorderRadius.circular(10)),
          child: Icon(icon, color: color, size: 20),
        ),
        const SizedBox(width: 12),
        Column(crossAxisAlignment: CrossAxisAlignment.start, mainAxisSize: MainAxisSize.min, children: [
          Text('\$value', style: const TextStyle(fontSize: 24, fontWeight: FontWeight.w800, color: _AP.ink, height: 1)),
          const SizedBox(height: 2),
          Text(label, style: const TextStyle(fontSize: 11, color: _AP.slate, fontWeight: FontWeight.w500)),
        ]),
      ]),
    );
  }

  // ── Trend chart ──────────────────────────────────────────
  Widget _buildChartCard(ReportStats stats) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: _card(),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          const Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('Findings Trend', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: _AP.ink)),
              SizedBox(height: 2),
              Text('By category over period', style: TextStyle(fontSize: 11, color: _AP.slate)),
            ]),
          ),
          _segmented(),
        ]),
        const SizedBox(height: 6),
        _legend(),
        const SizedBox(height: 16),
        SizedBox(height: 200, child: _chartType == 'Bar' ? _barChart(stats) : _lineChart(stats)),
      ]),
    );
  }

  Widget _segmented() => Row(children: ['Bar', 'Line'].map((t) {
        final active = _chartType == t;
        return GestureDetector(
          onTap: () => setState(() => _chartType = t),
          child: Container(
            margin: const EdgeInsets.only(left: 4),
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
            decoration: BoxDecoration(
              color: active ? _AP.forest : Colors.transparent,
              borderRadius: BorderRadius.circular(6),
              border: Border.all(color: active ? _AP.forest : _AP.border),
            ),
            child: Text(t, style: TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: active ? Colors.white : _AP.slate)),
          ),
        );
      }).toList());

  Widget _legend() => const Wrap(spacing: 16, children: [
        _LegendDot(color: _AP.leaf, label: 'Disease'),
        _LegendDot(color: _AP.amber, label: 'Pests'),
        _LegendDot(color: _AP.blue, label: 'Water'),
      ]);

  Widget _barChart(ReportStats d) {
    final labels = d.chartLabels;
    final maxY = [...d.trendDisease, ...d.trendPest, ...d.trendWater].fold(0.0, (a, b) => a > b ? a : b) * 1.3;
    return BarChart(BarChartData(
      alignment: BarChartAlignment.spaceAround,
      maxY: maxY < 1 ? 5 : maxY,
      barTouchData: BarTouchData(enabled: false),
      gridData: FlGridData(drawVerticalLine: false, getDrawingHorizontalLine: (_) => FlLine(color: _AP.divider, strokeWidth: 1)),
      borderData: FlBorderData(show: false),
      titlesData: FlTitlesData(
        leftTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        bottomTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, reservedSize: 24, getTitlesWidget: (v, _) {
          final i = v.toInt();
          if (i < 0 || i >= labels.length) return const SizedBox();
          return Padding(padding: const EdgeInsets.only(top: 4), child: Text(labels[i], style: const TextStyle(fontSize: 9, color: _AP.slate)));
        })),
      ),
      barGroups: List.generate(labels.length, (i) => BarChartGroupData(x: i, barRods: [
            BarChartRodData(toY: d.trendDisease[i], color: _AP.leaf, width: 4, borderRadius: BorderRadius.circular(3)),
            BarChartRodData(toY: d.trendPest[i], color: _AP.amber, width: 4, borderRadius: BorderRadius.circular(3)),
            BarChartRodData(toY: d.trendWater[i], color: _AP.blue, width: 4, borderRadius: BorderRadius.circular(3)),
          ])),
    ));
  }

  Widget _lineChart(ReportStats d) {
    final labels = d.chartLabels;
    final maxY = [...d.trendDisease, ...d.trendPest, ...d.trendWater].fold(0.0, (a, b) => a > b ? a : b) * 1.3;
    LineChartBarData series(List<double> v, Color c) => LineChartBarData(
          spots: v.asMap().entries.map((e) => FlSpot(e.key.toDouble(), e.value)).toList(),
          isCurved: true, color: c, barWidth: 2,
          dotData: FlDotData(show: true, getDotPainter: (s, _, __, ___) => FlDotCirclePainter(radius: 3, color: c, strokeWidth: 0, strokeColor: c)),
          belowBarData: BarAreaData(show: true, color: c.withValues(alpha: 0.06)),
        );
    return LineChart(LineChartData(
      minY: 0, maxY: maxY < 1 ? 5 : maxY,
      lineTouchData: const LineTouchData(enabled: false),
      gridData: FlGridData(drawVerticalLine: false, getDrawingHorizontalLine: (_) => FlLine(color: _AP.divider, strokeWidth: 1)),
      borderData: FlBorderData(show: false),
      titlesData: FlTitlesData(
        leftTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        bottomTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, reservedSize: 24, getTitlesWidget: (v, _) {
          final i = v.toInt();
          if (i < 0 || i >= labels.length) return const SizedBox();
          return Padding(padding: const EdgeInsets.only(top: 4), child: Text(labels[i], style: const TextStyle(fontSize: 9, color: _AP.slate)));
        })),
      ),
      lineBarsData: [series(d.trendDisease, _AP.leaf), series(d.trendPest, _AP.amber), series(d.trendWater, _AP.blue)],
    ));
  }

  // ── Severity donut ──────────────────────────────────────
  Widget _buildSeverityCard(ReportStats stats) {
    final sev = stats.bySeverity;
    final total = sev.values.fold(0, (a, b) => a + b);
    double pct(String k) => total == 0 ? 0.0 : (sev[k] ?? 0) / total * 100;
    final sevs = [
      ('Critical', pct('Critical'), const Color(0xFF7A1F1F)),
      ('High', pct('High'), _AP.red),
      ('Medium', pct('Medium'), _AP.amber),
      ('Low', pct('Low'), _AP.leaf),
    ];
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: _card(),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Text('Severity Breakdown', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: _AP.ink)),
        const SizedBox(height: 16),
        if (total == 0)
          const Center(child: Padding(padding: EdgeInsets.all(20), child: Text('No data', style: TextStyle(color: _AP.slate, fontSize: 13))))
        else
          Row(children: [
            SizedBox(width: 100, height: 100, child: PieChart(PieChartData(
              sections: sevs.map((s) => PieChartSectionData(value: s.\$2, color: s.\$3, title: '', radius: 38)).toList(),
              sectionsSpace: 2, centerSpaceRadius: 24, borderData: FlBorderData(show: false),
            ))),
            const SizedBox(width: 16),
            Expanded(child: Column(children: sevs.map((item) => Padding(
              padding: const EdgeInsets.symmetric(vertical: 4),
              child: Row(children: [
                Container(width: 8, height: 8, decoration: BoxDecoration(color: item.\$3, shape: BoxShape.circle)),
                const SizedBox(width: 8),
                Expanded(child: Text(item.\$1, style: const TextStyle(fontSize: 12, color: _AP.graphite))),
                Text('\${item.\$2.toInt()}%', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w700, color: item.\$3)),
              ]),
            )).toList())),
          ]),
      ]),
    );
  }

  // ── Top greenhouses ─────────────────────────────────────
  Widget _buildTopGhCard(ReportStats stats) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: _card(),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Text('Top Greenhouses', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: _AP.ink)),
        const SizedBox(height: 16),
        if (stats.topGreenhouses.isEmpty)
          const Center(child: Padding(padding: EdgeInsets.all(20), child: Text('No data', style: TextStyle(color: _AP.slate, fontSize: 13))))
        else
          ...stats.topGreenhouses.map((g) => Padding(
                padding: const EdgeInsets.symmetric(vertical: 6),
                child: Row(children: [
                  Container(
                    width: 28, height: 28,
                    decoration: BoxDecoration(color: _AP.mist, borderRadius: BorderRadius.circular(8)),
                    child: Center(child: Text(g.gh, style: const TextStyle(fontSize: 10, fontWeight: FontWeight.w700, color: _AP.forest))),
                  ),
                  const SizedBox(width: 10),
                  Expanded(child: Text(g.topIssue, style: const TextStyle(fontSize: 12, color: _AP.graphite), overflow: TextOverflow.ellipsis)),
                  Text('\${g.findings}', style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: _AP.ink)),
                ]),
              )),
      ]),
    );
  }

  // ── Category breakdown ──────────────────────────────────
  Widget _buildCategoryCard(ReportStats stats) {
    final entries = stats.byCategory.entries.toList()..sort((a, b) => b.value.compareTo(a.value));
    final maxVal = entries.isEmpty ? 1 : entries.first.value;
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: _card(),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Text('Findings by Category', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: _AP.ink)),
        const SizedBox(height: 16),
        if (entries.isEmpty)
          const Center(child: Padding(padding: EdgeInsets.all(20), child: Text('No data', style: TextStyle(color: _AP.slate, fontSize: 13))))
        else
          ...entries.map((e) => Padding(
                padding: const EdgeInsets.symmetric(vertical: 6),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Row(children: [
                    Expanded(child: Text(e.key, style: const TextStyle(fontSize: 12, color: _AP.graphite))),
                    Text('\${e.value}', style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w700, color: _AP.ink)),
                  ]),
                  const SizedBox(height: 4),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(4),
                    child: LinearProgressIndicator(
                      value: maxVal == 0 ? 0 : e.value / maxVal,
                      minHeight: 6,
                      backgroundColor: _AP.divider,
                      valueColor: const AlwaysStoppedAnimation(_AP.leaf),
                    ),
                  ),
                ]),
              )),
      ]),
    );
  }

  Widget _buildSkeleton() => const Padding(
        padding: EdgeInsets.symmetric(vertical: 40),
        child: Center(child: CircularProgressIndicator(color: _AP.leaf)),
      );

  Widget _buildError(String message) => Padding(
        padding: const EdgeInsets.symmetric(vertical: 40),
        child: Center(child: Text('Error: \$message', style: const TextStyle(color: _AP.red))),
      );
}

class _LegendDot extends StatelessWidget {
  final Color color;
  final String label;
  const _LegendDot({required this.color, required this.label});
  @override
  Widget build(BuildContext context) {
    return Row(mainAxisSize: MainAxisSize.min, children: [
      Container(width: 8, height: 8, decoration: BoxDecoration(color: color, shape: BoxShape.circle)),
      const SizedBox(width: 4),
      Text(label, style: const TextStyle(fontSize: 11, color: _AP.slate)),
    ]);
  }
}
"""

p.write_text(content, encoding='utf-8')
print(f"Created {p} ({len(content)} chars)")