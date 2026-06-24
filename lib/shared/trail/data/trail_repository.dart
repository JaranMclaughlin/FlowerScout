import 'package:supabase_flutter/supabase_flutter.dart';
import '../models/scout_trail.dart';

class TrailRepository {
  final SupabaseClient _db;
  const TrailRepository(this._db);

  Future<String> startTrail({
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
      if (reportId != null) 'report_id': reportId,
      if (farmId != null) 'farm_id': farmId,
      if (greenhouseId != null) 'greenhouse_id': greenhouseId,
    }).eq('id', trailId);
  }

  Future<void> deleteTrail(String trailId) async {
    await _db.from('scout_trails').delete().eq('id', trailId);
  }

  Future<List<ScoutTrail>> getActiveTrails() async {
    final res = await _db
        .from('scout_trails')
        .select('*, trail_points(*)')
        .filter('ended_at', 'is', null)
        .order('started_at', ascending: false);
    return _parseTrails(res as List<dynamic>);
  }

  Future<List<ScoutTrail>> getTrailHistory() async {
    final res = await _db
        .from('scout_trails')
        .select('*, trail_points(*)')
        .not('ended_at', 'is', null)
        .order('started_at', ascending: false)
        .limit(100);
    return _parseTrails(res as List<dynamic>);
  }

  Future<ScoutTrail> getTrailById(String trailId) async {
    final res = await _db
        .from('scout_trails')
        .select('*, trail_points(*)')
        .eq('id', trailId)
        .single();
    final points = _parsePoints(res['trail_points'] as List<dynamic>? ?? []);
    return ScoutTrail.fromMap(res as Map<String, dynamic>, points: points);
  }

  List<ScoutTrail> _parseTrails(List<dynamic> rows) {
    return rows.map((row) {
      final m = row as Map<String, dynamic>;
      final points = _parsePoints(m['trail_points'] as List<dynamic>? ?? []);
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
