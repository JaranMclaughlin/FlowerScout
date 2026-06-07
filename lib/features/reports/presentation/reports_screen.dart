// reports_screen.dart
//
// Dependencies (pubspec.yaml):
//   fl_chart: ^0.68.0
//
// TODO: Add when connecting real exports:
//   pdf: ^3.10.8
//   excel: ^4.0.3
//   share_plus: ^7.2.1
//   path_provider: ^2.1.2

import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

// ─────────────────────────────────────────────────────────────────────────────
// DATA MODELS
// ─────────────────────────────────────────────────────────────────────────────

class _Inspection {
  final String date;
  final String gh;
  final String variety;
  final String type;     // 'disease' | 'pest' | 'water'
  final String severity; // 'critical' | 'high' | 'medium' | 'low'
  final String inspector;

  const _Inspection({
    required this.date,
    required this.gh,
    required this.variety,
    required this.type,
    required this.severity,
    required this.inspector,
  });
}

class _PeriodData {
  final int total;
  final int disease;
  final int pest;
  final int critical;
  final List<double> trendDisease;
  final List<double> trendPest;
  final List<double> trendWater;
  // Severity breakdown for pie chart
  final double sevCritical;
  final double sevHigh;
  final double sevMedium;
  final double sevLow;
  // AI recommendation text
  final String aiInsight;
  final String aiRecommendation;
  // Chart x-axis labels matched to period
  final List<String> chartLabels;
  // Top greenhouses: gh -> finding count
  final List<_GhRank> topGreenhouses;

  const _PeriodData({
    required this.total,
    required this.disease,
    required this.pest,
    required this.critical,
    required this.trendDisease,
    required this.trendPest,
    required this.trendWater,
    required this.sevCritical,
    required this.sevHigh,
    required this.sevMedium,
    required this.sevLow,
    required this.aiInsight,
    required this.aiRecommendation,
    required this.chartLabels,
    required this.topGreenhouses,
  });
}

class _GhRank {
  final String gh;
  final int findings;
  final String topIssue;
  const _GhRank(this.gh, this.findings, this.topIssue);
}

// ─────────────────────────────────────────────────────────────────────────────
// SCREEN
// ─────────────────────────────────────────────────────────────────────────────

class ReportsScreen extends StatefulWidget {
  const ReportsScreen({super.key});

  @override
  State<ReportsScreen> createState() => _ReportsScreenState();
}

class _ReportsScreenState extends State<ReportsScreen> {
  // ── filter state ────────────────────────────────────────────────────────────
  String _selectedDate = 'Last 7 Days';
  String _selectedFarm = 'All Farms';
  String _selectedGreenhouse = 'All';
  String _selectedVariety = 'All';
  String _chartType = 'Bar';
  String _activeStatFilter = 'all';

  // ── filter options ──────────────────────────────────────────────────────────
  static const List<String> _dateFilters = [
    'Today',
    'Last 7 Days',
    'Last 30 Days',
    'Last 3 Months',
  ];

  static const Map<String, List<String>> _farmGreenhouses = {
    'All Farms': ['All'],
    'Kongoni River Farm': ['All', 'GH-01', 'GH-02', 'GH-03', 'GH-12', 'GH-25'],
    'Main Farm': ['All', 'GH-11', 'GH-12', 'GH-13'],
    'North Farm': ['All', 'GH-21', 'GH-22'],
  };

  static const Map<String, List<String>> _ghVarieties = {
    'GH-01': ['All', 'Athena', 'Moonwalk'],
    'GH-02': ['All', 'Madam Red'],
    'GH-03': ['All', 'Explorer'],
    'GH-12': ['All', 'Athena', 'Madam Red'],
    'GH-25': ['All', 'White Dove'],
  };

  // ── inspection data ─────────────────────────────────────────────────────────
  static const List<_Inspection> _allInspections = [
    _Inspection(date: '08 Jun 2026', gh: 'GH-12', variety: 'Athena',     type: 'disease', severity: 'high',     inspector: 'John'),
    _Inspection(date: '07 Jun 2026', gh: 'GH-01', variety: 'Moonwalk',   type: 'pest',    severity: 'medium',   inspector: 'Peter'),
    _Inspection(date: '07 Jun 2026', gh: 'GH-25', variety: 'White Dove', type: 'water',   severity: 'low',      inspector: 'Mary'),
    _Inspection(date: '06 Jun 2026', gh: 'GH-02', variety: 'Madam Red',  type: 'disease', severity: 'critical', inspector: 'John'),
    _Inspection(date: '05 Jun 2026', gh: 'GH-03', variety: 'Explorer',   type: 'pest',    severity: 'low',      inspector: 'Grace'),
    _Inspection(date: '04 Jun 2026', gh: 'GH-12', variety: 'Athena',     type: 'disease', severity: 'medium',   inspector: 'Peter'),
    _Inspection(date: '03 Jun 2026', gh: 'GH-11', variety: 'Athena',     type: 'water',   severity: 'medium',   inspector: 'Mary'),
  ];

  // ── period data ─────────────────────────────────────────────────────────────
  // Chart labels are meaningful per period — not hard-coded month names.
  static final Map<String, _PeriodData> _periodData = {
    'Today': _PeriodData(
      total: 12, disease: 7, pest: 4, critical: 1,
      trendDisease: [1.0, 2.0, 4.0, 2.0, 3.0, 4.0],
      trendPest:    [2.0, 1.0, 3.0, 1.0, 2.0, 2.0],
      trendWater:   [1.0, 0.0, 1.0, 2.0, 1.0, 2.0],
      sevCritical: 8, sevHigh: 25, sevMedium: 42, sevLow: 25,
      chartLabels: ['6am', '8am', '10am', '12pm', '2pm', '4pm'],
      aiInsight: "Disease is 58% of today's findings — above typical daily average.",
      aiRecommendation: 'Inspect GH-12 Athena section. Botrytis symptoms flagged by 2 scouts in the last 3 hours.',
      topGreenhouses: [
        _GhRank('GH-12', 5, 'Disease'),
        _GhRank('GH-01', 4, 'Pest'),
        _GhRank('GH-25', 3, 'Water Stress'),
      ],
    ),
    'Last 7 Days': _PeriodData(
      total: 128, disease: 87, pest: 56, critical: 14,
      trendDisease: [15.0, 22.0, 30.0, 20.0, 28.0, 48.0, 34.0],
      trendPest:    [8.0,  12.0, 18.0, 14.0, 16.0, 20.0, 15.0],
      trendWater:   [5.0,  8.0,  10.0, 7.0,  9.0,  12.0, 8.0],
      sevCritical: 11, sevHigh: 28, sevMedium: 38, sevLow: 23,
      chartLabels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      aiInsight: 'Disease findings are +18% above the 30-day average. Wednesday was the peak day.',
      aiRecommendation: 'Inspect GH-12 Athena section immediately. Disease incidence increased 23% compared to last week. Schedule GH-02 Madam Red follow-up.',
      topGreenhouses: [
        _GhRank('GH-12', 38, 'Disease'),
        _GhRank('GH-01', 27, 'Pest'),
        _GhRank('GH-25', 19, 'Water Stress'),
      ],
    ),
    'Last 30 Days': _PeriodData(
      total: 340, disease: 198, pest: 102, critical: 28,
      trendDisease: [40.0, 58.0, 80.0, 52.0],
      trendPest:    [20.0, 30.0, 42.0, 35.0],
      trendWater:   [12.0, 18.0, 22.0, 18.0],
      sevCritical: 8, sevHigh: 30, sevMedium: 40, sevLow: 22,
      chartLabels: ['W1', 'W2', 'W3', 'W4'],
      aiInsight: 'Disease accounts for 58% of findings. Pest pressure is declining across GH-01 and GH-03.',
      aiRecommendation: 'Prioritise GH-12 for a full disease audit. Consider applying preventive fungicide treatment to Athena and Madam Red varieties before end of month.',
      topGreenhouses: [
        _GhRank('GH-12', 110, 'Disease'),
        _GhRank('GH-01', 78, 'Pest'),
        _GhRank('GH-02', 55, 'Disease'),
      ],
    ),
    'Last 3 Months': _PeriodData(
      total: 820, disease: 450, pest: 280, critical: 60,
      trendDisease: [90.0, 130.0, 180.0, 120.0, 160.0, 220.0],
      trendPest:    [50.0, 70.0,  95.0,  80.0,  90.0,  110.0],
      trendWater:   [30.0, 40.0,  50.0,  40.0,  50.0,  65.0],
      sevCritical: 7, sevHigh: 32, sevMedium: 38, sevLow: 23,
      chartLabels: ['Apr W1', 'Apr W2', 'May W1', 'May W2', 'Jun W1', 'Jun W2'],
      aiInsight: 'Disease trend is consistently upward over 90 days — a structural issue, not seasonal.',
      aiRecommendation: 'Recommend a crop rotation review for Athena variety in GH-12. Disease incidence has grown 45% quarter-over-quarter. Engage agronomist for a soil and environment audit.',
      topGreenhouses: [
        _GhRank('GH-12', 280, 'Disease'),
        _GhRank('GH-01', 195, 'Pest'),
        _GhRank('GH-02', 140, 'Disease'),
      ],
    ),
  };

  // ── computed getters ────────────────────────────────────────────────────────
  _PeriodData get _data => _periodData[_selectedDate] ?? _periodData['Last 7 Days']!;

  List<String> get _greenhouses => _farmGreenhouses[_selectedFarm] ?? ['All'];

  List<String> get _varieties {
    if (_selectedGreenhouse == 'All') return ['All'];
    return _ghVarieties[_selectedGreenhouse] ?? ['All'];
  }

  List<_Inspection> get _filteredInspections {
    var list = _allInspections.toList();
    if (_activeStatFilter == 'critical') {
      return list.where((r) => r.severity == 'critical').toList();
    }
    if (_activeStatFilter != 'all') {
      return list.where((r) => r.type == _activeStatFilter).toList();
    }
    return list;
  }

  // ── helpers ─────────────────────────────────────────────────────────────────
  Color _severityColor(String s) {
    switch (s) {
      case 'critical': return const Color(0xFF7A1F1F);
      case 'high':     return const Color(0xFFA32D2D);
      case 'medium':   return const Color(0xFF854F0B);
      default:         return const Color(0xFF3B6D11);
    }
  }

  Color _typeColor(String t) {
    switch (t) {
      case 'disease': return const Color(0xFFA32D2D);
      case 'pest':    return const Color(0xFF854F0B);
      case 'water':   return const Color(0xFF185FA5);
      default:        return Colors.grey;
    }
  }

  String _typeLabel(String t) {
    switch (t) {
      case 'disease': return 'Disease';
      case 'pest':    return 'Pest';
      case 'water':   return 'Water Stress';
      default:        return t;
    }
  }

  // ── export ──────────────────────────────────────────────────────────────────
  void _showExportDialog(String type) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(18)),
        title: Text('Export ${type == 'pdf' ? 'PDF' : 'Excel'}'),
        content: Text(
          type == 'pdf'
              ? 'A PDF report will be generated for the current filters and saved to your device.'
              : 'An Excel (.xlsx) file with all inspection data for the selected filters will be saved to your device.',
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancel')),
          ElevatedButton(
            onPressed: () {
              Navigator.pop(ctx);
              _triggerExport(type);
            },
            child: const Text('Download'),
          ),
        ],
      ),
    );
  }

  void _triggerExport(String type) {
    // TODO: Connect PDF export service
    // Example:
    //   final pdf = pw.Document();
    //   pdf.addPage(pw.Page(build: (_) => pw.Text('Report')));
    //   final bytes = await pdf.save();
    //   final dir = await getApplicationDocumentsDirectory();
    //   final file = File('${dir.path}/report.pdf');
    //   await file.writeAsBytes(bytes);
    //   await Share.shareXFiles([XFile(file.path)]);

    // TODO: Connect Excel export service
    // Example:
    //   final excel = Excel.createExcel();
    //   final sheet = excel['Inspections'];
    //   for (final row in _allInspections) {
    //     sheet.appendRow([row.date, row.gh, row.variety, row.type, row.severity]);
    //   }
    //   final bytes = excel.save();
    //   final file = File('${dir.path}/inspections.xlsx');
    //   await file.writeAsBytes(bytes!);

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          '${type == 'pdf' ? 'PDF' : 'Excel'} export ready — $_selectedFarm · $_selectedDate',
        ),
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      ),
    );
  }

  // ─────────────────────────────────────────────────────────────────────────
  // BUILD
  // ─────────────────────────────────────────────────────────────────────────

  @override
  Widget build(BuildContext context) {
    final data = _data;

    // Use Container instead of Scaffold — avoids nested Scaffold issues
    // when this screen lives inside an AppShell that already has a Scaffold.
    return Container(
      color: const Color(0xFFF6F8F7),
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // ── Header ─────────────────────────────────────────────────────
            const Text(
              'Reports & Analytics',
              style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 4),
            const Text(
              'Inspection trends, findings and performance',
              style: TextStyle(color: Colors.grey, fontSize: 14),
            ),
            const SizedBox(height: 20),

            // ── AI Insight + Recommendation ────────────────────────────────
            _aiInsightBox(data),
            const SizedBox(height: 20),

            // ── Export Buttons (above filters) ─────────────────────────────
            Row(
              children: [
                Expanded(child: _exportButton(
                  icon: Icons.picture_as_pdf,
                  label: 'Export PDF',
                  color: const Color(0xFFA32D2D),
                  onTap: () => _showExportDialog('pdf'),
                )),
                const SizedBox(width: 12),
                Expanded(child: _exportButton(
                  icon: Icons.table_chart,
                  label: 'Export Excel',
                  color: const Color(0xFF3B6D11),
                  onTap: () => _showExportDialog('excel'),
                )),
              ],
            ),
            const SizedBox(height: 20),

            // ── Filters ────────────────────────────────────────────────────
            Wrap(
              spacing: 10,
              runSpacing: 10,
              children: [
                _dropdown(
                  label: 'Date Range',
                  value: _selectedDate,
                  items: _dateFilters,
                  onChanged: (v) => setState(() => _selectedDate = v!),
                ),
                _dropdown(
                  label: 'Farm',
                  value: _selectedFarm,
                  items: _farmGreenhouses.keys.toList(),
                  onChanged: (v) => setState(() {
                    _selectedFarm = v!;
                    _selectedGreenhouse = 'All';
                    _selectedVariety = 'All';
                  }),
                ),
                _dropdown(
                  label: 'Greenhouse',
                  value: _selectedGreenhouse,
                  items: _greenhouses,
                  onChanged: (v) => setState(() {
                    _selectedGreenhouse = v!;
                    _selectedVariety = 'All';
                  }),
                ),
                _dropdown(
                  label: 'Variety',
                  value: _selectedVariety,
                  items: _varieties,
                  onChanged: (v) => setState(() => _selectedVariety = v!),
                ),
              ],
            ),
            const SizedBox(height: 24),

            // ── Stat Cards ─────────────────────────────────────────────────
            LayoutBuilder(builder: (context, constraints) {
              final cols = constraints.maxWidth < 360 ? 2 : 4;
              return GridView.count(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                crossAxisCount: cols,
                crossAxisSpacing: 12,
                mainAxisSpacing: 12,
                childAspectRatio: 1.0,
                children: [
                  _statCard(id: 'all',      label: 'Inspections', value: data.total,    icon: Icons.assignment,  color: const Color(0xFF3B6D11), trend: '+12%', trendUp: true),
                  _statCard(id: 'disease',  label: 'Disease',     value: data.disease,  icon: Icons.coronavirus, color: const Color(0xFFA32D2D), trend: '+18%', trendUp: false),
                  _statCard(id: 'pest',     label: 'Pests',       value: data.pest,     icon: Icons.bug_report,  color: const Color(0xFF854F0B), trend: '-5%',  trendUp: true),
                  _statCard(id: 'critical', label: 'Critical',    value: data.critical, icon: Icons.warning,     color: const Color(0xFF993C1D), trend: '+3',   trendUp: false),
                ],
              );
            }),
            const SizedBox(height: 24),

            // ── Findings Trend ─────────────────────────────────────────────
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text('Findings Trend', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                _chartToggle(),
              ],
            ),
            const SizedBox(height: 8),
            _trendLegend(),
            const SizedBox(height: 10),
            Container(
              height: 220,
              width: double.infinity,
              padding: const EdgeInsets.fromLTRB(8, 16, 16, 8),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(18),
              ),
              child: _chartType == 'Bar'
                  ? _buildBarChart(data)
                  : _buildLineChart(data),
            ),
            const SizedBox(height: 24),

            // ── Severity Pie Chart ─────────────────────────────────────────
            const Text('Severity Breakdown', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            _severitySection(data),
            const SizedBox(height: 24),

            // ── Top Problem Categories ─────────────────────────────────────
            const Text('Top Problem Categories', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            _categoryTile('Disease',      42, const Color(0xFFE24B4A), '+4%',  false),
            _categoryTile('Pests',        28, const Color(0xFFEF9F27), '-2%',  true),
            _categoryTile('Water Stress', 15, const Color(0xFF378ADD), '0%',   true),
            _categoryTile('Nutrition',    10, const Color(0xFF639922), '-1%',  true),
            _categoryTile('Other',         5, Colors.grey,             '—',    true),
            const SizedBox(height: 24),

            // ── Top Greenhouses ────────────────────────────────────────────
            const Text('Top Greenhouses by Findings', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            _topGreenhousesSection(data),
            const SizedBox(height: 24),

            // ── Recent Inspections ─────────────────────────────────────────
            Row(
              children: [
                const Text('Recent Inspections', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                if (_activeStatFilter != 'all') ...[
                  const SizedBox(width: 8),
                  _chip(_typeLabel(_activeStatFilter), const Color(0xFF185FA5), const Color(0xFFE6F1FB)),
                ],
              ],
            ),
            const SizedBox(height: 10),
            _inspectionList(),
            const SizedBox(height: 32),
          ],
        ),
      ),
    );
  }

  // ─────────────────────────────────────────────────────────────────────────
  // SECTION WIDGETS
  // ─────────────────────────────────────────────────────────────────────────

  Widget _aiInsightBox(_PeriodData data) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: const Color(0xFFE6F1FB),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: const Color(0xFFB5D4F4)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: const [
              Icon(Icons.lightbulb_outline, color: Color(0xFF185FA5), size: 18),
              SizedBox(width: 6),
              Text('AI Insight', style: TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF0C447C), fontSize: 13)),
            ],
          ),
          const SizedBox(height: 6),
          Text(data.aiInsight, style: const TextStyle(fontSize: 13, color: Color(0xFF185FA5), height: 1.5)),
          const SizedBox(height: 10),
          const Divider(color: Color(0xFFB5D4F4), height: 1),
          const SizedBox(height: 10),
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Icon(Icons.recommend, color: Color(0xFF185FA5), size: 18),
              const SizedBox(width: 6),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('Recommendation', style: TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF0C447C), fontSize: 13)),
                    const SizedBox(height: 4),
                    Text(data.aiRecommendation, style: const TextStyle(fontSize: 13, color: Color(0xFF185FA5), height: 1.5)),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

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
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
      ),
      child: Row(
        children: [
          SizedBox(
            width: 130,
            height: 130,
            child: PieChart(
              PieChartData(
                sections: sections,
                sectionsSpace: 2,
                centerSpaceRadius: 30,
                borderData: FlBorderData(show: false),
              ),
            ),
          ),
          const SizedBox(width: 20),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: labels.map((l) {
                return Padding(
                  padding: const EdgeInsets.symmetric(vertical: 5),
                  child: Row(
                    children: [
                      Container(width: 10, height: 10, decoration: BoxDecoration(color: l.$3, shape: BoxShape.circle)),
                      const SizedBox(width: 8),
                      Expanded(child: Text(l.$1, style: const TextStyle(fontSize: 13))),
                      Text(l.$2, style: TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: l.$3)),
                    ],
                  ),
                );
              }).toList(),
            ),
          ),
        ],
      ),
    );
  }

  Widget _topGreenhousesSection(_PeriodData data) {
    final maxFindings = data.topGreenhouses.fold(0, (m, g) => g.findings > m ? g.findings : m).toDouble();

    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
      ),
      child: Column(
        children: data.topGreenhouses.asMap().entries.map((entry) {
          final rank = entry.key + 1;
          final gh = entry.value;
          final pct = maxFindings > 0 ? gh.findings / maxFindings : 0.0;
          final medalColors = [const Color(0xFFBA7517), const Color(0xFF888780), const Color(0xFF854F0B)];
          final issueColor = _typeColor(gh.topIssue.toLowerCase().replaceAll(' stress', ''));

          return Column(
            children: [
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                child: Row(
                  children: [
                    Container(
                      width: 26,
                      height: 26,
                      decoration: BoxDecoration(
                        color: medalColors[rank - 1].withValues(alpha: 0.12),
                        shape: BoxShape.circle,
                      ),
                      child: Center(
                        child: Text(
                          '#$rank',
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.bold,
                            color: medalColors[rank - 1],
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(gh.gh, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                          const SizedBox(height: 4),
                          ClipRRect(
                            borderRadius: BorderRadius.circular(4),
                            child: LinearProgressIndicator(
                              value: pct,
                              minHeight: 5,
                              backgroundColor: Colors.grey.shade100,
                              valueColor: AlwaysStoppedAnimation<Color>(issueColor),
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(width: 12),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        Text('${gh.findings}', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                        const SizedBox(height: 2),
                        _chip(gh.topIssue, issueColor, issueColor.withValues(alpha: 0.1)),
                      ],
                    ),
                  ],
                ),
              ),
              if (rank < data.topGreenhouses.length)
                const Divider(height: 1, indent: 16, endIndent: 16),
            ],
          );
        }).toList(),
      ),
    );
  }

  Widget _inspectionList() {
    final rows = _filteredInspections;
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
      ),
      child: rows.isEmpty
          ? const Padding(
              padding: EdgeInsets.all(20),
              child: Text('No inspections match this filter.', style: TextStyle(color: Colors.grey)),
            )
          : Column(
              children: rows.asMap().entries.map((entry) {
                final i = entry.key;
                final r = entry.value;
                return Column(
                  children: [
                    ListTile(
                      onTap: () => ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text('Opening: ${r.date} · ${r.gh} · ${r.variety}'),
                          behavior: SnackBarBehavior.floating,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                        ),
                      ),
                      title: Text(
                        '${r.date} · ${r.gh} · ${r.variety}',
                        style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13),
                      ),
                      subtitle: Padding(
                        padding: const EdgeInsets.only(top: 4),
                        child: Wrap(
                          spacing: 6,
                          runSpacing: 4,
                          children: [
                            _chip(_typeLabel(r.type), _typeColor(r.type), _typeColor(r.type).withValues(alpha: 0.1)),
                            _chip(
                              r.severity[0].toUpperCase() + r.severity.substring(1),
                              _severityColor(r.severity),
                              _severityColor(r.severity).withValues(alpha: 0.1),
                            ),
                            Text(r.inspector, style: const TextStyle(fontSize: 12, color: Colors.grey)),
                          ],
                        ),
                      ),
                      trailing: const Icon(Icons.chevron_right, color: Colors.grey, size: 18),
                    ),
                    if (i < rows.length - 1)
                      const Divider(height: 1, indent: 16, endIndent: 16),
                  ],
                );
              }).toList(),
            ),
    );
  }

  // ─────────────────────────────────────────────────────────────────────────
  // CHARTS
  // ─────────────────────────────────────────────────────────────────────────

  Widget _buildBarChart(_PeriodData data) {
    final labels = data.chartLabels;
    final disease = data.trendDisease;
    final pest = data.trendPest;
    final water = data.trendWater;
    final maxY = disease.reduce((a, b) => a > b ? a : b) * 1.25;
    final count = labels.length;

    return BarChart(BarChartData(
      alignment: BarChartAlignment.spaceAround,
      maxY: maxY,
      barTouchData: BarTouchData(
        touchTooltipData: BarTouchTooltipData(
          getTooltipItem: (group, groupIndex, rod, rodIndex) {
            final names = ['Disease', 'Pests', 'Water'];
            return BarTooltipItem(
              '${names[rodIndex]}: ${rod.toY.toInt()}',
              const TextStyle(color: Colors.white, fontSize: 11),
            );
          },
        ),
      ),
      titlesData: FlTitlesData(
        leftTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
        rightTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
        topTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
        bottomTitles: AxisTitles(
          sideTitles: SideTitles(
            showTitles: true,
            reservedSize: 28,
            getTitlesWidget: (value, meta) {
              final idx = value.toInt();
              if (idx < 0 || idx >= count) return const SizedBox();
              return Padding(
                padding: const EdgeInsets.only(top: 6),
                child: Text(labels[idx], style: const TextStyle(fontSize: 10, color: Colors.grey)),
              );
            },
          ),
        ),
      ),
      gridData: FlGridData(
        drawVerticalLine: false,
        getDrawingHorizontalLine: (_) => FlLine(color: Colors.grey.shade100, strokeWidth: 1),
      ),
      borderData: FlBorderData(show: false),
      barGroups: List.generate(count, (i) => BarChartGroupData(
        x: i,
        barRods: [
          BarChartRodData(toY: disease[i], color: const Color(0xFF3B6D11), width: 5, borderRadius: BorderRadius.circular(4)),
          BarChartRodData(toY: pest[i],    color: const Color(0xFFEF9F27), width: 5, borderRadius: BorderRadius.circular(4)),
          BarChartRodData(toY: water[i],   color: const Color(0xFF378ADD), width: 5, borderRadius: BorderRadius.circular(4)),
        ],
      )),
    ));
  }

  Widget _buildLineChart(_PeriodData data) {
    final labels = data.chartLabels;
    final disease = data.trendDisease;
    final pest = data.trendPest;
    final water = data.trendWater;
    final maxY = disease.reduce((a, b) => a > b ? a : b) * 1.25;
    final count = labels.length;

    LineChartBarData _series(List<double> vals, Color color) => LineChartBarData(
      spots: vals.asMap().entries.map((e) => FlSpot(e.key.toDouble(), e.value)).toList(),
      isCurved: true,
      color: color,
      barWidth: 2.5,
      dotData: const FlDotData(show: true),
      belowBarData: BarAreaData(show: false),
    );

    return LineChart(LineChartData(
      minY: 0,
      maxY: maxY,
      lineTouchData: LineTouchData(
        touchTooltipData: LineTouchTooltipData(
          getTooltipItems: (spots) => spots.map((s) {
            final names = ['Disease', 'Pests', 'Water'];
            return LineTooltipItem(
              '${names[s.barIndex]}: ${s.y.toInt()}',
              const TextStyle(color: Colors.white, fontSize: 11),
            );
          }).toList(),
        ),
      ),
      titlesData: FlTitlesData(
        leftTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
        rightTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
        topTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
        bottomTitles: AxisTitles(
          sideTitles: SideTitles(
            showTitles: true,
            reservedSize: 28,
            getTitlesWidget: (value, meta) {
              final idx = value.toInt();
              if (idx < 0 || idx >= count) return const SizedBox();
              return Padding(
                padding: const EdgeInsets.only(top: 6),
                child: Text(labels[idx], style: const TextStyle(fontSize: 10, color: Colors.grey)),
              );
            },
          ),
        ),
      ),
      gridData: FlGridData(
        drawVerticalLine: false,
        getDrawingHorizontalLine: (_) => FlLine(color: Colors.grey.shade100, strokeWidth: 1),
      ),
      borderData: FlBorderData(show: false),
      lineBarsData: [
        _series(disease, const Color(0xFF3B6D11)),
        _series(pest,    const Color(0xFFEF9F27)),
        _series(water,   const Color(0xFF378ADD)),
      ],
    ));
  }

  // ─────────────────────────────────────────────────────────────────────────
  // REUSABLE WIDGETS
  // ─────────────────────────────────────────────────────────────────────────

  Widget _exportButton({
    required IconData icon,
    required String label,
    required Color color,
    required VoidCallback onTap,
  }) {
    return Material(
      color: Colors.white,
      borderRadius: BorderRadius.circular(14),
      child: InkWell(
        borderRadius: BorderRadius.circular(14),
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 14),
          decoration: BoxDecoration(
            border: Border.all(color: color.withValues(alpha: 0.3)),
            borderRadius: BorderRadius.circular(14),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, color: color, size: 20),
              const SizedBox(width: 8),
              Text(label, style: TextStyle(fontWeight: FontWeight.w600, color: color, fontSize: 14)),
            ],
          ),
        ),
      ),
    );
  }

  Widget _dropdown({
    required String label,
    required String value,
    required List<String> items,
    required ValueChanged<String?> onChanged,
  }) {
    return SizedBox(
      width: 190,
      child: DropdownButtonFormField<String>(
        value: value,
        decoration: InputDecoration(
          labelText: label,
          border: const OutlineInputBorder(),
          contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
        ),
        items: items.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
        onChanged: onChanged,
      ),
    );
  }

  Widget _statCard({
    required String id,
    required String label,
    required int value,
    required IconData icon,
    required Color color,
    required String trend,
    required bool trendUp,
  }) {
    final isActive = _activeStatFilter == id;
    return GestureDetector(
      onTap: () => setState(() => _activeStatFilter = id),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          border: isActive
              ? Border.all(color: const Color(0xFF185FA5), width: 2)
              : Border.all(color: Colors.grey.shade200),
        ),
        padding: const EdgeInsets.all(12),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 26, color: color),
            const SizedBox(height: 6),
            Text('$value', style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
            const SizedBox(height: 2),
            Text(label, style: const TextStyle(fontSize: 11, color: Colors.grey)),
            const SizedBox(height: 4),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 2),
              decoration: BoxDecoration(
                color: trendUp ? Colors.green.shade50 : Colors.red.shade50,
                borderRadius: BorderRadius.circular(20),
              ),
              child: Text(
                trend,
                style: TextStyle(
                  fontSize: 10,
                  fontWeight: FontWeight.bold,
                  color: trendUp ? const Color(0xFF3B6D11) : const Color(0xFFA32D2D),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _chartToggle() {
    return Row(
      children: ['Bar', 'Line'].map((type) {
        final active = _chartType == type;
        return GestureDetector(
          onTap: () => setState(() => _chartType = type),
          child: Container(
            margin: const EdgeInsets.only(left: 6),
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 5),
            decoration: BoxDecoration(
              color: active ? const Color(0xFF185FA5) : Colors.transparent,
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: active ? const Color(0xFF185FA5) : Colors.grey.shade300),
            ),
            child: Text(
              type,
              style: TextStyle(
                fontSize: 12,
                color: active ? Colors.white : Colors.grey.shade600,
                fontWeight: active ? FontWeight.bold : FontWeight.normal,
              ),
            ),
          ),
        );
      }).toList(),
    );
  }

  Widget _trendLegend() {
    final items = [
      ('Disease',      const Color(0xFF3B6D11)),
      ('Pests',        const Color(0xFFEF9F27)),
      ('Water Stress', const Color(0xFF378ADD)),
    ];
    return Wrap(
      spacing: 14,
      children: items.map((item) => Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(width: 10, height: 10, decoration: BoxDecoration(color: item.$2, borderRadius: BorderRadius.circular(2))),
          const SizedBox(width: 4),
          Text(item.$1, style: const TextStyle(fontSize: 12, color: Colors.grey)),
        ],
      )).toList(),
    );
  }

  Widget _categoryTile(String title, int pct, Color color, String delta, bool improved) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
        child: Row(
          children: [
            Container(width: 10, height: 10, decoration: BoxDecoration(color: color, shape: BoxShape.circle)),
            const SizedBox(width: 10),
            Expanded(child: Text(title, style: const TextStyle(fontSize: 13))),
            SizedBox(
              width: 110,
              child: ClipRRect(
                borderRadius: BorderRadius.circular(4),
                child: LinearProgressIndicator(
                  value: pct / 100,
                  backgroundColor: Colors.grey.shade100,
                  valueColor: AlwaysStoppedAnimation<Color>(color),
                  minHeight: 6,
                ),
              ),
            ),
            const SizedBox(width: 10),
            SizedBox(
              width: 32,
              child: Text('$pct%', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13), textAlign: TextAlign.right),
            ),
            const SizedBox(width: 8),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 2),
              decoration: BoxDecoration(
                color: delta == '—' ? Colors.grey.shade100 : improved ? Colors.green.shade50 : Colors.red.shade50,
                borderRadius: BorderRadius.circular(20),
              ),
              child: Text(
                delta,
                style: TextStyle(
                  fontSize: 10,
                  fontWeight: FontWeight.bold,
                  color: delta == '—' ? Colors.grey : improved ? const Color(0xFF3B6D11) : const Color(0xFFA32D2D),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _chip(String label, Color textColor, Color bgColor) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
      decoration: BoxDecoration(color: bgColor, borderRadius: BorderRadius.circular(20)),
      child: Text(label, style: TextStyle(fontSize: 11, color: textColor, fontWeight: FontWeight.w600)),
    );
  }
}
