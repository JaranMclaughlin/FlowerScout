import pathlib

p = pathlib.Path('lib/shared/trail/data/trail_repository.dart')
text = p.read_text(encoding='utf-8')

old = """  Future<String> startTrail({
    required String scoutId,
    String? farmId,
    String? greenhouseId,
  }) async {
    final profileRes = await _db
        .from('user_profiles')
        .select('full_name')
        .eq('id', scoutId)
        .maybeSingle();
    final scoutName = profileRes?['full_name'] as String?;

    final res = await _db.from('scout_trails').insert({
      'scout_id': scoutId,
      'scout_name': scoutName,
      'farm_id': farmId,
      'greenhouse_id': greenhouseId,
      'started_at': DateTime.now().toIso8601String(),
    }).select('id').single();

    return res['id'] as String;
  }"""

new = """  Future<String> startTrail({
    required String scoutId,
    String? farmId,
    String? greenhouseId,
    String? scoutName,
  }) async {
    final res = await _db.from('scout_trails').insert({
      'scout_id': scoutId,
      // ignore: use_null_aware_elements
      if (scoutName != null) 'scout_name': scoutName,
      // ignore: use_null_aware_elements
      if (farmId != null) 'farm_id': farmId,
      // ignore: use_null_aware_elements
      if (greenhouseId != null) 'greenhouse_id': greenhouseId,
      'started_at': DateTime.now().toIso8601String(),
    }).select('id').single();

    return res['id'] as String;
  }"""

if old not in text:
    import sys; sys.exit("Anchor not found.")
text = text.replace(old, new)
p.write_text(text, encoding='utf-8')
print("trail_repository.dart fixed.")