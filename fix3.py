import pathlib

rp = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
rc = rp.read_text(encoding='utf-8')

# Fix return type of _buildTrend and remove unused 'now'
rc = rc.replace(
    "  static Map<String, List> _buildTrend(\n      List<_Inspection> inspections, String period) {\n    final now = DateTime.now();",
    "  static Map<String, List<dynamic>> _buildTrend(\n      List<_Inspection> inspections, String period) {"
)

# Fix the callers to cast properly
rc = rc.replace(
    "      trendDisease: buckets['disease']!,\n      trendPest: buckets['pest']!,\n      trendWater: buckets['water']!,",
    "      trendDisease: List<double>.from(buckets['disease']!),\n      trendPest: List<double>.from(buckets['pest']!),\n      trendWater: List<double>.from(buckets['water']!),"
)

# Remove unused farm_providers import from app_shell
sp = pathlib.Path('lib/shared/widgets/app_shell.dart')
sc = sp.read_text(encoding='utf-8')
sc = sc.replace("import '../providers/farm_providers.dart';\n", "")
sp.write_text(sc, encoding='utf-8')

# Remove unused trail_providers import from scouting_screen
scp = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
scc = scp.read_text(encoding='utf-8')
scc = scc.replace("import '../../../shared/trail/providers/trail_providers.dart';\n", "")
scp.write_text(scc, encoding='utf-8')

rp.write_text(rc, encoding='utf-8')
print('done')