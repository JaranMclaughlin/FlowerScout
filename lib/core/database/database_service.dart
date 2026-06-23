import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

class DatabaseService {
  static final DatabaseService instance =
      DatabaseService._();

  DatabaseService._();

  Database? _db;

  Future<Database> get database async {
    if (_db != null) return _db!;
    _db = await _initDb();
    return _db!;
  }

  Future<Database> _initDb() async {
    final dbPath = await getDatabasesPath();

    final path = join(
      dbPath,
      'flowerscout.db',
    );

    return openDatabase(
      path,
      version: 1,
      onCreate: (db, version) async {

        await db.execute('''
CREATE TABLE scouting_sessions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
start_time TEXT,
end_time TEXT,
distance_m REAL,
duration_seconds INTEGER
)
''');

        await db.execute('''
CREATE TABLE gps_points(
id INTEGER PRIMARY KEY AUTOINCREMENT,
session_id INTEGER,
latitude REAL,
longitude REAL,
timestamp TEXT
)
''');
      },
    );
  }
}
