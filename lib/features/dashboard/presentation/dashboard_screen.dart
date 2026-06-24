import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../shared/providers/locale_provider.dart';
import '../../../shared/l10n/app_strings.dart';
import '../../../core/theme/app_theme.dart';
import '../../../shared/theme/app_colors.dart';
import '../../../shared/providers/farm_providers.dart';
import '../../../shared/providers/farm_repository.dart';
import '../../../shared/providers/shell_tab_provider.dart';

class DashboardScreen extends ConsumerWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = ref.watch(stringsProvider);
    final farmsAsync   = ref.watch(farmsProvider);
    final profileAsync = ref.watch(profileProvider);
    final pad          = AppSizes.pagePadding(context);
    final isWide       = !AppSizes.isPhone(context);

    return Scaffold(
      backgroundColor: AppColors.background,
      body: RefreshIndicator(
        color: AppColors.leaf,
        onRefresh: () async {
          await ref.read(farmsProvider.notifier).refresh();
          await ref.read(profileProvider.notifier).refresh();
        },
        child: farmsAsync.when(
          loading: () => const Center(child: CircularProgressIndicator(color: AppColors.leaf)),
          error:   (e, _) => _ErrorState(message: e.toString()),
          data: (farms) {
            final stats    = _DashboardStats.fromFarms(farms);
            final userName = profileAsync.value?.fullName.split(' ').first;
            return SingleChildScrollView(
              physics: const AlwaysScrollableScrollPhysics(),
              padding: EdgeInsets.all(pad),
              child: Center(
                child: ConstrainedBox(
                  constraints: const BoxConstraints(maxWidth: AppSizes.maxContentWidth),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _Greeting(name: userName),
                      const SizedBox(height: AppSizes.spaceLg),
                      _HealthCard(stats: stats, s: s),
                      const SizedBox(height: AppSizes.space2xl),
                      Text(s.farmOverview, style: AppTextStyles.heading),
                      const SizedBox(height: AppSizes.spaceMd),
                      _StatsGrid(stats: stats, s: s),
                      const SizedBox(height: AppSizes.space2xl),
                      if (isWide)
                        _WideBody(farms: farms, stats: stats, ref: ref, s: s)
                      else
                        _NarrowBody(farms: farms, stats: stats, ref: ref, s: s),
                      const SizedBox(height: AppSizes.space3xl),
                    ],
                  ),
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}

// ── Wide layout (tablet / desktop) ──────────────────────────────────────────
class _WideBody extends StatelessWidget {
  final List<FarmModel> farms;
  final _DashboardStats stats;
  final WidgetRef ref;
  final AppStrings s;
  const _WideBody({required this.farms, required this.stats, required this.ref, required this.s});

  @override
  Widget build(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Left column — farms
        Expanded(
          flex: 3,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(s.farms, style: AppTextStyles.heading),
              const SizedBox(height: AppSizes.spaceMd),
              if (farms.isEmpty)
                _EmptyFarmsCard(s: s)
              else
                ...farms.map((f) => _FarmTile(farm: f, s: s)),
            ],
          ),
        ),
        const SizedBox(width: AppSizes.space2xl),
        // Right column — quick actions + report summary
        Expanded(
          flex: 2,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(s.quickActions, style: AppTextStyles.heading),
              const SizedBox(height: AppSizes.spaceMd),
              _QuickActions(),
              const SizedBox(height: AppSizes.space2xl),
              Text(s.reportSummary, style: AppTextStyles.heading),
              const SizedBox(height: AppSizes.spaceMd),
              _ReportSummaryCard(stats: stats, ref: ref, s: s),
            ],
          ),
        ),
      ],
    );
  }
}

// ── Narrow layout (phone) ────────────────────────────────────────────────────
class _NarrowBody extends StatelessWidget {
  final List<FarmModel> farms;
  final _DashboardStats stats;
  final WidgetRef ref;
  final AppStrings s;
  const _NarrowBody({required this.farms, required this.stats, required this.ref, required this.s});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Quick Actions', style: AppTextStyles.heading),
        const SizedBox(height: AppSizes.spaceMd),
        _QuickActions(),
        const SizedBox(height: AppSizes.space2xl),
        Text('Report Summary', style: AppTextStyles.heading),
        const SizedBox(height: AppSizes.spaceMd),
        _ReportSummaryCard(stats: stats, ref: ref, s: s),
        const SizedBox(height: AppSizes.space2xl),
        Text('Farms', style: AppTextStyles.heading),
        const SizedBox(height: AppSizes.spaceMd),
        if (farms.isEmpty)
          _EmptyFarmsCard(s: s)
        else
          ...farms.map((f) => _FarmTile(farm: f, s: s)),
      ],
    );
  }
}

// ── Report summary card ──────────────────────────────────────────────────────
class _ReportSummaryCard extends StatelessWidget {
  final AppStrings s;
  final _DashboardStats stats;
  final WidgetRef ref;
  const _ReportSummaryCard({required this.stats, required this.ref, required this.s});

  @override
  Widget build(BuildContext context) {
    final rows = [
      _SummaryRow(Icons.local_florist_rounded, s.totalPlants,       '${stats.totalPlants}',          AppColors.leaf),
      _SummaryRow(Icons.eco_rounded,            s.varietiesInUse,   '${stats.varieties.length}',     AppColors.canopy),
      _SummaryRow(Icons.house_siding_rounded,   s.activeGh, '${stats.activeGreenhouses}',   AppColors.info),
      _SummaryRow(Icons.warning_amber_rounded,  s.inactiveLabel,           '${stats.inactiveGreenhouses}', stats.inactiveGreenhouses > 0 ? AppColors.warning : AppColors.muted),
      _SummaryRow(Icons.straighten_rounded,     'Total area',
          stats.totalAreaM2 > 0 ? '${stats.totalAreaM2.toStringAsFixed(0)} m²' : '—', AppColors.graphite),
    ];

    return Container(
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(AppSizes.radiusLg),
        border: Border.all(color: AppColors.divider),
        boxShadow: [BoxShadow(color: Colors.black.withValues(alpha: 0.03),
            blurRadius: 8, offset: const Offset(0, 2))],
      ),
      child: Column(
        children: [
          ...rows.asMap().entries.map((e) => Column(children: [
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 11),
              child: Row(children: [
                Container(
                  width: 32, height: 32,
                  decoration: BoxDecoration(
                    color: e.value.color.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(AppSizes.radiusSm),
                  ),
                  child: Icon(e.value.icon, color: e.value.color, size: AppSizes.iconSm)),
                const SizedBox(width: 12),
                Expanded(child: Text(e.value.label, style: AppTextStyles.body)),
                Text(e.value.value, style: AppTextStyles.body.copyWith(
                    fontWeight: FontWeight.w700, color: AppColors.ink)),
              ]),
            ),
            if (e.key < rows.length - 1)
              const Divider(height: 0.5, thickness: 0.5, indent: 16, endIndent: 16),
          ])),
          const Divider(height: 0.5, thickness: 0.5),
          InkWell(
            borderRadius: const BorderRadius.vertical(bottom: Radius.circular(AppSizes.radiusLg)),
            onTap: () => ref.read(selectedTabProvider.notifier).set(3),
            child: Padding(
              padding: const EdgeInsets.symmetric(vertical: 12),
              child: Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                Text('View full reports', style: AppTextStyles.body.copyWith(
                    color: AppColors.leaf, fontWeight: FontWeight.w600)),
                const SizedBox(width: 4),
                const Icon(Icons.arrow_forward_rounded, size: 14, color: AppColors.leaf),
              ]),
            ),
          ),
        ],
      ),
    );
  }
}

class _SummaryRow {
  final IconData icon;
  final String label, value;
  final Color color;
  const _SummaryRow(this.icon, this.label, this.value, this.color);
}

// ── Computed stats ───────────────────────────────────────────────────────────
class _DashboardStats {
  final int totalFarms, totalGreenhouses, activeGreenhouses,
      inactiveGreenhouses, totalPlantings, totalPlants;
  final double totalAreaM2;
  final Set<String> varieties;

  const _DashboardStats({
    required this.totalFarms, required this.totalGreenhouses,
    required this.activeGreenhouses, required this.inactiveGreenhouses,
    required this.totalPlantings, required this.totalPlants,
    required this.totalAreaM2, required this.varieties,
  });

  factory _DashboardStats.fromFarms(List<FarmModel> farms) {
    int gh = 0, active = 0, plantings = 0, plants = 0;
    double area = 0;
    final varietySet = <String>{};
    for (final farm in farms) {
      for (final g in farm.greenhouses) {
        gh++;
        if (g.isActive) active++;
        for (final p in g.plantings) {
          plantings++;
          plants += p.numberOfPlants ?? 0;
          area   += p.areaM2 ?? 0;
          varietySet.add(p.varietyName);
        }
      }
    }
    return _DashboardStats(
      totalFarms: farms.length, totalGreenhouses: gh,
      activeGreenhouses: active, inactiveGreenhouses: gh - active,
      totalPlantings: plantings, totalPlants: plants,
      totalAreaM2: area, varieties: varietySet,
    );
  }

  int get healthScore => totalGreenhouses == 0
      ? 0 : ((activeGreenhouses / totalGreenhouses) * 100).round();
}

// ── Greeting ─────────────────────────────────────────────────────────────────
class _Greeting extends StatelessWidget {
  final String? name;
  const _Greeting({this.name});

  String _tod() {
    final h = DateTime.now().hour;
    if (h < 12) return 'Good morning';
    if (h < 17) return 'Good afternoon';
    return 'Good evening';
  }

  @override
  Widget build(BuildContext context) => Text(
    name != null && name!.isNotEmpty ? '${_tod()}, $name' : _tod(),
    style: AppTextStyles.displayLarge,
  );
}

// ── Health card ──────────────────────────────────────────────────────────────
class _HealthCard extends StatelessWidget {
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
}

// ── Stats grid ───────────────────────────────────────────────────────────────
class _StatsGrid extends StatelessWidget {
  final AppStrings s;
  final _DashboardStats stats;
  const _StatsGrid({required this.stats, required this.s});

  @override
  Widget build(BuildContext context) {
    final cards = [
      _StatCardData(s.farms,       '${stats.totalFarms}',       Icons.agriculture_rounded,    AppColors.leaf),
      _StatCardData(s.greenhouses, '${stats.totalGreenhouses}', Icons.house_siding_rounded,   AppColors.info),
      _StatCardData(s.plantings,   '${stats.totalPlantings}',   Icons.local_florist_rounded,  AppColors.canopy),
      _StatCardData(s.varieties,   '${stats.varieties.length}', Icons.eco_rounded,            AppColors.nutrition),
    ];
    return LayoutBuilder(builder: (context, c) {
      final cols = c.maxWidth >= 560 ? 4 : 2;
      return GridView.count(
        crossAxisCount: cols, shrinkWrap: true,
        physics: const NeverScrollableScrollPhysics(),
        crossAxisSpacing: AppSizes.spaceMd, mainAxisSpacing: AppSizes.spaceMd,
        childAspectRatio: 1.7,
        children: cards.map((c) => _StatCard(data: c)).toList(),
      );
    });
  }
}

class _StatCardData {
  final String label, value;
  final IconData icon;
  final Color color;
  const _StatCardData(this.label, this.value, this.icon, this.color);
}

class _StatCard extends StatelessWidget {
  final _StatCardData data;
  const _StatCard({required this.data});

  @override
  Widget build(BuildContext context) => Container(
    padding: AppSizes.cardPadding,
    decoration: BoxDecoration(
      color: AppColors.surface,
      borderRadius: BorderRadius.circular(AppSizes.radiusLg),
      border: Border.all(color: AppColors.divider),
      boxShadow: [BoxShadow(color: Colors.black.withValues(alpha: 0.03),
          blurRadius: 8, offset: const Offset(0, 2))],
    ),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisAlignment: MainAxisAlignment.center,
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(data.icon, color: data.color, size: AppSizes.iconMd),
        const SizedBox(height: AppSizes.spaceSm),
        Text(data.value, style: const TextStyle(fontSize: 24,
            fontWeight: FontWeight.bold, color: AppColors.ink)),
        const SizedBox(height: 2),
        Text(data.label, style: AppTextStyles.caption),
      ],
    ),
  );
}

// ── Quick actions ─────────────────────────────────────────────────────────────
class _QuickActions extends ConsumerWidget {
  const _QuickActions();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = ref.watch(stringsProvider);
    final actions = [
      (Icons.add_circle_outline_rounded, s.newReport, 1),
      (Icons.map_outlined,               s.openMaps,  2),
      (Icons.settings_outlined,          s.settings,   4),
    ];
    return Wrap(spacing: AppSizes.spaceSm, runSpacing: AppSizes.spaceSm,
      children: actions.map((a) {
        final isPrimary = a.$2 == s.newReport;
        return Material(
          color: isPrimary ? AppColors.leaf : AppColors.surface,
          borderRadius: BorderRadius.circular(AppSizes.radiusMd),
          child: InkWell(
            borderRadius: BorderRadius.circular(AppSizes.radiusMd),
            onTap: () => ref.read(selectedTabProvider.notifier).set(a.$3),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(AppSizes.radiusMd),
                border: Border.all(color: isPrimary ? AppColors.leaf : AppColors.divider),
              ),
              child: Row(mainAxisSize: MainAxisSize.min, children: [
                Icon(a.$1, size: AppSizes.iconSm,
                    color: isPrimary ? Colors.white : AppColors.leaf),
                const SizedBox(width: 6),
                Text(a.$2, style: AppTextStyles.body.copyWith(
                  fontWeight: FontWeight.w500,
                  color: isPrimary ? Colors.white : AppColors.ink,
                )),
              ]),
            ),
          ),
        );
      }).toList(),
    );
  }
}

// ── Farm tile ─────────────────────────────────────────────────────────────────
class _FarmTile extends StatelessWidget {
  final FarmModel farm;
  final AppStrings s;
  const _FarmTile({required this.farm, required this.s});

  @override
  Widget build(BuildContext context) {
    final ghCount    = farm.greenhouses.length;
    final activeCount = farm.greenhouses.where((g) => g.isActive).length;
    final inactiveGh = farm.greenhouses.where((g) => !g.isActive).toList();
    final pct        = ghCount == 0 ? 0.0 : activeCount / ghCount;
    final pctLabel   = '${(pct * 100).round()}%';

    return Container(
      margin: const EdgeInsets.only(bottom: AppSizes.spaceMd),
      padding: AppSizes.cardPadding,
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(AppSizes.radiusLg),
        border: Border.all(color: AppColors.divider),
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          Container(width: 40, height: 40,
            decoration: const BoxDecoration(color: AppColors.mist, shape: BoxShape.circle),
            child: const Icon(Icons.agriculture_rounded, color: AppColors.leaf, size: 20)),
          const SizedBox(width: AppSizes.spaceMd),
          Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(farm.name, style: AppTextStyles.title),
            const SizedBox(height: 2),
            Text(
              '$activeCount of $ghCount greenhouses active'
              '${farm.location != null ? ' · ${farm.location}' : ''}',
              style: AppTextStyles.caption),
            const SizedBox(height: 8),
            ClipRRect(
              borderRadius: BorderRadius.circular(4),
              child: LinearProgressIndicator(
                value: pct, minHeight: 4,
                backgroundColor: AppColors.divider,
                valueColor: AlwaysStoppedAnimation<Color>(
                  pct >= 0.8 ? AppColors.leaf
                      : pct >= 0.5 ? AppColors.warning : AppColors.critical),
              ),
            ),
          ])),
          const SizedBox(width: AppSizes.spaceMd),
          Column(crossAxisAlignment: CrossAxisAlignment.end, children: [
            Text(pctLabel, style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600,
                color: pct >= 0.8 ? AppColors.leaf
                    : pct >= 0.5 ? AppColors.warning : AppColors.critical)),
            const SizedBox(height: 4),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
              decoration: BoxDecoration(
                color: pct >= 0.8 ? AppColors.mist : AppColors.severityBg('medium'),
                borderRadius: BorderRadius.circular(AppSizes.radiusPill),
              ),
              child: Text(pct >= 0.8 ? s.active : s.check,
                style: TextStyle(fontSize: 11, fontWeight: FontWeight.w600,
                    color: pct >= 0.8 ? AppColors.leaf : AppColors.severityColor('medium'))),
            ),
          ]),
        ]),
        if (inactiveGh.isNotEmpty) ...[
          const SizedBox(height: AppSizes.spaceMd),
          const Divider(),
          const SizedBox(height: AppSizes.spaceSm),
          Wrap(spacing: AppSizes.spaceSm, runSpacing: AppSizes.spaceSm,
            children: inactiveGh.map((g) => Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
              decoration: BoxDecoration(
                color: AppColors.severityBg('medium'),
                borderRadius: BorderRadius.circular(AppSizes.radiusPill),
              ),
              child: Text('${g.code} ${s.inactive}', style: TextStyle(fontSize: 11,
                  fontWeight: FontWeight.w600,
                  color: AppColors.severityColor('medium'))),
            )).toList()),
        ],
      ]),
    );
  }
}

// ── Empty / error states ──────────────────────────────────────────────────────
class _EmptyFarmsCard extends StatelessWidget {
  final AppStrings s;
  const _EmptyFarmsCard({required this.s});
  @override
  Widget build(BuildContext context) => Container(
    width: double.infinity,
    padding: AppSizes.cardPaddingLg,
    decoration: BoxDecoration(
      color: AppColors.surface,
      borderRadius: BorderRadius.circular(AppSizes.radiusLg),
      border: Border.all(color: AppColors.divider),
    ),
    child: Column(children: [
      const Icon(Icons.agriculture_outlined, size: 40, color: AppColors.muted),
      const SizedBox(height: AppSizes.spaceMd),
      Text('No farms yet', style: AppTextStyles.title),
      const SizedBox(height: 4),
      Text(s.noFarmsDesc,
          style: AppTextStyles.caption, textAlign: TextAlign.center),
    ]),
  );
}

class _ErrorState extends StatelessWidget {
  final String message;
  const _ErrorState({required this.message});
  @override
  Widget build(BuildContext context) => Center(
    child: Padding(padding: const EdgeInsets.all(24),
      child: Column(mainAxisSize: MainAxisSize.min, children: [
        const Icon(Icons.error_outline_rounded, size: 40, color: AppColors.critical),
        const SizedBox(height: AppSizes.spaceMd),
        Text('Could not load dashboard', style: AppTextStyles.title),
        const SizedBox(height: 4),
        Text(message, style: AppTextStyles.caption, textAlign: TextAlign.center),
      ]),
    ),
  );
}