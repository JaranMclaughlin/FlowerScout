import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../shared/providers/locale_provider.dart';
import '../../../shared/l10n/app_strings.dart';
import '../../../shared/providers/farm_providers.dart';
import '../../../shared/providers/farm_repository.dart';
import '../../../shared/providers/analytics_data.dart';
import '../../../shared/theme/app_colors.dart';

class AnalyticsScreen extends ConsumerStatefulWidget {
  const AnalyticsScreen({super.key});
  @override
  ConsumerState<AnalyticsScreen> createState() => _AnalyticsScreenState();
}

class _AnalyticsScreenState extends ConsumerState<AnalyticsScreen> {
  String _period = '7days';
  String? _farmId;
  // Use a stable enum-like flag instead of a localized string
  bool _showBar = true;

  BoxDecoration _card() => BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.border),
        boxShadow: [BoxShadow(color: Colors.black.withValues(alpha: 0.03), blurRadius: 8, offset: const Offset(0, 2))],
      );

  AppStrings get s => AppStrings.of(ref.watch(localeProvider));

  @override
  Widget build(BuildContext context) {
    ref.watch(stringsProvider);
    final farmsAsync = ref.watch(farmsProvider);
    return Container(
      color: AppColors.background,
      child: farmsAsync.when(
        loading: () => const Center(child: CircularProgressIndicator(color: AppColors.leaf)),
        error: (e, _) => Center(child: Text('Error: $e')),
        data: (farms) {
          final filter = AnalyticsFilter(period: _period, farmId: _farmId);
          final statsAsync = ref.watch(reportStatsProvider(filter));
          return RefreshIndicator(
            color: AppColors.leaf,
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

  Widget _buildHeader(List<FarmModel> farms) {
    final farmItems = <String, String?>{s.allFarms: null};
    for (final f in farms) {
      farmItems[f.name] = f.id;
    }
    final periodItems = {
      s.today: 'today', s.last7Days: '7days',
      s.last30Days: '30days', s.last3Months: '3months',
    };
    return Container(
      color: AppColors.surface,
      padding: const EdgeInsets.fromLTRB(24, 24, 24, 20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(s.analytics, style: const TextStyle(fontSize: 26, fontWeight: FontWeight.w800, color: AppColors.ink, letterSpacing: -0.5)),
          const SizedBox(height: 4),
          Text(s.analyticsSubtitle, style: const TextStyle(fontSize: 13, color: AppColors.slate)),
          const SizedBox(height: 20),
          const Divider(height: 1, color: AppColors.divider),
          const SizedBox(height: 16),
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(children: [
              _filterPill(s.period,
                periodItems.entries.firstWhere((e) => e.value == _period, orElse: () => periodItems.entries.first).key,
                periodItems.keys.toList(), (v) => setState(() => _period = periodItems[v]!)),
              const SizedBox(width: 10),
              _filterPill(s.farmFilter,
                farmItems.entries.firstWhere((e) => e.value == _farmId, orElse: () => farmItems.entries.first).key,
                farmItems.keys.toList(), (v) => setState(() => _farmId = farmItems[v])),
            ]),
          ),
        ],
      ),
    );
  }

  Widget _filterPill(String label, String value, List<String> items, ValueChanged<String?> onChanged) =>
      Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
        decoration: BoxDecoration(color: AppColors.background, borderRadius: BorderRadius.circular(8), border: Border.all(color: AppColors.border)),
        child: DropdownButtonHideUnderline(
          child: DropdownButton<String>(
            value: items.contains(value) ? value : items.first,
            isDense: true,
            style: const TextStyle(fontSize: 12, color: AppColors.ink, fontWeight: FontWeight.w500),
            icon: const Icon(Icons.keyboard_arrow_down_rounded, size: 16, color: AppColors.slate),
            items: items.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
            onChanged: onChanged,
          ),
        ),
      );

  Widget _buildKpiRow(ReportStats stats) {
    final kpis = [
      ('Inspections', stats.total, Icons.assignment_outlined, AppColors.forest, AppColors.mist),
      ('Disease', stats.disease, Icons.coronavirus_outlined, AppColors.disease, const Color(0xFFFDF0F0)),
      ('Pests', stats.pest, Icons.bug_report_outlined, AppColors.pest, const Color(0xFFFFF8ED)),
      ('Critical', stats.critical, Icons.warning_amber_rounded, const Color(0xFF7A1F1F), const Color(0xFFFDE8E8)),
    ];
    return LayoutBuilder(builder: (_, con) {
      final cross = con.maxWidth > 600 ? 4 : 2;
      return GridView.count(
        crossAxisCount: cross, shrinkWrap: true,
        physics: const NeverScrollableScrollPhysics(),
        crossAxisSpacing: 12, mainAxisSpacing: 12,
        childAspectRatio: cross == 4 ? 1.6 : 1.8,
        children: kpis.map((k) => _kpiCard(k.$1, k.$2, k.$3, k.$4, k.$5)).toList(),
      );
    });
  }

  Widget _kpiCard(String label, int value, IconData icon, Color color, Color bg) =>
      Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: AppColors.surface, borderRadius: BorderRadius.circular(14),
          border: Border.all(color: AppColors.border),
          boxShadow: [BoxShadow(color: Colors.black.withValues(alpha: 0.03), blurRadius: 6, offset: const Offset(0, 2))],
        ),
        child: Row(children: [
          Container(width: 40, height: 40, decoration: BoxDecoration(color: bg, borderRadius: BorderRadius.circular(10)),
            child: Icon(icon, color: color, size: 20)),
          const SizedBox(width: 12),
          Column(crossAxisAlignment: CrossAxisAlignment.start, mainAxisSize: MainAxisSize.min, children: [
            Text('$value', style: const TextStyle(fontSize: 24, fontWeight: FontWeight.w800, color: AppColors.ink, height: 1)),
            const SizedBox(height: 2),
            Text(label, style: const TextStyle(fontSize: 11, color: AppColors.slate, fontWeight: FontWeight.w500)),
          ]),
        ]),
      );

  Widget _buildChartCard(ReportStats stats) =>
      Container(
        padding: const EdgeInsets.all(20),
        decoration: _card(),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Row(children: [
            Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(s.findingsTrend, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: AppColors.ink)),
              const SizedBox(height: 2),
              Text(s.findingsTrendSub, style: const TextStyle(fontSize: 11, color: AppColors.slate)),
            ])),
            _segmented(),
          ]),
          const SizedBox(height: 6),
          _legend(),
          const SizedBox(height: 16),
          SizedBox(height: 200, child: _showBar ? _barChart(stats) : _lineChart(stats)),
        ]),
      );

  Widget _segmented() => Row(children: [
    _segBtn(s.barLabel, true),
    _segBtn(s.lineLabel, false),
  ]);

  Widget _segBtn(String label, bool isBar) {
    final active = _showBar == isBar;
    return GestureDetector(
      onTap: () => setState(() => _showBar = isBar),
      child: Container(
        margin: const EdgeInsets.only(left: 4),
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
        decoration: BoxDecoration(
          color: active ? AppColors.forest : Colors.transparent,
          borderRadius: BorderRadius.circular(6),
          border: Border.all(color: active ? AppColors.forest : AppColors.border),
        ),
        child: Text(label, style: TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: active ? Colors.white : AppColors.slate)),
      ),
    );
  }

  Widget _legend() => Wrap(spacing: 16, children: [
    _LegendDot(color: AppColors.leaf, label: s.diseaseLegend),
    _LegendDot(color: AppColors.warning, label: s.pestsLegend),
    _LegendDot(color: AppColors.info, label: s.waterLegend),
  ]);

  Widget _barChart(ReportStats d) {
    final labels = d.chartLabels.length == 7 ? AppStrings.of(ref.watch(localeProvider)).chartLabelsWeekShort : d.chartLabels;
    final maxY = [...d.trendDisease, ...d.trendPest, ...d.trendWater].fold(0.0, (a, b) => a > b ? a : b) * 1.3;
    return BarChart(BarChartData(
      alignment: BarChartAlignment.spaceAround,
      maxY: maxY < 1 ? 5 : maxY,
      barTouchData: BarTouchData(enabled: false),
      gridData: FlGridData(drawVerticalLine: false, getDrawingHorizontalLine: (_) => const FlLine(color: AppColors.divider, strokeWidth: 1)),
      borderData: FlBorderData(show: false),
      titlesData: FlTitlesData(
        leftTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        bottomTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, reservedSize: 24, getTitlesWidget: (v, _) {
          final i = v.toInt();
          if (i < 0 || i >= labels.length) return const SizedBox();
          return Padding(padding: const EdgeInsets.only(top: 4), child: Text(labels[i], style: const TextStyle(fontSize: 9, color: AppColors.slate)));
        })),
      ),
      barGroups: List.generate(labels.length, (i) => BarChartGroupData(x: i, barRods: [
        BarChartRodData(toY: d.trendDisease[i], color: AppColors.leaf, width: 4, borderRadius: BorderRadius.circular(3)),
        BarChartRodData(toY: d.trendPest[i], color: AppColors.warning, width: 4, borderRadius: BorderRadius.circular(3)),
        BarChartRodData(toY: d.trendWater[i], color: AppColors.info, width: 4, borderRadius: BorderRadius.circular(3)),
      ])),
    ));
  }

  Widget _lineChart(ReportStats d) {
    final labels = d.chartLabels.length == 7 ? AppStrings.of(ref.watch(localeProvider)).chartLabelsWeekShort : d.chartLabels;
    final maxY = [...d.trendDisease, ...d.trendPest, ...d.trendWater].fold(0.0, (a, b) => a > b ? a : b) * 1.3;
    LineChartBarData series(List<double> v, Color c) => LineChartBarData(
      spots: v.asMap().entries.map((e) => FlSpot(e.key.toDouble(), e.value)).toList(),
      isCurved: true, color: c, barWidth: 2,
      dotData: FlDotData(show: true, getDotPainter: (s, _, _, _) => FlDotCirclePainter(radius: 3, color: c, strokeWidth: 0, strokeColor: c)),
      belowBarData: BarAreaData(show: true, color: c.withValues(alpha: 0.06)),
    );
    return LineChart(LineChartData(
      minY: 0, maxY: maxY < 1 ? 5 : maxY,
      lineTouchData: const LineTouchData(enabled: false),
      gridData: FlGridData(drawVerticalLine: false, getDrawingHorizontalLine: (_) => const FlLine(color: AppColors.divider, strokeWidth: 1)),
      borderData: FlBorderData(show: false),
      titlesData: FlTitlesData(
        leftTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        bottomTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, reservedSize: 24, getTitlesWidget: (v, _) {
          final i = v.toInt();
          if (i < 0 || i >= labels.length) return const SizedBox();
          return Padding(padding: const EdgeInsets.only(top: 4), child: Text(labels[i], style: const TextStyle(fontSize: 9, color: AppColors.slate)));
        })),
      ),
      lineBarsData: [series(d.trendDisease, AppColors.leaf), series(d.trendPest, AppColors.warning), series(d.trendWater, AppColors.info)],
    ));
  }

  Widget _buildSeverityCard(ReportStats stats) {
    final sev = stats.bySeverity;
    final total = sev.values.fold(0, (a, b) => a + b);
    double pct(String k) => total == 0 ? 0.0 : (sev[k] ?? 0) / total * 100;
    final sevs = [
      (s.criticalLabel, pct('Critical'), const Color(0xFF7A1F1F)),
      (s.highLabel, pct('High'), AppColors.disease),
      (s.mediumLabel, pct('Medium'), AppColors.warning),
      ('Low', pct('Low'), AppColors.leaf),
    ];
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: _card(),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(s.severityBreakdown, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: AppColors.ink)),
        const SizedBox(height: 16),
        if (total == 0)
          Center(child: Padding(padding: const EdgeInsets.all(20), child: Text(s.noData, style: const TextStyle(color: AppColors.slate, fontSize: 13))))
        else
          Row(children: [
            SizedBox(width: 100, height: 100, child: PieChart(PieChartData(
              sections: sevs.map((s) => PieChartSectionData(value: s.$2, color: s.$3, title: '', radius: 38)).toList(),
              sectionsSpace: 2, centerSpaceRadius: 24, borderData: FlBorderData(show: false),
            ))),
            const SizedBox(width: 16),
            Expanded(child: Column(children: sevs.map((item) => Padding(
              padding: const EdgeInsets.symmetric(vertical: 4),
              child: Row(children: [
                Container(width: 8, height: 8, decoration: BoxDecoration(color: item.$3, shape: BoxShape.circle)),
                const SizedBox(width: 8),
                Expanded(child: Text(item.$1, style: const TextStyle(fontSize: 12, color: AppColors.graphite))),
                Text('${item.$2.toInt()}%', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w700, color: item.$3)),
              ]),
            )).toList())),
          ]),
      ]),
    );
  }

  Widget _buildTopGhCard(ReportStats stats) =>
      Container(
        padding: const EdgeInsets.all(20),
        decoration: _card(),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(s.topGreenhouses, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: AppColors.ink)),
          const SizedBox(height: 16),
          if (stats.topGreenhouses.isEmpty)
            Center(child: Padding(padding: const EdgeInsets.all(20), child: Text(s.noData, style: const TextStyle(color: AppColors.slate, fontSize: 13))))
          else
            ...stats.topGreenhouses.map((g) => Padding(
              padding: const EdgeInsets.symmetric(vertical: 6),
              child: Row(children: [
                Container(width: 28, height: 28,
                  decoration: BoxDecoration(color: AppColors.mist, borderRadius: BorderRadius.circular(8)),
                  child: Center(child: Text(g.gh, style: const TextStyle(fontSize: 10, fontWeight: FontWeight.w700, color: AppColors.forest)))),
                const SizedBox(width: 10),
                Expanded(child: Text(g.topIssue, style: const TextStyle(fontSize: 12, color: AppColors.graphite), overflow: TextOverflow.ellipsis)),
                Text('${g.findings}', style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: AppColors.ink)),
              ]),
            )),
        ]),
      );

  Widget _buildCategoryCard(ReportStats stats) {
    final entries = stats.byCategory.entries.toList()..sort((a, b) => b.value.compareTo(a.value));
    final maxVal = entries.isEmpty ? 1 : entries.first.value;
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: _card(),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(s.findingsByCategory, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: AppColors.ink)),
        const SizedBox(height: 16),
        if (entries.isEmpty)
          Center(child: Padding(padding: const EdgeInsets.all(20), child: Text(s.noData, style: const TextStyle(color: AppColors.slate, fontSize: 13))))
        else
          ...entries.map((e) => Padding(
            padding: const EdgeInsets.symmetric(vertical: 6),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Row(children: [
                Expanded(child: Text(e.key, style: const TextStyle(fontSize: 12, color: AppColors.graphite))),
                Text('${e.value}', style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w700, color: AppColors.ink)),
              ]),
              const SizedBox(height: 4),
              ClipRRect(
                borderRadius: BorderRadius.circular(4),
                child: LinearProgressIndicator(
                  value: maxVal == 0 ? 0 : e.value / maxVal,
                  minHeight: 6,
                  backgroundColor: AppColors.divider,
                  valueColor: const AlwaysStoppedAnimation(AppColors.leaf),
                ),
              ),
            ]),
          )),
      ]),
    );
  }

  Widget _buildSkeleton() => const Padding(
    padding: EdgeInsets.symmetric(vertical: 40),
    child: Center(child: CircularProgressIndicator(color: AppColors.leaf)),
  );

  Widget _buildError(String message) => Padding(
    padding: const EdgeInsets.symmetric(vertical: 40),
    child: Center(child: Text('Error: $message', style: const TextStyle(color: AppColors.critical))),
  );
}

class _LegendDot extends StatelessWidget {
  final Color color;
  final String label;
  const _LegendDot({required this.color, required this.label});
  @override
  Widget build(BuildContext context) => Row(mainAxisSize: MainAxisSize.min, children: [
    Container(width: 8, height: 8, decoration: BoxDecoration(color: color, shape: BoxShape.circle)),
    const SizedBox(width: 4),
    Text(label, style: const TextStyle(fontSize: 11, color: AppColors.slate)),
  ]);
}