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
