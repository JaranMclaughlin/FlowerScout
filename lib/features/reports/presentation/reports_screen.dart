// reports_screen.dart
import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../shared/theme/app_colors.dart';
import '../../../shared/providers/farm_providers.dart';
import '../../../shared/providers/farm_repository.dart';

class _Inspection {
  final String date, gh, variety, type, severity, inspector;
  const _Inspection({
    required this.date, required this.gh, required this.variety,
    required this.type, required this.severity, required this.inspector,
  });
}

class _PeriodData {
  final int total, disease, pest, critical;
  final List<double> trendDisease, trendPest, trendWater;
  final double sevCritical, sevHigh, sevMedium, sevLow;
  final String aiInsight, aiRecommendation;
  final List<String> chartLabels;
  final List<_GhRank> topGreenhouses;
  const _PeriodData({
    required this.total, required this.disease, required this.pest,
    required this.critical, required this.trendDisease, required this.trendPest,
    required this.trendWater, required this.sevCritical, required this.sevHigh,
    required this.sevMedium, required this.sevLow, required this.aiInsight,
    required this.aiRecommendation, required this.chartLabels,
    required this.topGreenhouses,
  });
}

class _GhRank {
  final String gh, topIssue;
  final int findings;
  const _GhRank(this.gh, this.findings, this.topIssue);
}

class ReportsScreen extends ConsumerStatefulWidget {
  const ReportsScreen({super.key});
  @override
  ConsumerState<ReportsScreen> createState() => _ReportsScreenState();
}

class _ReportsScreenState extends ConsumerState<ReportsScreen> {
  String _selectedDate       = 'Last 7 Days';
  String _selectedFarm       = 'All Farms';
  String _selectedGreenhouse = 'All';
  String _selectedVariety    = 'All';
  String _chartType          = 'Bar';
  String _activeStatFilter   = 'all';

  static const List<String> _dateFilters = [
    'Today', 'Last 7 Days', 'Last 30 Days', 'Last 3 Months',
  ];

  static const List<_Inspection> _allInspections = [
    _Inspection(date: '08 Jun 2026', gh: 'GH-12', variety: 'Athena',     type: 'disease', severity: 'high',     inspector: 'John'),
    _Inspection(date: '07 Jun 2026', gh: 'GH-01', variety: 'Moonwalk',   type: 'pest',    severity: 'medium',   inspector: 'Peter'),
    _Inspection(date: '07 Jun 2026', gh: 'GH-25', variety: 'White Dove', type: 'water',   severity: 'low',      inspector: 'Mary'),
    _Inspection(date: '06 Jun 2026', gh: 'GH-02', variety: 'Madam Red',  type: 'disease', severity: 'critical', inspector: 'John'),
    _Inspection(date: '05 Jun 2026', gh: 'GH-03', variety: 'Explorer',   type: 'pest',    severity: 'low',      inspector: 'Grace'),
    _Inspection(date: '04 Jun 2026', gh: 'GH-12', variety: 'Athena',     type: 'disease', severity: 'medium',   inspector: 'Peter'),
    _Inspection(date: '03 Jun 2026', gh: 'GH-11', variety: 'Athena',     type: 'water',   severity: 'medium',   inspector: 'Mary'),
  ];

  static final Map<String, _PeriodData> _periodData = {
    'Today': _PeriodData(
      total: 12, disease: 7, pest: 4, critical: 1,
      trendDisease: [1, 2, 4, 2, 3, 4], trendPest: [2, 1, 3, 1, 2, 2], trendWater: [1, 0, 1, 2, 1, 2],
      sevCritical: 8, sevHigh: 25, sevMedium: 42, sevLow: 25,
      chartLabels: ['6am', '8am', '10am', '12pm', '2pm', '4pm'],
      aiInsight: "Disease is 58% of today's findings — above typical daily average.",
      aiRecommendation: 'Inspect GH-12 Athena section. Botrytis symptoms flagged by 2 scouts in the last 3 hours.',
      topGreenhouses: [_GhRank('GH-12', 5, 'Disease'), _GhRank('GH-01', 4, 'Pest'), _GhRank('GH-25', 3, 'Water Stress')],
    ),
    'Last 7 Days': _PeriodData(
      total: 128, disease: 87, pest: 56, critical: 14,
      trendDisease: [15, 22, 30, 20, 28, 48, 34], trendPest: [8, 12, 18, 14, 16, 20, 15], trendWater: [5, 8, 10, 7, 9, 12, 8],
      sevCritical: 11, sevHigh: 28, sevMedium: 38, sevLow: 23,
      chartLabels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      aiInsight: 'Disease findings are +18% above the 30-day average. Wednesday was the peak day.',
      aiRecommendation: 'Inspect GH-12 Athena section immediately. Disease incidence increased 23% vs last week. Schedule GH-02 Madam Red follow-up.',
      topGreenhouses: [_GhRank('GH-12', 38, 'Disease'), _GhRank('GH-01', 27, 'Pest'), _GhRank('GH-25', 19, 'Water Stress')],
    ),
    'Last 30 Days': _PeriodData(
      total: 340, disease: 198, pest: 102, critical: 28,
      trendDisease: [40, 58, 80, 52], trendPest: [20, 30, 42, 35], trendWater: [12, 18, 22, 18],
      sevCritical: 8, sevHigh: 30, sevMedium: 40, sevLow: 22,
      chartLabels: ['W1', 'W2', 'W3', 'W4'],
      aiInsight: 'Disease accounts for 58% of findings. Pest pressure declining across GH-01 and GH-03.',
      aiRecommendation: 'Prioritise GH-12 for a full disease audit. Consider preventive fungicide on Athena and Madam Red before end of month.',
      topGreenhouses: [_GhRank('GH-12', 110, 'Disease'), _GhRank('GH-01', 78, 'Pest'), _GhRank('GH-02', 55, 'Disease')],
    ),
    'Last 3 Months': _PeriodData(
      total: 820, disease: 450, pest: 280, critical: 60,
      trendDisease: [90, 130, 180, 120, 160, 220], trendPest: [50, 70, 95, 80, 90, 110], trendWater: [30, 40, 50, 40, 50, 65],
      sevCritical: 7, sevHigh: 32, sevMedium: 38, sevLow: 23,
      chartLabels: ['Apr W1', 'Apr W2', 'May W1', 'May W2', 'Jun W1', 'Jun W2'],
      aiInsight: 'Disease trend is consistently upward over 90 days — a structural issue, not seasonal.',
      aiRecommendation: 'Recommend crop rotation review for Athena in GH-12. Disease grew 45% quarter-over-quarter. Engage agronomist for soil and environment audit.',
      topGreenhouses: [_GhRank('GH-12', 280, 'Disease'), _GhRank('GH-01', 195, 'Pest'), _GhRank('GH-02', 140, 'Disease')],
    ),
  };

  List<String> _farmNames(List<FarmModel> farms) =>
      ['All Farms', ...farms.map((f) => f.name)];

  List<String> _greenhouseOptions(List<FarmModel> farms) {
    if (_selectedFarm == 'All Farms') return ['All'];
    final farm = farms.firstWhere((f) => f.name == _selectedFarm,
        orElse: () => farms.first);
    return ['All', ...farm.greenhouses.map((g) => g.code)];
  }

  List<String> _varietyOptions(List<FarmModel> farms) {
    if (_selectedGreenhouse == 'All') return ['All'];
    for (final farm in farms) {
      final matches = farm.greenhouses.where((g) => g.code == _selectedGreenhouse).toList();
      if (matches.isNotEmpty) return ['All', ...matches.first.varietyNames];
    }
    return ['All'];
  }

  _PeriodData get _data => _periodData[_selectedDate] ?? _periodData['Last 7 Days']!;

  List<_Inspection> get _filteredInspections {
    final list = _allInspections.toList();
    if (_activeStatFilter == 'critical') return list.where((r) => r.severity == 'critical').toList();
    if (_activeStatFilter != 'all') return list.where((r) => r.type == _activeStatFilter).toList();
    return list;
  }

  Color _severityColor(String s) => switch (s) {
    'critical' => const Color(0xFF7A1F1F),
    'high'     => const Color(0xFFA32D2D),
    'medium'   => const Color(0xFF854F0B),
    _          => const Color(0xFF3B6D11),
  };

  Color _typeColor(String t) => switch (t) {
    'disease' => const Color(0xFFA32D2D),
    'pest'    => const Color(0xFF854F0B),
    'water'   => AppColors.info,
    _         => Colors.grey,
  };

  String _typeLabel(String t) => switch (t) {
    'disease' => 'Disease',
    'pest'    => 'Pest',
    'water'   => 'Water Stress',
    _         => t,
  };

  void _showExportDialog(String type) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(18)),
        title: Text('Export ${type == 'pdf' ? 'PDF' : 'Excel'}'),
        content: Text(type == 'pdf'
            ? 'A PDF report will be generated for the current filters and saved to your device.'
            : 'An Excel (.xlsx) file with all inspection data will be saved to your device.'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancel')),
          ElevatedButton(
            onPressed: () { Navigator.pop(ctx); _triggerExport(type); },
            child: const Text('Download'),
          ),
        ],
      ),
    );
  }

  void _triggerExport(String type) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content: Text('${type == 'pdf' ? 'PDF' : 'Excel'} export ready — $_selectedFarm · $_selectedDate'),
      behavior: SnackBarBehavior.floating,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
    ));
  }

  @override
  Widget build(BuildContext context) {
    final farmsAsync = ref.watch(farmsProvider);
    final data = _data;
    return Container(
      color: AppColors.background,
      child: farmsAsync.when(
        loading: () => const Center(child: CircularProgressIndicator(color: AppColors.leaf)),
        error: (e, _) => Center(child: Text('Error: $e')),
        data: (farms) => SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Reports & Analytics',
                  style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
              const SizedBox(height: 4),
              const Text('Inspection trends, findings and performance',
                  style: TextStyle(color: Colors.grey, fontSize: 14)),
              const SizedBox(height: 20),
              _buildAiCard(data),
              const SizedBox(height: 20),
              Row(children: [
                Expanded(child: _exportButton(icon: Icons.picture_as_pdf, label: 'Export PDF',
                    color: const Color(0xFFA32D2D), onTap: () => _showExportDialog('pdf'))),
                const SizedBox(width: 12),
                Expanded(child: _exportButton(icon: Icons.table_chart, label: 'Export Excel',
                    color: const Color(0xFF3B6D11), onTap: () => _showExportDialog('excel'))),
              ]),
              const SizedBox(height: 20),
              LayoutBuilder(builder: (context, con) {
                final w = (con.maxWidth - 10) / 2;
                final ghOptions  = _greenhouseOptions(farms);
                final varOptions = _varietyOptions(farms);
                final safeGH  = ghOptions.contains(_selectedGreenhouse)  ? _selectedGreenhouse  : 'All';
                final safeVar = varOptions.contains(_selectedVariety)     ? _selectedVariety     : 'All';
                return Wrap(spacing: 10, runSpacing: 10, children: [
                  SizedBox(width: w, child: _dropdown(label: 'Date Range', value: _selectedDate,
                      items: _dateFilters, onChanged: (v) => setState(() => _selectedDate = v!))),
                  SizedBox(width: w, child: _dropdown(label: 'Farm', value: _selectedFarm,
                      items: _farmNames(farms), onChanged: (v) => setState(() {
                        _selectedFarm = v!; _selectedGreenhouse = 'All'; _selectedVariety = 'All';
                      }))),
                  SizedBox(width: w, child: _dropdown(label: 'Greenhouse', value: safeGH,
                      items: ghOptions, onChanged: (v) => setState(() {
                        _selectedGreenhouse = v!; _selectedVariety = 'All';
                      }))),
                  SizedBox(width: w, child: _dropdown(label: 'Variety', value: safeVar,
                      items: varOptions, onChanged: (v) => setState(() => _selectedVariety = v!))),
                ]);
              }),
              const SizedBox(height: 24),
              LayoutBuilder(builder: (context, constraints) {
                final isWide = constraints.maxWidth > 600;
                if (isWide) {
                  return Row(children: [
                    Expanded(child: _statCard(id: 'all',      label: 'Inspections', value: data.total,    icon: Icons.assignment_outlined,   color: const Color(0xFF2D6A2D), trend: '+12%', trendUp: true)),
                    const SizedBox(width: 8),
                    Expanded(child: _statCard(id: 'disease',  label: 'Disease',     value: data.disease,  icon: Icons.coronavirus_outlined,  color: const Color(0xFFB53030), trend: '+18%', trendUp: false)),
                    const SizedBox(width: 8),
                    Expanded(child: _statCard(id: 'pest',     label: 'Pests',       value: data.pest,     icon: Icons.bug_report_outlined,   color: const Color(0xFF9A5C00), trend: '-5%',  trendUp: true)),
                    const SizedBox(width: 8),
                    Expanded(child: _statCard(id: 'critical', label: 'Critical',    value: data.critical, icon: Icons.warning_amber_rounded, color: const Color(0xFF7A1F1F), trend: '+3',   trendUp: false)),
                  ]);
                }
                return SizedBox(height: 100, child: ListView(scrollDirection: Axis.horizontal, children: [
                  SizedBox(width: 130, child: _statCard(id: 'all',      label: 'Inspections', value: data.total,    icon: Icons.assignment_outlined,   color: const Color(0xFF2D6A2D), trend: '+12%', trendUp: true)),
                  const SizedBox(width: 8),
                  SizedBox(width: 130, child: _statCard(id: 'disease',  label: 'Disease',     value: data.disease,  icon: Icons.coronavirus_outlined,  color: const Color(0xFFB53030), trend: '+18%', trendUp: false)),
                  const SizedBox(width: 8),
                  SizedBox(width: 130, child: _statCard(id: 'pest',     label: 'Pests',       value: data.pest,     icon: Icons.bug_report_outlined,   color: const Color(0xFF9A5C00), trend: '-5%',  trendUp: true)),
                  const SizedBox(width: 8),
                  SizedBox(width: 130, child: _statCard(id: 'critical', label: 'Critical',    value: data.critical, icon: Icons.warning_amber_rounded, color: const Color(0xFF7A1F1F), trend: '+3',   trendUp: false)),
                ]));
              }),
              const SizedBox(height: 24),
              Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
                const Text('Findings Trend', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                _chartToggle(),
              ]),
              const SizedBox(height: 8),
              _trendLegend(),
              const SizedBox(height: 10),
              Container(
                height: 220, width: double.infinity,
                padding: const EdgeInsets.fromLTRB(8, 16, 16, 8),
                decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(18)),
                child: _chartType == 'Bar' ? _buildBarChart(data) : _buildLineChart(data),
              ),
              const SizedBox(height: 24),
              const Text('Severity Breakdown', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
              const SizedBox(height: 10),
              _severitySection(data),
              const SizedBox(height: 24),
              const Text('Top Problem Categories', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
              const SizedBox(height: 10),
              _categoryTile('Disease',      42, const Color(0xFFE24B4A), '+4%', false),
              _categoryTile('Pests',        28, const Color(0xFFEF9F27), '-2%', true),
              _categoryTile('Water Stress', 15, const Color(0xFF378ADD), '0%',  true),
              _categoryTile('Nutrition',    10, const Color(0xFF639922), '-1%', true),
              _categoryTile('Other',         5, Colors.grey,             '—',   true),
              const SizedBox(height: 24),
              const Text('Top Greenhouses by Findings', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
              const SizedBox(height: 10),
              _topGreenhousesSection(data),
              const SizedBox(height: 24),
              Row(children: [
                const Text('Recent Inspections', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                if (_activeStatFilter != 'all') ...[
                  const SizedBox(width: 8),
                  _chip(_typeLabel(_activeStatFilter), AppColors.info, const Color(0xFFE6F1FB)),
                ],
              ]),
              const SizedBox(height: 10),
              _inspectionList(),
              const SizedBox(height: 32),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildAiCard(_PeriodData data) => Container(
    decoration: const BoxDecoration(
      gradient: LinearGradient(colors: [Color(0xFF1B4D1B), Color(0xFF2D6A2D)],
          begin: Alignment.topLeft, end: Alignment.bottomRight),
      borderRadius: BorderRadius.all(Radius.circular(16)),
    ),
    padding: const EdgeInsets.all(14),
    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Row(children: [
        Container(padding: const EdgeInsets.all(5),
          decoration: BoxDecoration(color: Colors.white.withValues(alpha: 0.15),
              borderRadius: const BorderRadius.all(Radius.circular(8))),
          child: const Icon(Icons.auto_awesome, size: 13, color: Colors.white)),
        const SizedBox(width: 7),
        const Text('AI Insight', style: TextStyle(color: Colors.white,
            fontWeight: FontWeight.w700, fontSize: 13)),
      ]),
      const SizedBox(height: 8),
      Text(data.aiInsight, style: TextStyle(color: Colors.white.withValues(alpha: 0.9),
          fontSize: 12, height: 1.4)),
      const SizedBox(height: 8),
      Container(
        padding: const EdgeInsets.all(10),
        decoration: BoxDecoration(
          color: Colors.white.withValues(alpha: 0.1),
          borderRadius: const BorderRadius.all(Radius.circular(12)),
          border: Border.all(color: Colors.white.withValues(alpha: 0.15)),
        ),
        child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const Icon(Icons.arrow_right_alt, size: 14, color: Colors.white),
          const SizedBox(width: 6),
          Expanded(child: Text(data.aiRecommendation,
              style: TextStyle(color: Colors.white.withValues(alpha: 0.85),
                  fontSize: 11, height: 1.4))),
        ]),
      ),
    ]),
  );

  Widget _severitySection(_PeriodData data) {
    final sections = [
      PieChartSectionData(value: data.sevCritical, color: const Color(0xFF7A1F1F), title: '', radius: 50),
      PieChartSectionData(value: data.sevHigh,     color: const Color(0xFFA32D2D), title: '', radius: 50),
      PieChartSectionData(value: data.sevMedium,   color: const Color(0xFFEF9F27), title: '', radius: 50),
      PieChartSectionData(value: data.sevLow,      color: const Color(0xFF3B6D11), title: '', radius: 50),
    ];
    final labels = [
      ('Critical', '${data.sevCritical.toInt()}%', const Color(0xFF7A1F1F)),
      ('High',     '${data.sevHigh.toInt()}%',     const Color(0xFFA32D2D)),
      ('Medium',   '${data.sevMedium.toInt()}%',   const Color(0xFFEF9F27)),
      ('Low',      '${data.sevLow.toInt()}%',       const Color(0xFF3B6D11)),
    ];
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(18)),
      child: Row(children: [
        SizedBox(width: 130, height: 130,
          child: PieChart(PieChartData(sections: sections, sectionsSpace: 2,
              centerSpaceRadius: 30, borderData: FlBorderData(show: false)))),
        const SizedBox(width: 20),
        Expanded(child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: labels.map((l) => Padding(
            padding: const EdgeInsets.symmetric(vertical: 5),
            child: Row(children: [
              Container(width: 10, height: 10,
                  decoration: BoxDecoration(color: l.$3, shape: BoxShape.circle)),
              const SizedBox(width: 8),
              Expanded(child: Text(l.$1, style: const TextStyle(fontSize: 13))),
              Text(l.$2, style: TextStyle(fontSize: 13,
                  fontWeight: FontWeight.bold, color: l.$3)),
            ]),
          )).toList(),
        )),
      ]),
    );
  }

  Widget _topGreenhousesSection(_PeriodData data) {
    final maxF = data.topGreenhouses.fold(0, (m, g) => g.findings > m ? g.findings : m).toDouble();
    final medalColors = [const Color(0xFFBA7517), const Color(0xFF888780), const Color(0xFF854F0B)];
    return Container(
      decoration: const BoxDecoration(color: Colors.white,
          borderRadius: BorderRadius.all(Radius.circular(16))),
      child: Column(children: data.topGreenhouses.asMap().entries.map((entry) {
        final rank = entry.key + 1;
        final gh   = entry.value;
        final pct  = maxF > 0 ? gh.findings / maxF : 0.0;
        final ic   = _typeColor(gh.topIssue.toLowerCase().replaceAll(' stress', ''));
        return Column(children: [
          Padding(padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            child: Row(children: [
              Container(width: 26, height: 26,
                decoration: BoxDecoration(color: medalColors[rank-1].withValues(alpha: 0.12),
                    shape: BoxShape.circle),
                child: Center(child: Text('#$rank', style: TextStyle(fontSize: 11,
                    fontWeight: FontWeight.bold, color: medalColors[rank-1])))),
              const SizedBox(width: 12),
              Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(gh.gh, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                const SizedBox(height: 4),
                ClipRRect(borderRadius: BorderRadius.circular(4),
                  child: LinearProgressIndicator(value: pct, minHeight: 5,
                      backgroundColor: Colors.grey.shade100,
                      valueColor: AlwaysStoppedAnimation<Color>(ic))),
              ])),
              const SizedBox(width: 12),
              Column(crossAxisAlignment: CrossAxisAlignment.end, children: [
                Text('${gh.findings}', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                const SizedBox(height: 2),
                _chip(gh.topIssue, ic, ic.withValues(alpha: 0.1)),
              ]),
            ])),
          if (rank < data.topGreenhouses.length)
            const Divider(height: 1, indent: 16, endIndent: 16),
        ]);
      }).toList()),
    );
  }

  Widget _inspectionList() {
    final rows = _filteredInspections;
    return Container(
      decoration: const BoxDecoration(color: Colors.white,
          borderRadius: BorderRadius.all(Radius.circular(16))),
      child: rows.isEmpty
          ? const Padding(padding: EdgeInsets.all(20),
              child: Text('No inspections match this filter.',
                  style: TextStyle(color: Colors.grey)))
          : Column(children: rows.asMap().entries.map((entry) {
              final i = entry.key;
              final r = entry.value;
              return Column(children: [
                Material(color: Colors.transparent, child: ListTile(
                  onTap: () => ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                    content: Text('Opening: ${r.date} · ${r.gh} · ${r.variety}'),
                    behavior: SnackBarBehavior.floating,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                  )),
                  title: Text('${r.date} · ${r.gh} · ${r.variety}',
                      style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
                  subtitle: Padding(padding: const EdgeInsets.only(top: 4),
                    child: Wrap(spacing: 6, runSpacing: 4, children: [
                      _chip(_typeLabel(r.type), _typeColor(r.type),
                          _typeColor(r.type).withValues(alpha: 0.1)),
                      _chip(r.severity[0].toUpperCase() + r.severity.substring(1),
                          _severityColor(r.severity),
                          _severityColor(r.severity).withValues(alpha: 0.1)),
                      Text(r.inspector, style: const TextStyle(fontSize: 12, color: Colors.grey)),
                    ])),
                  trailing: const Icon(Icons.chevron_right, color: Colors.grey, size: 18),
                )),
                if (i < rows.length - 1) const Divider(height: 1, indent: 16, endIndent: 16),
              ]);
            }).toList()),
    );
  }

  Widget _buildBarChart(_PeriodData data) {
    final labels = data.chartLabels;
    final maxY   = data.trendDisease.reduce((a, b) => a > b ? a : b) * 1.25;
    final count  = labels.length;
    return BarChart(BarChartData(
      alignment: BarChartAlignment.spaceAround, maxY: maxY,
      barTouchData: BarTouchData(touchTooltipData: BarTouchTooltipData(
        getTooltipItem: (group, gi, rod, ri) => BarTooltipItem(
          '${['Disease','Pests','Water'][ri]}: ${rod.toY.toInt()}',
          const TextStyle(color: Colors.white, fontSize: 11)),
      )),
      titlesData: FlTitlesData(
        leftTitles:   AxisTitles(sideTitles: SideTitles(showTitles: false)),
        rightTitles:  AxisTitles(sideTitles: SideTitles(showTitles: false)),
        topTitles:    AxisTitles(sideTitles: SideTitles(showTitles: false)),
        bottomTitles: AxisTitles(sideTitles: SideTitles(
          showTitles: true, reservedSize: 28,
          getTitlesWidget: (v, m) {
            final idx = v.toInt();
            if (idx < 0 || idx >= count) return const SizedBox();
            return Padding(padding: const EdgeInsets.only(top: 6),
              child: Text(labels[idx], style: const TextStyle(fontSize: 10, color: Colors.grey)));
          },
        )),
      ),
      gridData: FlGridData(drawVerticalLine: false,
          getDrawingHorizontalLine: (_) => FlLine(color: Colors.grey.shade100, strokeWidth: 1)),
      borderData: FlBorderData(show: false),
      barGroups: List.generate(count, (i) => BarChartGroupData(x: i, barRods: [
        BarChartRodData(toY: data.trendDisease[i], color: const Color(0xFF3B6D11), width: 5, borderRadius: BorderRadius.circular(4)),
        BarChartRodData(toY: data.trendPest[i],    color: const Color(0xFFEF9F27), width: 5, borderRadius: BorderRadius.circular(4)),
        BarChartRodData(toY: data.trendWater[i],   color: const Color(0xFF378ADD), width: 5, borderRadius: BorderRadius.circular(4)),
      ])),
    ));
  }

  Widget _buildLineChart(_PeriodData data) {
    final labels = data.chartLabels;
    final maxY   = data.trendDisease.reduce((a, b) => a > b ? a : b) * 1.25;
    final count  = labels.length;

    LineChartBarData series(List<double> vals, Color color) => LineChartBarData(
      spots: vals.asMap().entries.map((e) => FlSpot(e.key.toDouble(), e.value)).toList(),
      isCurved: true, color: color, barWidth: 2.5,
      dotData: const FlDotData(show: true),
      belowBarData: BarAreaData(show: false),
    );

    return LineChart(LineChartData(
      minY: 0, maxY: maxY,
      lineTouchData: LineTouchData(touchTooltipData: LineTouchTooltipData(
        getTooltipItems: (spots) => spots.map((s) => LineTooltipItem(
          '${['Disease','Pests','Water'][s.barIndex]}: ${s.y.toInt()}',
          const TextStyle(color: Colors.white, fontSize: 11))).toList(),
      )),
      titlesData: FlTitlesData(
        leftTitles:   AxisTitles(sideTitles: SideTitles(showTitles: false)),
        rightTitles:  AxisTitles(sideTitles: SideTitles(showTitles: false)),
        topTitles:    AxisTitles(sideTitles: SideTitles(showTitles: false)),
        bottomTitles: AxisTitles(sideTitles: SideTitles(
          showTitles: true, reservedSize: 28,
          getTitlesWidget: (v, m) {
            final idx = v.toInt();
            if (idx < 0 || idx >= count) return const SizedBox();
            return Padding(padding: const EdgeInsets.only(top: 6),
              child: Text(labels[idx], style: const TextStyle(fontSize: 10, color: Colors.grey)));
          },
        )),
      ),
      gridData: FlGridData(drawVerticalLine: false,
          getDrawingHorizontalLine: (_) => FlLine(color: Colors.grey.shade100, strokeWidth: 1)),
      borderData: FlBorderData(show: false),
      lineBarsData: [
        series(data.trendDisease, const Color(0xFF3B6D11)),
        series(data.trendPest,    const Color(0xFFEF9F27)),
        series(data.trendWater,   const Color(0xFF378ADD)),
      ],
    ));
  }

  Widget _exportButton({required IconData icon, required String label,
      required Color color, required VoidCallback onTap}) =>
    Material(color: Colors.white, borderRadius: BorderRadius.circular(14),
      child: InkWell(borderRadius: BorderRadius.circular(14), onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 14),
          decoration: BoxDecoration(border: Border.all(color: color.withValues(alpha: 0.3)),
              borderRadius: BorderRadius.circular(14)),
          child: Row(mainAxisAlignment: MainAxisAlignment.center, children: [
            Icon(icon, color: color, size: 20),
            const SizedBox(width: 8),
            Text(label, style: TextStyle(fontWeight: FontWeight.w600, color: color, fontSize: 14)),
          ]),
        ),
      ),
    );

  Widget _dropdown({required String label, required String value,
      required List<String> items, required ValueChanged<String?> onChanged}) =>
    DropdownButtonFormField<String>(
      value: value, isExpanded: true,
      decoration: InputDecoration(
        labelText: label,
        labelStyle: const TextStyle(fontSize: 11, color: Colors.grey),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: Color(0xFFE2E8E2))),
        enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: Color(0xFFE2E8E2))),
        focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: AppColors.leaf, width: 1.5)),
        contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
        isDense: true, filled: true, fillColor: Colors.white,
      ),
      style: const TextStyle(fontSize: 12, color: Color(0xFF1A1F1A), fontWeight: FontWeight.w500),
      items: items.map((e) => DropdownMenuItem(value: e,
          child: Text(e, overflow: TextOverflow.ellipsis))).toList(),
      onChanged: onChanged,
    );

  Widget _statCard({required String id, required String label, required int value,
      required IconData icon, required Color color, required String trend,
      required bool trendUp}) {
    final isActive = _activeStatFilter == id;
    return GestureDetector(
      onTap: () => setState(() => _activeStatFilter = id),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        decoration: BoxDecoration(
          color: Colors.white, borderRadius: BorderRadius.circular(16),
          border: isActive ? Border.all(color: AppColors.info, width: 2)
              : Border.all(color: Colors.grey.shade200),
        ),
        padding: const EdgeInsets.all(10),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min, children: [
          Row(children: [
            Container(padding: const EdgeInsets.all(5),
              decoration: BoxDecoration(color: color.withValues(alpha: 0.12),
                  borderRadius: BorderRadius.circular(8)),
              child: Icon(icon, size: 14, color: color)),
            const Spacer(),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 2),
              decoration: BoxDecoration(
                color: trendUp ? const Color(0xFFE8F5E8) : const Color(0xFFFFF0F0),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Text(trend, style: TextStyle(fontSize: 9, fontWeight: FontWeight.w700,
                  color: trendUp ? AppColors.leaf : AppColors.critical)),
            ),
          ]),
          const SizedBox(height: 6),
          Text('$value', style: const TextStyle(fontSize: 22,
              fontWeight: FontWeight.w800, color: Color(0xFF1A1F1A), height: 1)),
          const SizedBox(height: 1),
          Text(label, style: const TextStyle(fontSize: 10,
              color: Colors.grey, fontWeight: FontWeight.w500)),
        ]),
      ),
    );
  }

  Widget _chartToggle() => Row(
    children: ['Bar', 'Line'].map((type) {
      final active = _chartType == type;
      return GestureDetector(
        onTap: () => setState(() => _chartType = type),
        child: Container(
          margin: const EdgeInsets.only(left: 6),
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 5),
          decoration: BoxDecoration(
            color: active ? AppColors.info : Colors.transparent,
            borderRadius: BorderRadius.circular(20),
            border: Border.all(color: active ? AppColors.info : Colors.grey.shade300),
          ),
          child: Text(type, style: TextStyle(fontSize: 12,
            color: active ? Colors.white : Colors.grey.shade600,
            fontWeight: active ? FontWeight.bold : FontWeight.normal)),
        ),
      );
    }).toList(),
  );

  Widget _trendLegend() => Wrap(spacing: 14, children: [
    ('Disease',      const Color(0xFF3B6D11)),
    ('Pests',        const Color(0xFFEF9F27)),
    ('Water Stress', const Color(0xFF378ADD)),
  ].map((item) => Row(mainAxisSize: MainAxisSize.min, children: [
    Container(width: 10, height: 10, decoration: BoxDecoration(
        color: item.$2, borderRadius: BorderRadius.circular(2))),
    const SizedBox(width: 4),
    Text(item.$1, style: const TextStyle(fontSize: 12, color: Colors.grey)),
  ])).toList());

  Widget _categoryTile(String title, int pct, Color color, String delta, bool improved) =>
    Card(margin: const EdgeInsets.only(bottom: 8),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
        child: Row(children: [
          Container(width: 10, height: 10,
              decoration: BoxDecoration(color: color, shape: BoxShape.circle)),
          const SizedBox(width: 10),
          Expanded(child: Text(title, style: const TextStyle(fontSize: 13))),
          SizedBox(width: 110, child: ClipRRect(borderRadius: BorderRadius.circular(4),
            child: LinearProgressIndicator(value: pct / 100,
              backgroundColor: Colors.grey.shade100,
              valueColor: AlwaysStoppedAnimation<Color>(color), minHeight: 6))),
          const SizedBox(width: 10),
          SizedBox(width: 32, child: Text('$pct%',
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
            textAlign: TextAlign.right)),
          const SizedBox(width: 8),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 2),
            decoration: BoxDecoration(
              color: delta == '—' ? Colors.grey.shade100
                  : improved ? Colors.green.shade50 : Colors.red.shade50,
              borderRadius: BorderRadius.circular(20),
            ),
            child: Text(delta, style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold,
              color: delta == '—' ? Colors.grey
                  : improved ? const Color(0xFF3B6D11) : const Color(0xFFA32D2D))),
          ),
        ]),
      ),
    );

  Widget _chip(String label, Color textColor, Color bgColor) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
    decoration: BoxDecoration(color: bgColor, borderRadius: BorderRadius.circular(20)),
    child: Text(label, style: TextStyle(fontSize: 11, color: textColor,
        fontWeight: FontWeight.w600)),
  );
}