import '../database/database_service.dart';

class ScoutingRepository {
  static final ScoutingRepository instance =
      ScoutingRepository._();

  ScoutingRepository._();

  Future<int> createSession() async {
    final db = await DatabaseService.instance.database;

    return await db.insert(
      'scouting_sessions',
      {
        'start_time': DateTime.now().toIso8601String(),
        'end_time': null,
        'distance_m': 0,
        'duration_seconds': 0,
      },
    );
  }

  Future<void> addPoint({
    required int sessionId,
    required double latitude,
    required double longitude,
  }) async {
    final db = await DatabaseService.instance.database;

    await db.insert(
      'gps_points',
      {
        'session_id': sessionId,
        'latitude': latitude,
        'longitude': longitude,
        'timestamp': DateTime.now().toIso8601String(),
      },
    );
  }

  Future<void> endSession({
    required int sessionId,
    required double distanceMeters,
    required int durationSeconds,
  }) async {
    final db = await DatabaseService.instance.database;

    await db.update(
      'scouting_sessions',
      {
        'end_time': DateTime.now().toIso8601String(),
        'distance_m': distanceMeters,
        'duration_seconds': durationSeconds,
      },
      where: 'id = ?',
      whereArgs: [sessionId],
    );
  }
}
