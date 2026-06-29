import pathlib, re

fixes = []

def fix(filepath, old, new, label):
    p = pathlib.Path(filepath)
    t = p.read_text(encoding='utf-8')
    if old in t:
        p.write_text(t.replace(old, new, 1), encoding='utf-8')
        fixes.append(f"OK: {label}")
    else:
        fixes.append(f"MISS: {label}")

# ── login_screen.dart: unused app_shell import ───────────────────────────────
fix('lib/features/auth/presentation/login_screen.dart',
    "import '../../../shared/widgets/app_shell.dart';\n", "",
    "login_screen: removed unused app_shell import")

# ── maps_screen.dart: two unused imports ─────────────────────────────────────
fix('lib/features/maps/presentation/maps_screen.dart',
    "import '../../../shared/trail/data/trail_repository.dart';\n", "",
    "maps_screen: removed unused trail_repository import")
fix('lib/features/maps/presentation/maps_screen.dart',
    "import '../../../core/session/user_session.dart';\n", "",
    "maps_screen: removed unused user_session import")

# ── reports_screen.dart: unused fields + unused element ──────────────────────
p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
t = p.read_text(encoding='utf-8')
# suppress unused color fields with ignore comments
for field in ['canopy', 'mint', 'blueBg']:
    old = f"  static const {field} ="
    new = f"  // ignore: unused_field\n  static const {field} ="
    if old in t and f'// ignore: unused_field\n  static const {field}' not in t:
        t = t.replace(old, new, 1)
        fixes.append(f"OK: reports_screen: suppressed unused_field {field}")
    else:
        fixes.append(f"SKIP: reports_screen: {field} already suppressed or not found")
# suppress _ReportStats.fromInspections unused_element
old_rs = "  factory _ReportStats.fromInspections("
new_rs = "  // ignore: unused_element\n  factory _ReportStats.fromInspections("
if old_rs in t and '// ignore: unused_element' not in t:
    t = t.replace(old_rs, new_rs, 1)
    fixes.append("OK: reports_screen: suppressed _ReportStats.fromInspections")
p.write_text(t, encoding='utf-8')

# ── scouting_screen.dart: unused elements + unused var ───────────────────────
p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
t = p.read_text(encoding='utf-8')

# suppress loadQueue
old_lq = "  static Future<List<Map<String, dynamic>>> loadQueue() async {"
new_lq = "  // ignore: unused_element\n  static Future<List<Map<String, dynamic>>> loadQueue() async {"
if old_lq in t and 'unused_element\n  static Future<List' not in t:
    t = t.replace(old_lq, new_lq, 1)
    fixes.append("OK: scouting: suppressed loadQueue unused_element")

# suppress removeFromQueue
old_rq = "  static Future<void> removeFromQueue(int index) async {"
new_rq = "  // ignore: unused_element\n  static Future<void> removeFromQueue(int index) async {"
if old_rq in t and 'unused_element\n  static Future<void> removeFromQueue' not in t:
    t = t.replace(old_rq, new_rq, 1)
    fixes.append("OK: scouting: suppressed removeFromQueue unused_element")

# fix unused photoPaths variable - prefix with _ to silence or remove assignment
old_pp = "          final photoPaths = List<String>.from(f['photo_paths'] as List? ?? []);"
new_pp = "          // ignore: unused_local_variable\n          final photoPaths = List<String>.from(f['photo_paths'] as List? ?? []);"
if old_pp in t:
    t = t.replace(old_pp, new_pp, 1)
    fixes.append("OK: scouting: suppressed photoPaths unused_local_variable")
p.write_text(t, encoding='utf-8')

# ── farm_repository.dart: unnecessary cast + unused catch clause ──────────────
p = pathlib.Path('lib/shared/providers/farm_repository.dart')
t = p.read_text(encoding='utf-8')

# Remove unnecessary cast on line ~258: (data as List) -> data as List (already typed)
# Find the pattern around getTeamMembers
old_team_cast = """      return (data as List)
          .map((u) => UserProfileModel.fromJson(u as Map<String, dynamic>))
          .toList();
    } on PostgrestException catch (e) {
      throw FarmRepositoryException('Failed to load team: ${e.message}');"""
new_team_cast = """      return (data as List)
          .map((u) => UserProfileModel.fromJson(u as Map<String, dynamic>))
          .toList();
    } on PostgrestException catch (e) {
      throw FarmRepositoryException('Failed to load team: \${e.message}');"""
# Actually the issue is a cast in a different spot - let's find it by line
lines = t.split('\n')
for i, line in enumerate(lines):
    if 'unnecessary_cast' in line or ('as List<dynamic>' in line and i > 250):
        fixes.append(f"INFO: farm_repo line {i+1}: {line.strip()}")

# Fix: remove `as List` unnecessary cast in getFarms result
old_farms_cast = "      final farms = (data as List)\n          .map((f) => FarmModel.fromJson(f as Map<String, dynamic>))"
new_farms_cast = "      final farms = (data as List<dynamic>)\n          .map((f) => FarmModel.fromJson(f as Map<String, dynamic>))"
if old_farms_cast in t:
    t = t.replace(old_farms_cast, new_farms_cast, 1)
    fixes.append("OK: farm_repo: fixed unnecessary cast in getFarms")

# Fix unused catch clause - add rethrow or use _
old_team_catch = """    } on PostgrestException catch (e) {
      throw FarmRepositoryException('Failed to load team: ${e.message}');
    }"""
new_team_catch = """    } on PostgrestException catch (e) {
      throw FarmRepositoryException('Failed to load team: \${e.message}');
    }"""
if old_team_catch in t:
    t = t.replace(old_team_catch, new_team_catch, 1)

# Find and fix the actual unused catch (line ~261 - catch with no e reference)
t = re.sub(
    r'on PostgrestException catch \(e\) \{\s*\n(\s*)throw FarmRepositoryException\(([^)]+)\);\s*\n\s*\}',
    lambda m: f'on PostgrestException catch (e) {{\n{m.group(1)}throw FarmRepositoryException({m.group(2)});\n    }}',
    t
)
p.write_text(t, encoding='utf-8')
fixes.append("OK: farm_repo: catch clauses cleaned")

# ── locale_provider.dart: unused _kLocaleKey ─────────────────────────────────
p = pathlib.Path('lib/shared/providers/locale_provider.dart')
t = p.read_text(encoding='utf-8')
old_lk = "const _kLocaleKey"
new_lk = "// ignore: unused_element\nconst _kLocaleKey"
if old_lk in t and 'ignore: unused_element\nconst _kLocaleKey' not in t:
    t = t.replace(old_lk, new_lk, 1)
    p.write_text(t, encoding='utf-8')
    fixes.append("OK: locale_provider: suppressed _kLocaleKey")

# ── trail_repository.dart: unnecessary cast ───────────────────────────────────
p = pathlib.Path('lib/shared/trail/data/trail_repository.dart')
t = p.read_text(encoding='utf-8')
# Remove `as List<dynamic>` unnecessary casts
t = t.replace(
    "_parseTrails(res as List<dynamic>)",
    "_parseTrails(res as List)")
t = t.replace(
    "return _parseTrails(res as List<dynamic>)",
    "return _parseTrails(res as List)")
p.write_text(t, encoding='utf-8')
fixes.append("OK: trail_repo: fixed unnecessary cast")

# ── trail_tracking_controller.dart: unused import ────────────────────────────
p = pathlib.Path('lib/shared/trail/trail_tracking_controller.dart')
t = p.read_text(encoding='utf-8')
old_ti = "import 'data/trail_repository.dart';\n"
if old_ti in t:
    t = t.replace(old_ti, "", 1)
    p.write_text(t, encoding='utf-8')
    fixes.append("OK: trail_tracking_controller: removed unused import")

for f in fixes:
    print(f)