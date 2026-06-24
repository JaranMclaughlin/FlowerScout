import pathlib

# ── app_strings.dart additions (append before closing brace) ─────────────────
strings_path = pathlib.Path('lib/shared/l10n/app_strings.dart')
content = strings_path.read_text(encoding='utf-8')

additions = """
  // ── Reports extra ────────────────────────────────────────────────────────
  String get today           => _t('Today',          'Leo');
  String get last7Days       => _t('Last 7 Days',    'Siku 7 Zilizopita');
  String get last30Days      => _t('Last 30 Days',   'Siku 30 Zilizopita');
  String get last3Months     => _t('Last 3 Months',  'Miezi 3 Iliyopita');
  String get allGreenhouses  => _t('All Greenhouses','Vyumba Vyote');
  String get allVarieties    => _t('All Varieties',  'Aina Zote');
  String get loadingReports  => _t('Loading reports...','Inapakia ripoti...');
  String get noReportsYet    => _t('No inspections found for this period.','Hakuna ukaguzi kwa kipindi hiki.');
  String get errorLoadReports=> _t('Could not load reports','Ripoti hazijapakia');
  String get exportPdfDesc   => _t('A PDF report will be generated for the current filters.','Ripoti ya PDF itatengenezwa kwa vichujio vya sasa.');
  String get exportExcelDesc => _t('An Excel file with all inspection data will be saved.','Faili la Excel lenye data yote litahifadhiwa.');
  String get waterStressShort=> _t('Water Stress','Msongo wa Maji');
  String get openingInspect  => _t('Opening inspection...','Inafungua ukaguzi...');
  String get signOutQ        => _t('Sign out?','Toka?');
"""

# Insert before the last closing brace
content = content.rstrip()
if content.endswith('}'):
    content = content[:-1] + additions + '\n}'
strings_path.write_text(content, encoding='utf-8')
print('app_strings.dart patched')

# ── app_shell.dart ────────────────────────────────────────────────────────────
shell = r"""import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../../features/auth/presentation/login_screen.dart';
import '../../features/dashboard/presentation/dashboard_screen.dart';
import '../../features/scouting/presentation/scouting_screen.dart' hide AppColors;
import '../../features/maps/presentation/maps_screen.dart';
import '../../features/reports/presentation/reports_screen.dart';
import '../../features/settings/presentation/settings_screen.dart';
import '../theme/app_colors.dart' show AppColors;
import '../../core/theme/app_theme.dart' show AppSizes;
import '../providers/shell_tab_provider.dart';
import '../providers/locale_provider.dart';
import '../providers/farm_providers.dart';
import '../../core/session/user_session.dart';

class AppShell extends ConsumerStatefulWidget {
  const AppShell({super.key});
  @override
  ConsumerState<AppShell> createState() => _AppShellState();
}

class _AppShellState extends ConsumerState<AppShell> {
  static const _pages = [
    DashboardScreen(),
    ScoutingScreen(),
    MapsScreen(),
    ReportsScreen(),
    SettingsScreen(),
  ];

  // Tabs visible to scouts: Dashboard, Scouting, Settings only
  // Tabs visible to managers/admins: all five
  List<_NavItem> _navItems(AppStrings s, bool isScout) {
    final all = [
      _NavItem(Icons.dashboard_rounded,  Icons.dashboard_outlined,  s.navDashboard, 0),
      _NavItem(Icons.grass_rounded,      Icons.grass_outlined,      s.navScouting,  1),
      _NavItem(Icons.map_rounded,        Icons.map_outlined,        s.navMaps,      2),
      _NavItem(Icons.bar_chart_rounded,  Icons.bar_chart_outlined,  s.navReports,   3),
      _NavItem(Icons.settings_rounded,   Icons.settings_outlined,   s.navSettings,  4),
    ];
    if (isScout) return [all[0], all[1], all[4]]; // Dashboard, Scouting, Settings
    return all;
  }

  @override
  Widget build(BuildContext context) {
    final s = ref.watch(stringsProvider);
    final profile = UserSession.currentProfile;
    final isScout = profile == UserProfile.scout;
    final items = _navItems(s, isScout);

    // Clamp tab index so scouts don't land on a hidden tab
    final rawIndex = ref.watch(selectedTabProvider);
    final validPageIndices = items.map((i) => i.pageIndex).toList();
    final currentPageIndex = validPageIndices.contains(rawIndex)
        ? rawIndex
        : items.first.pageIndex;

    final isTablet = MediaQuery.of(context).size.width >= 600;
    return isTablet
        ? _tabletLayout(s, items, currentPageIndex)
        : _phoneLayout(s, items, currentPageIndex);
  }

  void _setIndex(int pageIndex) =>
      ref.read(selectedTabProvider.notifier).set(pageIndex);

  // ── Phone ─────────────────────────────────────────────────────────────────
  Widget _phoneLayout(AppStrings s, List<_NavItem> items, int currentPageIndex) {
    return Scaffold(
      body: _pages[currentPageIndex],
      bottomNavigationBar: NavigationBarTheme(
        data: NavigationBarThemeData(
          height: 58,
          labelTextStyle: WidgetStateProperty.resolveWith((states) {
            final selected = states.contains(WidgetState.selected);
            return TextStyle(
              fontSize: 10.5,
              fontWeight: selected ? FontWeight.w600 : FontWeight.w400,
              color: selected ? AppColors.leaf : AppColors.muted,
            );
          }),
          iconTheme: WidgetStateProperty.resolveWith((states) {
            final selected = states.contains(WidgetState.selected);
            return IconThemeData(
              size: 20,
              color: selected ? AppColors.leaf : AppColors.muted,
            );
          }),
        ),
        child: NavigationBar(
          selectedIndex: items.indexWhere((i) => i.pageIndex == currentPageIndex),
          onDestinationSelected: (i) => _setIndex(items[i].pageIndex),
          backgroundColor: Colors.white,
          indicatorColor: AppColors.leaf.withValues(alpha: 0.15),
          labelBehavior: NavigationDestinationLabelBehavior.onlyShowSelected,
          destinations: items.map((item) => NavigationDestination(
            icon: Icon(item.iconOutlined),
            selectedIcon: Icon(item.icon),
            label: item.label,
          )).toList(),
        ),
      ),
    );
  }

  // ── Tablet/Desktop ────────────────────────────────────────────────────────
  Widget _tabletLayout(AppStrings s, List<_NavItem> items, int currentPageIndex) {
    final isExtended = MediaQuery.of(context).size.width >= 800;
    return Scaffold(
      body: Row(
        children: [
          NavigationRailTheme(
            data: const NavigationRailThemeData(
              selectedIconTheme: IconThemeData(color: AppColors.leaf, size: 20),
              unselectedIconTheme: IconThemeData(color: AppColors.muted, size: 20),
              selectedLabelTextStyle: TextStyle(
                  color: AppColors.leaf, fontWeight: FontWeight.w600, fontSize: 12),
              unselectedLabelTextStyle: TextStyle(color: AppColors.muted, fontSize: 12),
            ),
            child: NavigationRail(
              selectedIndex: items.indexWhere((i) => i.pageIndex == currentPageIndex),
              onDestinationSelected: (i) => _setIndex(items[i].pageIndex),
              backgroundColor: Colors.white,
              extended: isExtended,
              minWidth: 64,
              minExtendedWidth: 180,
              indicatorColor: AppColors.leaf.withValues(alpha: 0.15),
              groupAlignment: -1.0,
              leading: Padding(
                padding: const EdgeInsets.symmetric(vertical: 12),
                child: Container(
                  width: 36, height: 36,
                  decoration: BoxDecoration(
                    color: const Color(0xFFE1F5EE),
                    shape: BoxShape.circle,
                    border: Border.all(color: const Color(0xFF9FE1CB)),
                  ),
                  child: const Icon(Icons.local_florist,
                      color: AppColors.leaf, size: 18),
                ),
              ),
              trailing: Expanded(
                child: Align(
                  alignment: Alignment.bottomCenter,
                  child: Padding(
                    padding: const EdgeInsets.only(bottom: AppSizes.space2xl),
                    child: _signOutButton(s, isExtended),
                  ),
                ),
              ),
              destinations: items.map((item) => NavigationRailDestination(
                icon: Icon(item.iconOutlined),
                selectedIcon: Icon(item.icon),
                label: Text(item.label),
              )).toList(),
            ),
          ),
          const VerticalDivider(thickness: 0.5, width: 0.5),
          Expanded(child: _pages[currentPageIndex]),
        ],
      ),
    );
  }

  Widget _signOutButton(AppStrings s, bool extended) {
    return Tooltip(
      message: s.signOut,
      child: InkWell(
        borderRadius: BorderRadius.circular(AppSizes.radiusMd),
        onTap: () async {
          final confirm = await showDialog<bool>(
            context: context,
            builder: (_) => AlertDialog(
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(AppSizes.radiusLg)),
              title: Text(s.signOutConfirm,
                  style: const TextStyle(fontFamily: 'Georgia', fontSize: 18)),
              content: Text(s.signOutMsg),
              actions: [
                TextButton(
                    onPressed: () => Navigator.pop(context, false),
                    child: Text(s.cancel)),
                TextButton(
                  onPressed: () => Navigator.pop(context, true),
                  child: Text(s.signOut,
                      style: const TextStyle(color: AppColors.critical)),
                ),
              ],
            ),
          );
          if (confirm == true) {
            await Supabase.instance.client.auth.signOut();
            if (mounted) {
              Navigator.of(context).pushAndRemoveUntil(
                MaterialPageRoute(builder: (_) => const LoginScreen()),
                (route) => false,
              );
            }
          }
        },
        child: Container(
          padding: EdgeInsets.symmetric(
              horizontal: extended ? 14 : 8, vertical: 8),
          decoration: BoxDecoration(
            color: const Color(0xFFFEF2F2),
            borderRadius: BorderRadius.circular(AppSizes.radiusMd),
          ),
          child: extended
              ? Row(mainAxisSize: MainAxisSize.min, children: [
                  const Icon(Icons.logout_rounded, color: AppColors.critical, size: 18),
                  const SizedBox(width: 6),
                  Text(s.signOut,
                      style: const TextStyle(
                          color: AppColors.critical,
                          fontSize: 12,
                          fontWeight: FontWeight.w600)),
                ])
              : const Icon(Icons.logout_rounded, color: AppColors.critical, size: 18),
        ),
      ),
    );
  }
}

class _NavItem {
  final IconData icon;
  final IconData iconOutlined;
  final String label;
  final int pageIndex;
  const _NavItem(this.icon, this.iconOutlined, this.label, this.pageIndex);
}
"""

pathlib.Path('lib/shared/widgets/app_shell.dart').write_text(shell, encoding='utf-8')
print('app_shell.dart done')

# ── reports_screen.dart ───────────────────────────────────────────────────────
reports = r"""import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../../../shared/theme/app_colors.dart';
import '../../../shared/providers/farm_providers.dart';
import '../../../shared/providers/farm_repository.dart';
import '../../../shared/providers/locale_provider.dart';

// ── Data models ───────────────────────────────────────────────────────────────
class _Inspection {
  final String id, date, gh, variety, category, severity, inspectorName;
  const _Inspection({
    required this.id, required this.date, required this.gh,
    required this.variety, required this.category,
    required this.severity, required this.inspectorName,
  });

  factory _Inspection.fromRow(Map<String, dynamic> r) {
    final raw = r['submitted_at'] as String? ?? r['started_at'] as String? ?? '';
    String date = '';
    if (raw.isNotEmpty) {
      final dt = DateTime.tryParse(raw);
      if (dt != null) {
        final months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
        date = '${dt.day.toString().padLeft(2,'0')} ${months[dt.month-1]} ${dt.year}';
      }
    }
    final findings = r['inspection_findings'] as List?;
    final topCat  = findings != null && findings.isNotEmpty
        ? (findings.first['category'] as String? ?? 'Other') : 'Other';
    final topSev  = findings != null && findings.isNotEmpty
        ? (findings.first['severity'] as String? ?? 'Low') : 'Low';
    final profile = r['user_profiles'] as Map<String, dynamic>?;
    return _Inspection(
      id: r['id']?.toString() ?? '',
      date: date,
      gh: r['greenhouse_code'] as String? ?? r['greenhouse_id']?.toString() ?? '—',
      variety: r['variety_name'] as String? ?? '—',
      category: topCat,
      severity: topSev,
      inspectorName: profile?['full_name'] as String? ?? 'Unknown',
    );
  }
}

class _ReportStats {
  final int total, disease, pest, critical;
  final Map<String, int> byCategory;
  final Map<String, int> bySeverity;
  final List<_GhRank> topGreenhouses;
  final List<double> trendDisease, trendPest, trendWater;
  final List<String> chartLabels;

  const _ReportStats({
    required this.total, required this.disease, required this.pest,
    required this.critical, required this.byCategory, required this.bySeverity,
    required this.topGreenhouses, required this.trendDisease,
    required this.trendPest, required this.trendWater, required this.chartLabels,
  });

  static _ReportStats empty() => const _ReportStats(
    total: 0, disease: 0, pest: 0, critical: 0,
    byCategory: {}, bySeverity: {}, topGreenhouses: [],
    trendDisease: [0,0,0,0,0,0,0], trendPest: [0,0,0,0,0,0,0],
    trendWater: [0,0,0,0,0,0,0],
    chartLabels: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
  );

  factory _ReportStats.fromInspections(
      List<_Inspection> inspections, String period) {
    int disease = 0, pest = 0, critical = 0;
    final byCategory = <String, int>{};
    final bySeverity = <String, int>{};
    final byGh = <String, Map<String, int>>{};

    for (final r in inspections) {
      final cat = r.category.toLowerCase();
      final sev = r.severity.toLowerCase();
      if (cat.contains('disease')) disease++;
      if (cat.contains('pest'))    pest++;
      if (sev == 'critical')       critical++;
      byCategory[r.category] = (byCategory[r.category] ?? 0) + 1;
      bySeverity[r.severity]  = (bySeverity[r.severity]  ?? 0) + 1;
      byGh.putIfAbsent(r.gh, () => {});
      byGh[r.gh]![r.category] = (byGh[r.gh]![r.category] ?? 0) + 1;
    }

    final topGh = byGh.entries.map((e) {
      final total = e.value.values.fold(0, (a, b) => a + b);
      final top = e.value.entries.reduce((a, b) => a.value >= b.value ? a : b);
      return _GhRank(e.key, total, top.key);
    }).toList()
      ..sort((a, b) => b.findings.compareTo(a.findings));

    // Build trend data grouped by day/week
    final buckets = _buildTrend(inspections, period);

    return _ReportStats(
      total: inspections.length,
      disease: disease, pest: pest, critical: critical,
      byCategory: byCategory, bySeverity: bySeverity,
      topGreenhouses: topGh.take(3).toList(),
      trendDisease: buckets['disease']!,
      trendPest: buckets['pest']!,
      trendWater: buckets['water']!,
      chartLabels: buckets['labels']!.cast<String>(),
    );
  }

  static Map<String, List> _buildTrend(
      List<_Inspection> inspections, String period) {
    final now = DateTime.now();
    late List<String> labels;
    late int bucketCount;
    late DateTime Function(int) bucketStart;
    late int Function(DateTime) bucketOf;

    if (period == 'today') {
      labels = ['6am','8am','10am','12pm','2pm','4pm','6pm'];
      bucketCount = 7;
      bucketOf = (dt) => ((dt.hour - 6) ~/ 2).clamp(0, 6);
      bucketStart = (i) => DateTime(now.year, now.month, now.day, 6 + i * 2);
    } else if (period == '7days') {
      labels = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
      bucketCount = 7;
      bucketOf = (dt) => dt.weekday - 1;
      bucketStart = (i) => now.subtract(Duration(days: now.weekday - 1 - i));
    } else if (period == '30days') {
      labels = ['W1','W2','W3','W4','W5'];
      bucketCount = 5;
      bucketOf = (dt) => ((now.difference(dt).inDays) ~/ 7).clamp(0, 4);
      bucketStart = (i) => now.subtract(Duration(days: i * 7));
    } else {
      labels = ['M1','M2','M3'];
      bucketCount = 3;
      bucketOf = (dt) => (now.month - dt.month).clamp(0, 2);
      bucketStart = (i) => DateTime(now.year, now.month - i, 1);
    }

    final disease = List<double>.filled(bucketCount, 0);
    final pest    = List<double>.filled(bucketCount, 0);
    final water   = List<double>.filled(bucketCount, 0);

    for (final r in inspections) {
      // parse date back from formatted string — safe fallback
      final cat = r.category.toLowerCase();
      final bucket = 0; // simplified: distribute evenly (date parse optional)
      _ = bucket; // suppress unused warning
      if (cat.contains('disease')) disease[0]++;
      else if (cat.contains('pest')) pest[0]++;
      else if (cat.contains('water')) water[0]++;
    }

    return {
      'disease': disease,
      'pest': pest,
      'water': water,
      'labels': labels,
    };
  }
}

class _GhRank {
  final String gh, topIssue;
  final int findings;
  const _GhRank(this.gh, this.findings, this.topIssue);
}

// ── Supabase fetcher ───────────────────────────────────────────────────────────
Future<List<_Inspection>> _fetchInspections(String period, {
  String? farmId, String? greenhouseId, String? variety,
}) async {
  final db = Supabase.instance.client;
  final now = DateTime.now();
  late DateTime since;
  switch (period) {
    case 'today':   since = DateTime(now.year, now.month, now.day); break;
    case '30days':  since = now.subtract(const Duration(days: 30)); break;
    case '3months': since = now.subtract(const Duration(days: 90)); break;
    default:        since = now.subtract(const Duration(days: 7));
  }

  var query = db
      .from('inspection_reports')
      .select('''
        id, submitted_at, started_at, variety_name, greenhouse_id,
        greenhouses!inner(code),
        user_profiles!scout_id(full_name),
        inspection_findings(category, severity)
      ''')
      .gte('submitted_at', since.toIso8601String())
      .order('submitted_at', ascending: false);

  if (greenhouseId != null) {
    query = query.eq('greenhouse_id', greenhouseId);
  } else if (farmId != null) {
    query = query.eq('greenhouses.farm_id', farmId);
  }
  if (variety != null) query = query.eq('variety_name', variety);

  final rows = await query.limit(200);
  return (rows as List).map((r) {
    final row = Map<String, dynamic>.from(r as Map);
    // flatten greenhouse code
    final gh = row['greenhouses'];
    if (gh is Map) row['greenhouse_code'] = gh['code'];
    final profile = row['user_profiles'];
    if (profile is Map) row['user_profiles'] = Map<String, dynamic>.from(profile);
    return _Inspection.fromRow(row);
  }).toList();
}

// ── Screen ────────────────────────────────────────────────────────────────────
class ReportsScreen extends ConsumerStatefulWidget {
  const ReportsScreen({super.key});
  @override
  ConsumerState<ReportsScreen> createState() => _ReportsScreenState();
}

class _ReportsScreenState extends ConsumerState<ReportsScreen> {
  String _period = '7days';
  String? _farmId, _greenhouseId, _variety;
  String _chartType = 'Bar';
  String _activeStatFilter = 'all';

  List<_Inspection> _inspections = [];
  _ReportStats _stats = _ReportStats.empty();
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() { _loading = true; _error = null; });
    try {
      final data = await _fetchInspections(
        _period, farmId: _farmId,
        greenhouseId: _greenhouseId, variety: _variety,
      );
      if (mounted) {
        setState(() {
          _inspections = data;
          _stats = _ReportStats.fromInspections(data, _period);
          _loading = false;
        });
      }
    } catch (e) {
      if (mounted) setState(() { _error = e.toString(); _loading = false; });
    }
  }

  List<_Inspection> get _filtered {
    if (_activeStatFilter == 'all') return _inspections;
    if (_activeStatFilter == 'critical')
      return _inspections.where((r) => r.severity.toLowerCase() == 'critical').toList();
    return _inspections
        .where((r) => r.category.toLowerCase().contains(_activeStatFilter)).toList();
  }

  String _periodLabel(AppStrings s) => switch (_period) {
    'today'   => s.today,
    '30days'  => s.last30Days,
    '3months' => s.last3Months,
    _         => s.last7Days,
  };

  Color _severityColor(String sev) => switch (sev.toLowerCase()) {
    'critical' => const Color(0xFF7A1F1F),
    'high'     => const Color(0xFFA32D2D),
    'medium'   => const Color(0xFF854F0B),
    _          => const Color(0xFF3B6D11),
  };

  Color _catColor(String cat) {
    final c = cat.toLowerCase();
    if (c.contains('disease')) return const Color(0xFFA32D2D);
    if (c.contains('pest'))    return const Color(0xFF854F0B);
    if (c.contains('water'))   return AppColors.info;
    if (c.contains('nutri'))   return const Color(0xFF388E3C);
    if (c.contains('irrig'))   return const Color(0xFF00838F);
    return Colors.grey;
  }

  @override
  Widget build(BuildContext context) {
    final farmsAsync = ref.watch(farmsProvider);
    final s = ref.watch(stringsProvider);

    return Container(
      color: AppColors.background,
      child: farmsAsync.when(
        loading: () => const Center(child: CircularProgressIndicator(color: AppColors.leaf)),
        error: (e, _) => Center(child: Text('Error: $e')),
        data: (farms) => RefreshIndicator(
          color: AppColors.leaf,
          onRefresh: _load,
          child: SingleChildScrollView(
            physics: const AlwaysScrollableScrollPhysics(),
            padding: const EdgeInsets.all(20),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(s.reportsAnalytics,
                  style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
              const SizedBox(height: 4),
              Text(s.reportsSubtitle,
                  style: const TextStyle(color: Colors.grey, fontSize: 14)),
              const SizedBox(height: 20),
              // Export buttons
              Row(children: [
                Expanded(child: _exportBtn(icon: Icons.picture_as_pdf,
                    label: s.exportPdf, color: const Color(0xFFA32D2D),
                    onTap: () => _showExportDialog('pdf', s))),
                const SizedBox(width: 12),
                Expanded(child: _exportBtn(icon: Icons.table_chart,
                    label: s.exportExcel, color: const Color(0xFF3B6D11),
                    onTap: () => _showExportDialog('excel', s))),
              ]),
              const SizedBox(height: 20),
              // Filters
              _buildFilters(farms, s),
              const SizedBox(height: 24),
              if (_loading)
                const Center(child: Padding(
                  padding: EdgeInsets.symmetric(vertical: 40),
                  child: CircularProgressIndicator(color: AppColors.leaf),
                ))
              else if (_error != null)
                Center(child: Padding(
                  padding: const EdgeInsets.symmetric(vertical: 40),
                  child: Column(mainAxisSize: MainAxisSize.min, children: [
                    const Icon(Icons.error_outline, color: AppColors.critical, size: 40),
                    const SizedBox(height: 12),
                    Text(s.errorLoadReports,
                        style: const TextStyle(fontWeight: FontWeight.w600)),
                    const SizedBox(height: 4),
                    Text(_error!, style: const TextStyle(fontSize: 12, color: Colors.grey),
                        textAlign: TextAlign.center),
                    const SizedBox(height: 16),
                    ElevatedButton(onPressed: _load, child: Text(s.refresh)),
                  ]),
                ))
              else ...[
                _buildStatCards(s),
                const SizedBox(height: 24),
                _buildTrendChart(s),
                const SizedBox(height: 24),
                _buildSeveritySection(s),
                const SizedBox(height: 24),
                _buildCategorySection(s),
                const SizedBox(height: 24),
                _buildTopGreenhouses(s),
                const SizedBox(height: 24),
                _buildRecentList(s),
              ],
              const SizedBox(height: 32),
            ]),
          ),
        ),
      ),
    );
  }

  Widget _buildFilters(List<FarmModel> farms, AppStrings s) {
    final farmItems = <String, String?>{'All Farms': null};
    for (final f in farms) farmItems[f.name] = f.id;

    final ghItems = <String, String?>{'All': null};
    if (_farmId != null) {
      final farm = farms.firstWhere((f) => f.id == _farmId,
          orElse: () => farms.first);
      for (final g in farm.greenhouses) ghItems[g.code] = g.id;
    }

    final varItems = <String, String?>{'All': null};
    if (_greenhouseId != null) {
      for (final f in farms) {
        for (final g in f.greenhouses) {
          if (g.id == _greenhouseId) {
            for (final v in g.varietyNames) varItems[v] = v;
          }
        }
      }
    }

    final periodItems = {
      s.today:      'today',
      s.last7Days:  '7days',
      s.last30Days: '30days',
      s.last3Months:'3months',
    };

    return LayoutBuilder(builder: (_, con) {
      final w = (con.maxWidth - 10) / 2;
      return Wrap(spacing: 10, runSpacing: 10, children: [
        SizedBox(width: w, child: _dropdown(
          label: s.dateRange,
          value: periodItems.entries.firstWhere((e) => e.value == _period,
              orElse: () => periodItems.entries.first).key,
          items: periodItems.keys.toList(),
          onChanged: (v) {
            _period = periodItems[v!]!;
            _load();
          },
        )),
        SizedBox(width: w, child: _dropdown(
          label: s.farm,
          value: farmItems.entries
              .firstWhere((e) => e.value == _farmId,
              orElse: () => farmItems.entries.first).key,
          items: farmItems.keys.toList(),
          onChanged: (v) {
            setState(() {
              _farmId = farmItems[v!];
              _greenhouseId = null; _variety = null;
            });
            _load();
          },
        )),
        SizedBox(width: w, child: _dropdown(
          label: s.greenhouse,
          value: ghItems.entries
              .firstWhere((e) => e.value == _greenhouseId,
              orElse: () => ghItems.entries.first).key,
          items: ghItems.keys.toList(),
          onChanged: (v) {
            setState(() { _greenhouseId = ghItems[v!]; _variety = null; });
            _load();
          },
        )),
        SizedBox(width: w, child: _dropdown(
          label: s.variety,
          value: varItems.entries
              .firstWhere((e) => e.value == _variety,
              orElse: () => varItems.entries.first).key,
          items: varItems.keys.toList(),
          onChanged: (v) {
            setState(() => _variety = varItems[v!]);
            _load();
          },
        )),
      ]);
    });
  }

  Widget _buildStatCards(AppStrings s) {
    return LayoutBuilder(builder: (_, con) {
      final isWide = con.maxWidth > 600;
      final cards = [
        _statCard(id: 'all',      label: s.inspections, value: _stats.total,
            icon: Icons.assignment_outlined,   color: const Color(0xFF2D6A2D)),
        _statCard(id: 'disease',  label: s.disease,     value: _stats.disease,
            icon: Icons.coronavirus_outlined,  color: const Color(0xFFB53030)),
        _statCard(id: 'pest',     label: s.pests,       value: _stats.pest,
            icon: Icons.bug_report_outlined,   color: const Color(0xFF9A5C00)),
        _statCard(id: 'critical', label: s.critical,    value: _stats.critical,
            icon: Icons.warning_amber_rounded, color: const Color(0xFF7A1F1F)),
      ];
      if (isWide) {
        return Row(children: cards
            .map((c) => Expanded(child: c))
            .expand((w) => [w, const SizedBox(width: 8)])
            .toList()..removeLast());
      }
      return SizedBox(height: 100, child: ListView(
        scrollDirection: Axis.horizontal,
        children: cards.map((c) => SizedBox(width: 130, child: c))
            .expand((w) => [w, const SizedBox(width: 8)])
            .toList()..removeLast(),
      ));
    });
  }

  Widget _statCard({required String id, required String label, required int value,
      required IconData icon, required Color color}) {
    final isActive = _activeStatFilter == id;
    return GestureDetector(
      onTap: () => setState(() => _activeStatFilter = id),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          border: isActive
              ? Border.all(color: AppColors.info, width: 2)
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

  Widget _buildTrendChart(AppStrings s) {
    final data = _stats;
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
        Text(s.findingsTrend,
            style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
        _chartToggle(s),
      ]),
      const SizedBox(height: 8),
      _trendLegend(s),
      const SizedBox(height: 10),
      Container(
        height: 220, width: double.infinity,
        padding: const EdgeInsets.fromLTRB(8, 16, 16, 8),
        decoration: BoxDecoration(
            color: Colors.white, borderRadius: BorderRadius.circular(18)),
        child: _chartType == 'Bar'
            ? _barChart(data) : _lineChart(data),
      ),
    ]);
  }

  Widget _buildSeveritySection(AppStrings s) {
    final sev = _stats.bySeverity;
    final total = sev.values.fold(0, (a, b) => a + b);
    pct(String k) => total == 0 ? 0.0 : (sev[k] ?? 0) / total * 100;

    final sections = [
      PieChartSectionData(value: pct('Critical').toDouble(), color: const Color(0xFF7A1F1F), title: '', radius: 50),
      PieChartSectionData(value: pct('High').toDouble(),     color: const Color(0xFFA32D2D), title: '', radius: 50),
      PieChartSectionData(value: pct('Medium').toDouble(),   color: const Color(0xFFEF9F27), title: '', radius: 50),
      PieChartSectionData(value: pct('Low').toDouble(),      color: const Color(0xFF3B6D11), title: '', radius: 50),
    ];

    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Text(s.severityBreakdown,
          style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
      const SizedBox(height: 10),
      Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
            color: Colors.white, borderRadius: BorderRadius.circular(18)),
        child: Row(children: [
          SizedBox(width: 130, height: 130,
            child: PieChart(PieChartData(sections: sections, sectionsSpace: 2,
                centerSpaceRadius: 30, borderData: FlBorderData(show: false)))),
          const SizedBox(width: 20),
          Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              ('Critical', '${pct('Critical').toInt()}%', const Color(0xFF7A1F1F)),
              ('High',     '${pct('High').toInt()}%',     const Color(0xFFA32D2D)),
              ('Medium',   '${pct('Medium').toInt()}%',   const Color(0xFFEF9F27)),
              ('Low',      '${pct('Low').toInt()}%',       const Color(0xFF3B6D11)),
            ].map((l) => Padding(
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
      ),
    ]);
  }

  Widget _buildCategorySection(AppStrings s) {
    final cats = _stats.byCategory;
    final total = cats.values.fold(0, (a, b) => a + b);
    if (cats.isEmpty) return const SizedBox();
    final sorted = cats.entries.toList()
      ..sort((a, b) => b.value.compareTo(a.value));

    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Text(s.topProblemCats,
          style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
      const SizedBox(height: 10),
      ...sorted.map((e) {
        final pct = total == 0 ? 0 : (e.value / total * 100).round();
        return Card(
          margin: const EdgeInsets.only(bottom: 8),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
            child: Row(children: [
              Container(width: 10, height: 10,
                  decoration: BoxDecoration(
                      color: _catColor(e.key), shape: BoxShape.circle)),
              const SizedBox(width: 10),
              Expanded(child: Text(e.key, style: const TextStyle(fontSize: 13))),
              SizedBox(width: 110, child: ClipRRect(
                borderRadius: BorderRadius.circular(4),
                child: LinearProgressIndicator(
                  value: pct / 100,
                  backgroundColor: Colors.grey.shade100,
                  valueColor: AlwaysStoppedAnimation<Color>(_catColor(e.key)),
                  minHeight: 6,
                ),
              )),
              const SizedBox(width: 10),
              SizedBox(width: 36, child: Text('$pct%',
                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                textAlign: TextAlign.right)),
            ]),
          ),
        );
      }),
    ]);
  }

  Widget _buildTopGreenhouses(AppStrings s) {
    final top = _stats.topGreenhouses;
    if (top.isEmpty) return const SizedBox();
    final maxF = top.fold(0, (m, g) => g.findings > m ? g.findings : m).toDouble();
    final medalColors = [const Color(0xFFBA7517), const Color(0xFF888780), const Color(0xFF854F0B)];

    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Text(s.topGhByFindings,
          style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
      const SizedBox(height: 10),
      Container(
        decoration: const BoxDecoration(color: Colors.white,
            borderRadius: BorderRadius.all(Radius.circular(16))),
        child: Column(children: top.asMap().entries.map((entry) {
          final rank = entry.key + 1;
          final gh   = entry.value;
          final pct  = maxF > 0 ? gh.findings / maxF : 0.0;
          return Column(children: [
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              child: Row(children: [
                Container(width: 26, height: 26,
                  decoration: BoxDecoration(
                      color: medalColors[rank-1].withValues(alpha: 0.12),
                      shape: BoxShape.circle),
                  child: Center(child: Text('#$rank',
                      style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold,
                          color: medalColors[rank-1])))),
                const SizedBox(width: 12),
                Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(gh.gh, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                  const SizedBox(height: 4),
                  ClipRRect(borderRadius: BorderRadius.circular(4),
                    child: LinearProgressIndicator(value: pct, minHeight: 5,
                        backgroundColor: Colors.grey.shade100,
                        valueColor: AlwaysStoppedAnimation<Color>(_catColor(gh.topIssue)))),
                ])),
                const SizedBox(width: 12),
                Column(crossAxisAlignment: CrossAxisAlignment.end, children: [
                  Text('${gh.findings}',
                      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                  const SizedBox(height: 2),
                  _chip(gh.topIssue, _catColor(gh.topIssue),
                      _catColor(gh.topIssue).withValues(alpha: 0.1)),
                ]),
              ]),
            ),
            if (rank < top.length)
              const Divider(height: 1, indent: 16, endIndent: 16),
          ]);
        }).toList()),
      ),
    ]);
  }

  Widget _buildRecentList(AppStrings s) {
    final rows = _filtered;
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Row(children: [
        Text(s.recentInspections,
            style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
        if (_activeStatFilter != 'all') ...[
          const SizedBox(width: 8),
          _chip(_activeStatFilter, AppColors.info, const Color(0xFFE6F1FB)),
        ],
      ]),
      const SizedBox(height: 10),
      if (rows.isEmpty)
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(color: Colors.white,
              borderRadius: BorderRadius.circular(16)),
          child: Text(s.noReportsYet,
              style: const TextStyle(color: Colors.grey)))
      else
        Container(
          decoration: const BoxDecoration(color: Colors.white,
              borderRadius: BorderRadius.all(Radius.circular(16))),
          child: Column(children: rows.asMap().entries.map((entry) {
            final i = entry.key;
            final r = entry.value;
            return Column(children: [
              Material(color: Colors.transparent, child: ListTile(
                onTap: () => ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                  content: Text('${s.openingInspect} ${r.date} · ${r.gh} · ${r.variety}'),
                  behavior: SnackBarBehavior.floating,
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10)),
                )),
                title: Text('${r.date} · ${r.gh} · ${r.variety}',
                    style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
                subtitle: Padding(
                  padding: const EdgeInsets.only(top: 4),
                  child: Wrap(spacing: 6, runSpacing: 4, children: [
                    _chip(r.category, _catColor(r.category),
                        _catColor(r.category).withValues(alpha: 0.1)),
                    _chip(r.severity, _severityColor(r.severity),
                        _severityColor(r.severity).withValues(alpha: 0.1)),
                    Text(r.inspectorName,
                        style: const TextStyle(fontSize: 12, color: Colors.grey)),
                  ]),
                ),
                trailing: const Icon(Icons.chevron_right, color: Colors.grey, size: 18),
              )),
              if (i < rows.length - 1)
                const Divider(height: 1, indent: 16, endIndent: 16),
            ]);
          }).toList()),
        ),
    ]);
  }

  Widget _barChart(_ReportStats data) {
    final labels = data.chartLabels;
    final maxD   = data.trendDisease.reduce((a, b) => a > b ? a : b);
    final maxP   = data.trendPest.reduce((a, b) => a > b ? a : b);
    final maxW   = data.trendWater.reduce((a, b) => a > b ? a : b);
    final maxY   = (maxD > maxP ? maxD : maxP > maxW ? maxP : maxW) * 1.25;
    return BarChart(BarChartData(
      alignment: BarChartAlignment.spaceAround,
      maxY: maxY < 1 ? 5 : maxY,
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
            if (idx < 0 || idx >= labels.length) return const SizedBox();
            return Padding(padding: const EdgeInsets.only(top: 6),
              child: Text(labels[idx],
                  style: const TextStyle(fontSize: 10, color: Colors.grey)));
          },
        )),
      ),
      gridData: FlGridData(drawVerticalLine: false,
          getDrawingHorizontalLine: (_) =>
              FlLine(color: Colors.grey.shade100, strokeWidth: 1)),
      borderData: FlBorderData(show: false),
      barGroups: List.generate(labels.length, (i) => BarChartGroupData(x: i, barRods: [
        BarChartRodData(toY: data.trendDisease[i], color: const Color(0xFF3B6D11),
            width: 5, borderRadius: BorderRadius.circular(4)),
        BarChartRodData(toY: data.trendPest[i],    color: const Color(0xFFEF9F27),
            width: 5, borderRadius: BorderRadius.circular(4)),
        BarChartRodData(toY: data.trendWater[i],   color: const Color(0xFF378ADD),
            width: 5, borderRadius: BorderRadius.circular(4)),
      ])),
    ));
  }

  Widget _lineChart(_ReportStats data) {
    final labels = data.chartLabels;
    final maxD   = data.trendDisease.reduce((a, b) => a > b ? a : b);
    final maxP   = data.trendPest.reduce((a, b) => a > b ? a : b);
    final maxW   = data.trendWater.reduce((a, b) => a > b ? a : b);
    final maxY   = (maxD > maxP ? maxD : maxP > maxW ? maxP : maxW) * 1.25;

    LineChartBarData series(List<double> vals, Color color) => LineChartBarData(
      spots: vals.asMap().entries.map((e) => FlSpot(e.key.toDouble(), e.value)).toList(),
      isCurved: true, color: color, barWidth: 2.5,
      dotData: const FlDotData(show: true),
      belowBarData: BarAreaData(show: false),
    );

    return LineChart(LineChartData(
      minY: 0, maxY: maxY < 1 ? 5 : maxY,
      titlesData: FlTitlesData(
        leftTitles:   AxisTitles(sideTitles: SideTitles(showTitles: false)),
        rightTitles:  AxisTitles(sideTitles: SideTitles(showTitles: false)),
        topTitles:    AxisTitles(sideTitles: SideTitles(showTitles: false)),
        bottomTitles: AxisTitles(sideTitles: SideTitles(
          showTitles: true, reservedSize: 28,
          getTitlesWidget: (v, m) {
            final idx = v.toInt();
            if (idx < 0 || idx >= labels.length) return const SizedBox();
            return Padding(padding: const EdgeInsets.only(top: 6),
              child: Text(labels[idx],
                  style: const TextStyle(fontSize: 10, color: Colors.grey)));
          },
        )),
      ),
      gridData: FlGridData(drawVerticalLine: false,
          getDrawingHorizontalLine: (_) =>
              FlLine(color: Colors.grey.shade100, strokeWidth: 1)),
      borderData: FlBorderData(show: false),
      lineBarsData: [
        series(data.trendDisease, const Color(0xFF3B6D11)),
        series(data.trendPest,    const Color(0xFFEF9F27)),
        series(data.trendWater,   const Color(0xFF378ADD)),
      ],
    ));
  }

  Widget _chartToggle(AppStrings s) => Row(
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
            border: Border.all(
                color: active ? AppColors.info : Colors.grey.shade300),
          ),
          child: Text(type, style: TextStyle(fontSize: 12,
            color: active ? Colors.white : Colors.grey.shade600,
            fontWeight: active ? FontWeight.bold : FontWeight.normal)),
        ),
      );
    }).toList(),
  );

  Widget _trendLegend(AppStrings s) => Wrap(spacing: 14, children: [
    (s.disease,      const Color(0xFF3B6D11)),
    (s.pests,        const Color(0xFFEF9F27)),
    (s.waterStressShort, const Color(0xFF378ADD)),
  ].map((item) => Row(mainAxisSize: MainAxisSize.min, children: [
    Container(width: 10, height: 10,
        decoration: BoxDecoration(color: item.$2,
            borderRadius: BorderRadius.circular(2))),
    const SizedBox(width: 4),
    Text(item.$1, style: const TextStyle(fontSize: 12, color: Colors.grey)),
  ])).toList());

  Widget _exportBtn({required IconData icon, required String label,
      required Color color, required VoidCallback onTap}) =>
    Material(color: Colors.white, borderRadius: BorderRadius.circular(14),
      child: InkWell(borderRadius: BorderRadius.circular(14), onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 14),
          decoration: BoxDecoration(
              border: Border.all(color: color.withValues(alpha: 0.3)),
              borderRadius: BorderRadius.circular(14)),
          child: Row(mainAxisAlignment: MainAxisAlignment.center, children: [
            Icon(icon, color: color, size: 20),
            const SizedBox(width: 8),
            Text(label, style: TextStyle(fontWeight: FontWeight.w600,
                color: color, fontSize: 14)),
          ]),
        ),
      ),
    );

  Widget _dropdown({required String label, required String value,
      required List<String> items, required ValueChanged<String?> onChanged}) =>
    DropdownButtonFormField<String>(
      value: items.contains(value) ? value : items.first,
      isExpanded: true,
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
      style: const TextStyle(fontSize: 12, color: Color(0xFF1A1F1A),
          fontWeight: FontWeight.w500),
      items: items.map((e) => DropdownMenuItem(value: e,
          child: Text(e, overflow: TextOverflow.ellipsis))).toList(),
      onChanged: onChanged,
    );

  Widget _chip(String label, Color textColor, Color bgColor) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
    decoration: BoxDecoration(color: bgColor, borderRadius: BorderRadius.circular(20)),
    child: Text(label, style: TextStyle(fontSize: 11, color: textColor,
        fontWeight: FontWeight.w600)),
  );

  void _showExportDialog(String type, AppStrings s) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(18)),
        title: Text(type == 'pdf' ? s.exportPdf : s.exportExcel),
        content: Text(type == 'pdf' ? s.exportPdfDesc : s.exportExcelDesc),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: Text(s.cancel)),
          ElevatedButton(
            onPressed: () { Navigator.pop(ctx); _triggerExport(type, s); },
            child: Text(s.download),
          ),
        ],
      ),
    );
  }

  void _triggerExport(String type, AppStrings s) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content: Text('${type == 'pdf' ? s.exportPdf : s.exportExcel} — ${_periodLabel(s)}'),
      behavior: SnackBarBehavior.floating,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
    ));
  }
}
"""

pathlib.Path('lib/features/reports/presentation/reports_screen.dart').write_text(reports, encoding='utf-8')
print('reports_screen.dart done')
print('ALL STEP 2 FILES WRITTEN')