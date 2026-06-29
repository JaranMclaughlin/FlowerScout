import pathlib, sys

p = pathlib.Path('lib/features/dashboard/presentation/dashboard_screen.dart')
text = p.read_text(encoding='utf-8')

# 1. Add analytics_data import
old_import = "import '../../../shared/providers/shell_tab_provider.dart';"
new_import = """import '../../../shared/providers/shell_tab_provider.dart';
import '../../../shared/providers/analytics_data.dart';
import '../../../shared/providers/locale_provider.dart';"""
if old_import not in text:
    sys.exit("Import anchor not found.")
text = text.replace(old_import, new_import, 1)

# 2. Wire reportStatsProvider into build
old_build = """        data: (farms) {
            final stats    = _DashboardStats.fromFarms(farms);
            final userName = profileAsync.value?.fullName.split(' ').first;
            return SingleChildScrollView("""
new_build = """        data: (farms) {
            final stats    = _DashboardStats.fromFarms(farms);
            final userName = profileAsync.value?.fullName.split(' ').first;
            final filter   = AnalyticsFilter(period: '7days');
            final rptStats = ref.watch(reportStatsProvider(filter));
            final critical = rptStats.value?.critical ?? 0;
            final total    = rptStats.value?.total ?? 0;
            return SingleChildScrollView("""
if old_build not in text:
    sys.exit("Build anchor not found.")
text = text.replace(old_build, new_build, 1)

# 3. Pass critical + total to _HealthCard and _StatsGrid
old_health = "                  _HealthCard(stats: stats, s: s),"
new_health = "                  _HealthCard(stats: stats, s: s, criticalFindings: critical, totalFindings: total),"
text = text.replace(old_health, new_health, 1)

# 4. Update _HealthCard to accept and use findings data
old_card_class = """class _HealthCard extends StatelessWidget {
  final AppStrings s;
  final _DashboardStats stats;
  const _HealthCard({required this.stats, required this.s});

  @override
  Widget build(BuildContext context) {
    final score = stats.healthScore;
    final label = score >= 80 ? s.excellentCond
        : score >= 60 ? s.goodCond
        : score >= 40 ? s.needsAttention
        : s.criticalAction;
    return Container(
      width: double.infinity,
      padding: AppSizes.cardPaddingLg,
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [AppColors.forest, AppColors.canopy, AppColors.leaf],
          begin: Alignment.topLeft, end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(AppSizes.radiusXl),
        boxShadow: [BoxShadow(color: AppColors.canopy.withValues(alpha: 0.30),
            blurRadius: 20, offset: const Offset(0, 8))],
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(s.ghActivation,
            style: TextStyle(color: Colors.white.withValues(alpha: 0.75), fontSize: 13)),
        const SizedBox(height: AppSizes.spaceSm),
        Text('$score%', style: const TextStyle(color: Colors.white,
            fontSize: 44, fontWeight: FontWeight.bold, height: 1)),
        const SizedBox(height: AppSizes.spaceSm),
        Text('$label · ${stats.activeGreenhouses}/${stats.totalGreenhouses} ${s.activeGh}',
            style: const TextStyle(color: Colors.white, fontSize: 13)),
      ]),
    );
  }
}"""

new_card_class = """class _HealthCard extends StatelessWidget {
  final AppStrings s;
  final _DashboardStats stats;
  final int criticalFindings;
  final int totalFindings;
  const _HealthCard({
    required this.stats, required this.s,
    this.criticalFindings = 0, this.totalFindings = 0,
  });

  /// Composite score:
  /// 60% greenhouse activation + 40% finding severity penalty
  int get healthScore {
    if (stats.totalGreenhouses == 0) return 0;
    final activePct = (stats.activeGreenhouses / stats.totalGreenhouses) * 60;
    // Severity penalty: each critical finding costs 4pts, capped at 40
    final penalty = (criticalFindings * 4).clamp(0, 40);
    return (activePct + (40 - penalty)).round().clamp(0, 100);
  }

  @override
  Widget build(BuildContext context) {
    final score = healthScore;
    final label = score >= 80 ? s.excellentCond
        : score >= 60 ? s.goodCond
        : score >= 40 ? s.needsAttention
        : s.criticalAction;
    final gradientColors = score >= 80
        ? [AppColors.forest, AppColors.canopy, AppColors.leaf]
        : score >= 60
            ? [AppColors.canopy, AppColors.leaf, const Color(0xFF52B788)]
            : score >= 40
                ? [const Color(0xFF7A5C00), const Color(0xFF9A7500), AppColors.warning]
                : [const Color(0xFF7A1F1F), const Color(0xFFB53030), AppColors.critical];
    return Container(
      width: double.infinity,
      padding: AppSizes.cardPaddingLg,
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: gradientColors,
          begin: Alignment.topLeft, end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(AppSizes.radiusXl),
        boxShadow: [BoxShadow(color: gradientColors[0].withValues(alpha: 0.30),
            blurRadius: 20, offset: const Offset(0, 8))],
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(s.ghActivation,
            style: TextStyle(color: Colors.white.withValues(alpha: 0.75), fontSize: 13)),
        const SizedBox(height: AppSizes.spaceSm),
        Row(crossAxisAlignment: CrossAxisAlignment.end, children: [
          Text('$score%', style: const TextStyle(color: Colors.white,
              fontSize: 44, fontWeight: FontWeight.bold, height: 1)),
          const SizedBox(width: 12),
          if (criticalFindings > 0)
            Container(
              margin: const EdgeInsets.only(bottom: 6),
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
              decoration: BoxDecoration(
                color: Colors.white.withValues(alpha: 0.20),
                borderRadius: BorderRadius.circular(AppSizes.radiusPill),
              ),
              child: Row(mainAxisSize: MainAxisSize.min, children: [
                const Icon(Icons.warning_amber_rounded, color: Colors.white, size: 12),
                const SizedBox(width: 4),
                Text('$criticalFindings critical (7d)',
                    style: const TextStyle(color: Colors.white, fontSize: 11,
                        fontWeight: FontWeight.w600)),
              ]),
            ),
        ]),
        const SizedBox(height: AppSizes.spaceSm),
        Text('$label · ${stats.activeGreenhouses}/${stats.totalGreenhouses} ${s.activeGh}'
            '${totalFindings > 0 ? " · $totalFindings inspections" : ""}',
            style: const TextStyle(color: Colors.white, fontSize: 13)),
      ]),
    );
  }
}"""

if old_card_class not in text:
    sys.exit("HealthCard anchor not found.")
text = text.replace(old_card_class, new_card_class, 1)

p.write_text(text, encoding='utf-8')
print("dashboard_screen.dart: real health score wired.")