import pathlib

p = pathlib.Path('test/shared/analytics_data_test.dart')
p.parent.mkdir(parents=True, exist_ok=True)

content = """import 'package:flutter_test/flutter_test.dart';
import 'package:mobile/shared/providers/analytics_data.dart';

InspectionRecord _record({
  required DateTime dateTime,
  String category = 'Disease',
  String severity = 'High',
  String gh = 'GH01',
}) {
  return InspectionRecord(
    id: 'id',
    dateTime: dateTime,
    dateLabel: '',
    gh: gh,
    variety: 'TestVariety',
    category: category,
    severity: severity,
    inspectorId: 'scout1',
  );
}

void main() {
  group('ReportStats.fromInspections - trend bucketing', () {
    test('today: buckets by hour into 7 two-hour slots starting at 6am', () {
      final base = DateTime(2026, 6, 29);
      final records = [
        _record(dateTime: base.add(const Duration(hours: 7)), category: 'Disease'),
        _record(dateTime: base.add(const Duration(hours: 9)), category: 'Disease'),
        _record(dateTime: base.add(const Duration(hours: 17)), category: 'Pest'),
        _record(dateTime: base.add(const Duration(hours: 23)), category: 'Water Stress'),
      ];
      final stats = ReportStats.fromInspections(records, 'today', base);

      expect(stats.chartLabels, ['6am', '8am', '10am', '12pm', '2pm', '4pm', '6pm']);
      expect(stats.trendDisease[0], 1); // hour 7 -> idx 0
      expect(stats.trendDisease[1], 1); // hour 9 -> idx 1
      expect(stats.trendPest[5], 1);    // hour 17 -> idx 5
      expect(stats.trendWater[6], 1);   // hour 23 -> clamped to last slot (idx 6)
    });

    test('7days (default): buckets by weekday, Monday=0 .. Sunday=6', () {
      // 2026-06-29 is a Monday.
      final monday = DateTime(2026, 6, 29);
      final wednesday = DateTime(2026, 7, 1);
      final sunday = DateTime(2026, 7, 5);
      final records = [
        _record(dateTime: monday, category: 'Disease'),
        _record(dateTime: wednesday, category: 'Pest'),
        _record(dateTime: sunday, category: 'Water Stress'),
      ];
      final stats = ReportStats.fromInspections(records, '7days', monday);

      expect(stats.chartLabels, ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']);
      expect(stats.trendDisease[0], 1); // Monday -> idx 0
      expect(stats.trendPest[2], 1);    // Wednesday -> idx 2
      expect(stats.trendWater[6], 1);   // Sunday -> idx 6
    });

    test('30days: buckets by week (5 buckets), not all into bucket 0', () {
      final since = DateTime(2026, 6, 1);
      final records = [
        _record(dateTime: since.add(const Duration(days: 1)), category: 'Disease'),  // week 0
        _record(dateTime: since.add(const Duration(days: 10)), category: 'Disease'), // week 1
        _record(dateTime: since.add(const Duration(days: 25)), category: 'Disease'), // week 3
      ];
      final stats = ReportStats.fromInspections(records, '30days', since);

      expect(stats.chartLabels, ['W1', 'W2', 'W3', 'W4', 'W5']);
      expect(stats.trendDisease[0], 1);
      expect(stats.trendDisease[1], 1);
      expect(stats.trendDisease[3], 1);
      // This is the regression check: before the fix, ALL of these
      // landed in trendDisease[0] regardless of date.
      expect(stats.trendDisease.reduce((a, b) => a + b), 3);
      expect(stats.trendDisease[0] == 3, isFalse);
    });

    test('3months: buckets by month (3 buckets)', () {
      final since = DateTime(2026, 4, 1);
      final records = [
        _record(dateTime: since.add(const Duration(days: 5)), category: 'Pest'),  // month 0
        _record(dateTime: since.add(const Duration(days: 45)), category: 'Pest'), // month 1
        _record(dateTime: since.add(const Duration(days: 85)), category: 'Pest'), // month 2
      ];
      final stats = ReportStats.fromInspections(records, '3months', since);

      expect(stats.chartLabels, ['M1', 'M2', 'M3']);
      expect(stats.trendPest[0], 1);
      expect(stats.trendPest[1], 1);
      expect(stats.trendPest[2], 1);
    });

    test('empty input produces zeroed stats, not an exception', () {
      final stats = ReportStats.fromInspections([], '7days', DateTime(2026, 6, 29));
      expect(stats.total, 0);
      expect(stats.trendDisease, [0, 0, 0, 0, 0, 0, 0]);
      expect(stats.topGreenhouses, isEmpty);
    });
  });

  group('ReportStats.fromInspections - aggregate counts', () {
    test('counts disease/pest/critical correctly across mixed records', () {
      final now = DateTime(2026, 6, 29);
      final records = [
        _record(dateTime: now, category: 'Disease', severity: 'High'),
        _record(dateTime: now, category: 'Pest', severity: 'Critical'),
        _record(dateTime: now, category: 'Water Stress', severity: 'Low'),
      ];
      final stats = ReportStats.fromInspections(records, '7days', now);

      expect(stats.total, 3);
      expect(stats.disease, 1);
      expect(stats.pest, 1);
      expect(stats.critical, 1);
    });

    test('ranks greenhouses by finding count, descending', () {
      final now = DateTime(2026, 6, 29);
      final records = [
        _record(dateTime: now, gh: 'GH01', category: 'Disease'),
        _record(dateTime: now, gh: 'GH01', category: 'Disease'),
        _record(dateTime: now, gh: 'GH02', category: 'Pest'),
      ];
      final stats = ReportStats.fromInspections(records, '7days', now);

      expect(stats.topGreenhouses.first.gh, 'GH01');
      expect(stats.topGreenhouses.first.findings, 2);
    });
  });

  group('AnalyticsFilter', () {
    test('two filters with identical fields are equal and share a hashCode', () {
      const a = AnalyticsFilter(period: '7days', farmId: 'farm1');
      const b = AnalyticsFilter(period: '7days', farmId: 'farm1');
      expect(a, equals(b));
      expect(a.hashCode, equals(b.hashCode));
    });

    test('filters with different farmId are not equal', () {
      const a = AnalyticsFilter(period: '7days', farmId: 'farm1');
      const b = AnalyticsFilter(period: '7days', farmId: 'farm2');
      expect(a == b, isFalse);
    });

    test('since() resolves correctly for each period', () {
      const today = AnalyticsFilter(period: 'today');
      const days30 = AnalyticsFilter(period: '30days');
      const days90 = AnalyticsFilter(period: '3months');
      const days7 = AnalyticsFilter(period: '7days');

      final now = DateTime.now();
      expect(today.since.day, now.day);
      expect(today.since.hour, 0);
      expect(now.difference(days30.since).inDays, 30);
      expect(now.difference(days90.since).inDays, 90);
      expect(now.difference(days7.since).inDays, 7);
    });
  });
}
"""

p.write_text(content, encoding='utf-8')
print(f"Created {p} ({len(content)} chars)")