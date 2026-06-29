import 'package:supabase_flutter/supabase_flutter.dart';
import '../models/scout_trail.dart';

class TrailRepository {
  final SupabaseClient _db;
  const TrailRepository(this._db);

  Future<String> startTrail({
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
  }

  Future<void> appendPoints(String trailId, List<TrailPoint> points) async {
    if (points.isEmpty) return;
    await _db.from('trail_points').insert(
      points.map((p) => p.toMap(trailId)).toList(),
    );
  }

  Future<void> endTrail(
    String trailId, {
    String? reportId,
    String? farmId,
    String? greenhouseId,
  }) async {
    await _db.from('scout_trails').update({
      'ended_at': DateTime.now().toIso8601String(),
      // ignore: use_null_aware_elements
      if (reportId != null) 'report_id': reportId,
      // ignore: use_null_aware_elements
      if (farmId != null) 'farm_id': farmId,
      // ignore: use_null_aware_elements
      if (greenhouseId != null) 'greenhouse_id': greenhouseId,
    }).eq('id', trailId);
  }

  /// Force-ends any trail older than [maxAge] that never got ended_at set.
  Future<void> endStaleTrails({Duration maxAge = const Duration(hours: 4)}) async {
    final cutoff = DateTime.now().subtract(maxAge).toIso8601String();
    await _db.from('scout_trails').update({
      'ended_at': DateTime.now().toIso8601String(),
    }).filter('ended_at', 'is', null).lt('started_at', cutoff);
  }

  Future<void> deleteTrail(String trailId) async {
    await _db.from('scout_trails').delete().eq('id', trailId);
  }

  Future<List<ScoutTrail>> getActiveTrails() async {
    final res = await _db
        .from('scout_trails')
        .select('id, scout_id, scout_name, farm_id, greenhouse_id, report_id, started_at, ended_at')
        .filter('ended_at', 'is', null)
        .order('started_at', ascending: false);
    return _parseTrails(res as List, includePoints: false);
  }

  Future<List<ScoutTrail>> getTrailHistory() async {
    final res = await _db
        .from('scout_trails')
        .select('id, scout_id, scout_name, farm_id, greenhouse_id, report_id, started_at, ended_at')
        .not('ended_at', 'is', null)
        .order('started_at', ascending: false)
        .limit(100);
    return _parseTrails(res as List, includePoints: false);
  }

  Future<ScoutTrail> getTrailById(String trailId) async {
    final res = await _db
        .from('scout_trails')
        .select('*, trail_points(*)')
        .eq('id', trailId)
        .single();
    final points = _parsePoints(res['trail_points'] as List<dynamic>? ?? []);
    // ignore: unnecessary_cast
    return ScoutTrail.fromMap(res as Map<String, dynamic>, points: points);
  }

  List<ScoutTrail> _parseTrails(List<dynamic> rows, {bool includePoints = true}) {
    return rows.map((row) {
      final m = row as Map<String, dynamic>;
      final points = includePoints
          ? _parsePoints(m['trail_points'] as List<dynamic>? ?? [])
          : const <TrailPoint>[];
      return ScoutTrail.fromMap(m, points: points);
    }).toList();
  }

  List<TrailPoint> _parsePoints(List<dynamic> rows) {
    final pts = rows
        .map((r) => TrailPoint.fromMap(r as Map<String, dynamic>))
        .toList();
    pts.sort((a, b) => a.sequence.compareTo(b.sequence));
    return pts;
  }
}


