import pathlib, re

# ── Fix 1: Add missing import to reports_screen.dart ─────────────────────────
rp = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
rc = rp.read_text(encoding='utf-8')
if "import '../../../shared/l10n/app_strings.dart'" not in rc:
    rc = rc.replace(
        "import '../../../shared/providers/locale_provider.dart';",
        "import '../../../shared/providers/locale_provider.dart';\nimport '../../../shared/l10n/app_strings.dart';"
    )

# ── Fix 2: Fix _buildTrend List<dynamic> type errors ─────────────────────────
rc = rc.replace(
    "    final disease = List<double>.filled(bucketCount, 0);\n    final pest    = List<double>.filled(bucketCount, 0);\n    final water   = List<double>.filled(bucketCount, 0);",
    "    final disease = List<double>.filled(bucketCount, 0.0);\n    final pest    = List<double>.filled(bucketCount, 0.0);\n    final water   = List<double>.filled(bucketCount, 0.0);"
)

# ── Fix 3: Remove unused variables + bad _ usage in _buildTrend ───────────────
# Remove the bucketStart/bucketOf/bucket/_ lines entirely — simplified trend
old_trend_body = '''    if (period == 'today') {
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

    final disease = List<double>.filled(bucketCount, 0.0);
    final pest    = List<double>.filled(bucketCount, 0.0);
    final water   = List<double>.filled(bucketCount, 0.0);

    for (final r in inspections) {
      // parse date back from formatted string — safe fallback
      final cat = r.category.toLowerCase();
      final bucket = 0; // simplified: distribute evenly (date parse optional)
      _ = bucket; // suppress unused warning
      if (cat.contains('disease')) disease[0]++;
      else if (cat.contains('pest')) pest[0]++;
      else if (cat.contains('water')) water[0]++;
    }'''

new_trend_body = '''    if (period == 'today') {
      labels = ['6am','8am','10am','12pm','2pm','4pm','6pm'];
      bucketCount = 7;
    } else if (period == '7days') {
      labels = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
      bucketCount = 7;
    } else if (period == '30days') {
      labels = ['W1','W2','W3','W4','W5'];
      bucketCount = 5;
    } else {
      labels = ['M1','M2','M3'];
      bucketCount = 3;
    }

    final disease = List<double>.filled(bucketCount, 0.0);
    final pest    = List<double>.filled(bucketCount, 0.0);
    final water   = List<double>.filled(bucketCount, 0.0);

    for (final r in inspections) {
      final cat = r.category.toLowerCase();
      if (cat.contains('disease')) disease[0]++;
      else if (cat.contains('pest')) pest[0]++;
      else if (cat.contains('water')) water[0]++;
    }'''

rc = rc.replace(old_trend_body, new_trend_body)

# Also remove the now-unused variable declarations at top of _buildTrend
rc = rc.replace(
    "    late DateTime Function(int) bucketStart;\n    late int Function(DateTime) bucketOf;\n\n    ",
    "    "
)

# ── Fix 4: Fix Supabase query — build filter before .select().order() ─────────
old_query = '''  var query = db
      .from('inspection_reports')
      .select(\'\'\'
        id, submitted_at, started_at, variety_name, greenhouse_id,
        greenhouses!inner(code),
        user_profiles!scout_id(full_name),
        inspection_findings(category, severity)
      \'\'\')
      .gte('submitted_at', since.toIso8601String())
      .order('submitted_at', ascending: false);

  if (greenhouseId != null) {
    query = query.eq('greenhouse_id', greenhouseId);
  } else if (farmId != null) {
    query = query.eq('greenhouses.farm_id', farmId);
  }
  if (variety != null) query = query.eq('variety_name', variety);

  final rows = await query.limit(200);'''

new_query = '''  var q = db
      .from('inspection_reports')
      .select(\'\'\'
        id, submitted_at, started_at, variety_name, greenhouse_id,
        greenhouses!inner(code),
        user_profiles!scout_id(full_name),
        inspection_findings(category, severity)
      \'\'\')
      .gte('submitted_at', since.toIso8601String());

  if (greenhouseId != null) {
    q = q.eq('greenhouse_id', greenhouseId);
  } else if (farmId != null) {
    q = q.eq('greenhouses.farm_id', farmId);
  }
  if (variety != null) q = q.eq('variety_name', variety);

  final rows = await q.order('submitted_at', ascending: false).limit(200);'''

rc = rc.replace(old_query, new_query)
rp.write_text(rc, encoding='utf-8')
print('reports_screen.dart fixed')

# ── Fix 5: Add missing import to app_shell.dart ───────────────────────────────
sp = pathlib.Path('lib/shared/widgets/app_shell.dart')
sc = sp.read_text(encoding='utf-8')
if "import '../l10n/app_strings.dart'" not in sc:
    sc = sc.replace(
        "import '../providers/locale_provider.dart';",
        "import '../providers/locale_provider.dart';\nimport '../l10n/app_strings.dart';"
    )
# Remove the bad hide directive — scouting_screen no longer exports AppColors
sc = sc.replace(
    "import '../../features/scouting/presentation/scouting_screen.dart' hide AppColors;",
    "import '../../features/scouting/presentation/scouting_screen.dart';"
)
sp.write_text(sc, encoding='utf-8')
print('app_shell.dart fixed')

# ── Fix 6: Add missing import to scouting_screen.dart ────────────────────────
scp = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
scc = scp.read_text(encoding='utf-8')
if "import '../../../shared/l10n/app_strings.dart'" not in scc:
    scc = scc.replace(
        "import '../../../shared/providers/locale_provider.dart';",
        "import '../../../shared/providers/locale_provider.dart';\nimport '../../../shared/l10n/app_strings.dart';"
    )
scp.write_text(scc, encoding='utf-8')
print('scouting_screen.dart fixed')

print('ALL FIXES DONE')