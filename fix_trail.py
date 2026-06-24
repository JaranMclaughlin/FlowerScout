import os, pathlib

files = {}

files['lib/shared/trail/models/scout_trail.dart'] = r"""
class TrailPoint {
  final double lat;
  final double lng;
  final DateTime recordedAt;
  final double? accuracy;
  final int sequence;

  const TrailPoint({
    required this.lat,
    required this.lng,
    required this.recordedAt,
    this.accuracy,
    required this.sequence,
  });

  factory TrailPoint.fromMap(Map<String, dynamic> m) => TrailPoint(
        lat: (m['lat'] as num).toDouble(),
        lng: (m['lng'] as num).toDouble(),
        recordedAt: DateTime.parse(m['recorded_at'] as String),
        accuracy: m['accuracy'] != null ? (m['accuracy'] as num).toDouble() : null,
        sequence: m['sequence'] as int,
      );

  Map<String, dynamic> toMap(String trailId) => {
        'trail_id': trailId,
        'lat': lat,
        'lng': lng,
        'recorded_at': recordedAt.toIso8601String(),
        'accuracy': accuracy,
        'sequence': sequence,
      };
}

class ScoutTrail {
  final String id;
  final String scoutId;
  final String? scoutName;
  final String? farmId;
  final String? greenhouseId;
  final String? reportId;
  final DateTime startedAt;
  final DateTime? endedAt;
  final List<TrailPoint> points;

  const ScoutTrail({
    required this.id,
    required this.scoutId,
    this.scoutName,
    this.farmId,
    this.greenhouseId,
    this.reportId,
    required this.startedAt,
    this.endedAt,
    this.points = const [],
  });

  factory ScoutTrail.fromMap(Map<String, dynamic> m, {List<TrailPoint> points = const []}) =>
      ScoutTrail(
        id: m['id'] as String,
        scoutId: m['scout_id'] as String,
        scoutName: m['scout_name'] as String?,
        farmId: m['farm_id'] as String?,
        greenhouseId: m['greenhouse_id'] as String?,
        reportId: m['report_id'] as String?,
        startedAt: DateTime.parse(m['started_at'] as String),
        endedAt: m['ended_at'] != null ? DateTime.parse(m['ended_at'] as String) : null,
        points: points,
      );
}
""".lstrip()

files['lib/shared/trail/data/trail_repository.dart'] = r"""
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
""".lstrip()

files['lib/shared/trail/providers/trail_providers.dart'] = r"""
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/trail_repository.dart';
import '../models/scout_trail.dart';
import '../../providers/farm_providers.dart';

final trailRepositoryProvider = Provider<TrailRepository>((ref) {
  final db = ref.watch(supabaseClientProvider);
  return TrailRepository(db);
});

final activeTrailsProvider = FutureProvider<List<ScoutTrail>>((ref) {
  final repo = ref.watch(trailRepositoryProvider);
  return repo.getActiveTrails();
});

final trailHistoryProvider = FutureProvider<List<ScoutTrail>>((ref) {
  final repo = ref.watch(trailRepositoryProvider);
  return repo.getTrailHistory();
});

final trailByIdProvider =
    FutureProvider.family<ScoutTrail, String>((ref, trailId) {
  final repo = ref.watch(trailRepositoryProvider);
  return repo.getTrailById(trailId);
});
""".lstrip()

for path, content in files.items():
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Written:', path)

print('All done.')