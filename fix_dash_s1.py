import pathlib
p = pathlib.Path('lib/features/dashboard/presentation/dashboard_screen.dart')
t = p.read_text(encoding='utf-8')

# Add locale import
if 'locale_provider' not in t:
    old = "import 'package:flutter_riverpod/flutter_riverpod.dart';"
    new = "import 'package:flutter_riverpod/flutter_riverpod.dart';\nimport '../../../shared/providers/locale_provider.dart';\nimport '../../../shared/l10n/app_strings.dart';"
    t = t.replace(old, new, 1)

# DashboardScreen.build - add s
old = "  Widget build(BuildContext context, WidgetRef ref) {\n"
new = "  Widget build(BuildContext context, WidgetRef ref) {\n    final s = ref.watch(stringsProvider);\n"
# Only replace first occurrence (DashboardScreen)
t = t.replace(old, new, 1)

# _WideBody - add s field and pass it
old = "class _WideBody extends StatelessWidget {\n  final List<FarmModel> farms;\n  final _DashboardStats stats;\n  final WidgetRef ref;\n  const _WideBody({required this.farms, required this.stats, required this.ref});"
new = "class _WideBody extends StatelessWidget {\n  final List<FarmModel> farms;\n  final _DashboardStats stats;\n  final WidgetRef ref;\n  final AppStrings s;\n  const _WideBody({required this.farms, required this.stats, required this.ref, required this.s});"
if old in t: t = t.replace(old, new, 1)
else: print('MISSED _WideBody constructor')

# _NarrowBody - add s field
old = "class _NarrowBody extends StatelessWidget {\n  final List<FarmModel> farms;\n  final _DashboardStats stats;\n  final WidgetRef ref;\n  const _NarrowBody({required this.farms, required this.stats, required this.ref});"
new = "class _NarrowBody extends StatelessWidget {\n  final List<FarmModel> farms;\n  final _DashboardStats stats;\n  final WidgetRef ref;\n  final AppStrings s;\n  const _NarrowBody({required this.farms, required this.stats, required this.ref, required this.s});"
if old in t: t = t.replace(old, new, 1)
else: print('MISSED _NarrowBody constructor')

# Pass s to _WideBody and _NarrowBody at call sites
t = t.replace('_WideBody(farms: farms, stats: stats, ref: ref)', '_WideBody(farms: farms, stats: stats, ref: ref, s: s)')
t = t.replace('_NarrowBody(farms: farms, stats: stats, ref: ref)', '_NarrowBody(farms: farms, stats: stats, ref: ref, s: s)')

# _ReportSummaryCard - add s
old = "class _ReportSummaryCard extends StatelessWidget {"
new = "class _ReportSummaryCard extends StatelessWidget {\n  final AppStrings s;"
if old in t: t = t.replace(old, new, 1)

# _HealthCard - add s
old = "class _HealthCard extends StatelessWidget {"
new = "class _HealthCard extends StatelessWidget {\n  final AppStrings s;"
if old in t: t = t.replace(old, new, 1)

# _StatsGrid - add s
old = "class _StatsGrid extends StatelessWidget {"
new = "class _StatsGrid extends StatelessWidget {\n  final AppStrings s;"
if old in t: t = t.replace(old, new, 1)

# _FarmTile - add s
old = "class _FarmTile extends StatelessWidget {\n  final FarmModel farm;"
new = "class _FarmTile extends StatelessWidget {\n  final FarmModel farm;\n  final AppStrings s;"
if old in t: t = t.replace(old, new, 1)

# _EmptyFarmsCard - add s
old = "class _EmptyFarmsCard extends StatelessWidget {\n  const _EmptyFarmsCard();"
new = "class _EmptyFarmsCard extends StatelessWidget {\n  final AppStrings s;\n  const _EmptyFarmsCard({required this.s});"
if old in t: t = t.replace(old, new, 1)

p.write_text(t, encoding='utf-8')
print('Pass 1 done - fields added.')