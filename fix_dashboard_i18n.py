import pathlib
p = pathlib.Path('lib/features/dashboard/presentation/dashboard_screen.dart')
t = p.read_text(encoding='utf-8')

# Check if stringsProvider is available
if 'stringsProvider' not in t:
    old_imp = "import 'package:flutter_riverpod/flutter_riverpod.dart';"
    new_imp = "import 'package:flutter_riverpod/flutter_riverpod.dart';\nimport '../../../shared/providers/locale_provider.dart';\nimport '../../../shared/l10n/app_strings.dart';"
    t = t.replace(old_imp, new_imp, 1)

replacements = [
    # Section headings
    ("Text('Farm Overview', style: AppTextStyles.heading)",
     "Text(s.farmOverview, style: AppTextStyles.heading)"),
    ("Text('Farms', style: AppTextStyles.heading)",
     "Text(s.farms, style: AppTextStyles.heading)"),
    ("Text('Quick Actions', style: AppTextStyles.heading)",
     "Text(s.quickActions, style: AppTextStyles.heading)"),
    ("Text('Report Summary', style: AppTextStyles.heading)",
     "Text(s.reportSummary, style: AppTextStyles.heading)"),
    # Stat cards
    ("_StatCardData('Farms',       '${stats.totalFarms}',",
     "_StatCardData(s.farms,       '${stats.totalFarms}',"),
    ("_StatCardData('Greenhouses', '${stats.totalGreenhouses}',",
     "_StatCardData(s.greenhouses, '${stats.totalGreenhouses}',"),
    ("_StatCardData('Plantings',   '${stats.totalPlantings}',",
     "_StatCardData(s.plantings,   '${stats.totalPlantings}',"),
    ("_StatCardData('Varieties',   '${stats.varieties.length}',",
     "_StatCardData(s.varieties,   '${stats.varieties.length}',"),
    # Summary rows
    ("_SummaryRow(Icons.local_florist_rounded, 'Total plants',",
     "_SummaryRow(Icons.local_florist_rounded, s.totalPlants,"),
    ("_SummaryRow(Icons.eco_rounded,            'Varieties in use',",
     "_SummaryRow(Icons.eco_rounded,            s.varietiesInUse,"),
    ("_SummaryRow(Icons.house_siding_rounded,   'Active greenhouses',",
     "_SummaryRow(Icons.house_siding_rounded,   s.activeGh,"),
    ("_SummaryRow(Icons.warning_amber_rounded,  'Inactive',",
     "_SummaryRow(Icons.warning_amber_rounded,  s.inactiveLabel,"),
    # Greenhouse activation card
    ("Text('Greenhouse Activation',",
     "Text(s.ghActivation,"),
    # Condition label
    ("final label = score >= 80 ? 'Excellent condition'",
     "final label = score >= 80 ? s.excellentCond"),
    # greenhouses active suffix
    ("Text('$label \u00b7 ${stats.activeGreenhouses}/${stats.totalGreenhouses} greenhouses active',",
     "Text('$label \u00b7 ${stats.activeGreenhouses}/${stats.totalGreenhouses} ${s.activeGh}',"),
    # Quick actions buttons
    ("(Icons.add_circle_outline_rounded, 'New Report', 1),",
     "(Icons.add_circle_outline_rounded, s.newReport, 1),"),
    ("(Icons.map_outlined,               'Open Maps',  2),",
     "(Icons.map_outlined,               s.openMaps,  2),"),
    ("final isPrimary = a.\$2 == 'New Report';",
     "final isPrimary = a.\$2 == s.newReport;"),
    # Farm card active/check badge
    ("child: Text(pct >= 0.8 ? 'Active' : 'Check',",
     "child: Text(pct >= 0.8 ? s.active : s.check,"),
    # Inactive GH badge
    ("child: Text('\${g.code} inactive', style: TextStyle(fontSize: 11,",
     "child: Text('\${g.code} \${s.inactive}', style: TextStyle(fontSize: 11,"),
    # Empty farms card
    ("Text('Farms you have access to will appear here.',",
     "Text(s.noFarmsDesc,"),
]

failed = []
for old, new in replacements:
    if old in t:
        t = t.replace(old, new, 1)
    else:
        failed.append(old[:70])

p.write_text(t, encoding='utf-8')
print('dashboard_screen.dart updated.')
if failed: print('MISSED:', failed)