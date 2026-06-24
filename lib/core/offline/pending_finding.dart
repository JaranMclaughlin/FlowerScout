import 'package:hive/hive.dart';

class PendingReport extends HiveObject {
  String id = '';
  String scoutId = '';
  String greenhouseId = '';
  String varietyName = '';
  String startedAt = '';
  String submittedAt = '';
  int durationSeconds = 0;
  double? latitude;
  double? longitude;
  String? trailId;
  List<String> findingCategories = [];
  List<String> findingSeverities = [];
  List<String> findingIssues = [];
  List<String> findingPhotoUrls = [];
  int retryCount = 0;
}

class PendingReportAdapter extends TypeAdapter<PendingReport> {
  @override
  final int typeId = 0;

  @override
  PendingReport read(BinaryReader reader) {
    final numOfFields = reader.readByte();
    final fields = <int, dynamic>{
      for (int i = 0; i < numOfFields; i++) reader.readByte(): reader.read(),
    };
    return PendingReport()
      ..id = (fields[0] as String?) ?? ''
      ..scoutId = (fields[1] as String?) ?? ''
      ..greenhouseId = (fields[2] as String?) ?? ''
      ..varietyName = (fields[3] as String?) ?? ''
      ..startedAt = (fields[4] as String?) ?? ''
      ..submittedAt = (fields[5] as String?) ?? ''
      ..durationSeconds = (fields[6] as int?) ?? 0
      ..latitude = fields[7] as double?
      ..longitude = fields[8] as double?
      ..trailId = fields[9] as String?
      ..findingCategories = (fields[10] as List?)?.cast<String>() ?? []
      ..findingSeverities = (fields[11] as List?)?.cast<String>() ?? []
      ..findingIssues = (fields[12] as List?)?.cast<String>() ?? []
      ..findingPhotoUrls = (fields[13] as List?)?.cast<String>() ?? []
      ..retryCount = (fields[14] as int?) ?? 0;
  }

  @override
  void write(BinaryWriter writer, PendingReport obj) {
    writer
      ..writeByte(15)
      ..writeByte(0)..write(obj.id)
      ..writeByte(1)..write(obj.scoutId)
      ..writeByte(2)..write(obj.greenhouseId)
      ..writeByte(3)..write(obj.varietyName)
      ..writeByte(4)..write(obj.startedAt)
      ..writeByte(5)..write(obj.submittedAt)
      ..writeByte(6)..write(obj.durationSeconds)
      ..writeByte(7)..write(obj.latitude)
      ..writeByte(8)..write(obj.longitude)
      ..writeByte(9)..write(obj.trailId)
      ..writeByte(10)..write(obj.findingCategories)
      ..writeByte(11)..write(obj.findingSeverities)
      ..writeByte(12)..write(obj.findingIssues)
      ..writeByte(13)..write(obj.findingPhotoUrls)
      ..writeByte(14)..write(obj.retryCount);
  }

  @override
  int get hashCode => typeId.hashCode;

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is PendingReportAdapter &&
          runtimeType == other.runtimeType &&
          typeId == other.typeId;
}
