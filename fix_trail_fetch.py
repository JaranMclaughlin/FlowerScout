import pathlib, sys

p = pathlib.Path('lib/shared/trail/data/trail_repository.dart')
text = p.read_text(encoding='utf-8')

# Split getActiveTrails and getTrailHistory to fetch metadata only
# Points are already loaded lazily via getTrailById on tile tap

old_active = """  Future<List<ScoutTrail>> getActiveTrails() async {
    final res = await _db
        .from('scout_trails')
        .select('*, trail_points(*)')
        .filter('ended_at', 'is', null)
        .order('started_at', ascending: false);
    return _parseTrails(res as List);
  }"""

new_active = """  Future<List<ScoutTrail>> getActiveTrails() async {
    final res = await _db
        .from('scout_trails')
        .select('id, scout_id, scout_name, farm_id, greenhouse_id, report_id, started_at, ended_at')
        .filter('ended_at', 'is', null)
        .order('started_at', ascending: false);
    return _parseTrails(res as List, includePoints: false);
  }"""

old_history = """  Future<List<ScoutTrail>> getTrailHistory() async {
    final res = await _db
        .from('scout_trails')
        .select('*, trail_points(*)')
        .not('ended_at', 'is', null)
        .order('started_at', ascending: false)
        .limit(100);
    return _parseTrails(res as List);
  }"""

new_history = """  Future<List<ScoutTrail>> getTrailHistory() async {
    final res = await _db
        .from('scout_trails')
        .select('id, scout_id, scout_name, farm_id, greenhouse_id, report_id, started_at, ended_at')
        .not('ended_at', 'is', null)
        .order('started_at', ascending: false)
        .limit(100);
    return _parseTrails(res as List, includePoints: false);
  }"""

old_parse = """  List<ScoutTrail> _parseTrails(List<dynamic> rows) {
    return rows.map((row) {
      final m = row as Map<String, dynamic>;
      final points = _parsePoints(m['trail_points'] as List<dynamic>? ?? []);
      return ScoutTrail.fromMap(m, points: points);
    }).toList();
  }"""

new_parse = """  List<ScoutTrail> _parseTrails(List<dynamic> rows, {bool includePoints = true}) {
    return rows.map((row) {
      final m = row as Map<String, dynamic>;
      final points = includePoints
          ? _parsePoints(m['trail_points'] as List<dynamic>? ?? [])
          : const <TrailPoint>[];
      return ScoutTrail.fromMap(m, points: points);
    }).toList();
  }"""

for old, new in [(old_active, new_active), (old_history, new_history), (old_parse, new_parse)]:
    if old not in text:
        import sys; sys.exit(f"Anchor not found: {old[:60]}")
    text = text.replace(old, new)

p.write_text(text, encoding='utf-8')
print("trail_repository.dart: metadata-only fetch for list views.")