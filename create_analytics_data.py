import pathlib

p = pathlib.Path('lib/shared/providers/analytics_data.dart')
p.parent.mkdir(parents=True, exist_ok=True)

content = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'farm_providers.dart';

// ── Models ──────────────────────────────────────────────────────────────

class InspectionRecord {
  final String id;
  final DateTime dateTime;
  final String dateLabel;
  final String gh;
  final String variety;
  final String category;
  final String severity;
  final String inspectorId;

  const InspectionRecord({
    required this.id,
    required this.dateTime,
    required this.dateLabel,
    required this.gh,
    required this.variety,
    required this.category,
    required this.severity,
    required this.inspectorId,
  });

  factory InspectionRecord.fromRow(Map<String, dynamic> r) {
    final raw = r['submitted_at'] as String? ?? r['started_at'] as String? ?? '';
    DateTime dt = DateTime.now();
    String label = '';
    if (raw.isNotEmpty) {
      final parsed = DateTime.tryParse(raw);
      if (parsed != null) {
        dt = parsed;
        const months = ['Jan','Feb','Mar','Apr','May','Jun',
                        'Jul','Aug','Sep','Oct','Nov','Dec'];
        label = '${dt.day.toString().padLeft(2,'0')} ${months[dt.month-1]} ${dt.year}';
      }
    }
    final findings = r['inspection_findings'] as List?;
    final topCat = findings != null && findings.isNotEmpty
        ? (findings.first['category'] as String? ?? 'Other') : 'Other';
    final topSev = findings != null && findings.isNotEmpty
        ? (findings.first['severity'] as String? ?? 'Low') : 'Low';
    final scoutId = r['scout_id']?.toString() ?? '';
    return InspectionRecord(
      id: r['id']?.toString() ?? '',
      dateTime: dt,
      dateLabel: label,
      gh: r['greenhouse_code'] as String? ?? r['greenhouse_id']?.toString() ?? '—',
      variety: r['variety_name'] as String? ?? '—',
      category: topCat,
      severity: topSev,
      inspectorId: scoutId.length >= 8 ? scoutId.substring(0, 8) : scoutId,
    );
  }
}

class GreenhouseRank {
  final String gh;
  final int findings;
  final String topIssue;
  const GreenhouseRank(this.gh, this.findings, this.topIssue);
}

class ReportStats {
  final int total, disease, pest, critical;
  final Map<String, int> byCategory, bySeverity;
  final List<GreenhouseRank> topGreenhouses;
  final List<double> trendDisease, trendPest, trendWater;
  final List<String> chartLabels;

  const ReportStats({
    required this.total, required this.disease, required this.pest,
    required this.critical, required this.byCategory, required this.bySeverity,
    required this.topGreenhouses, required this.trendDisease,
    required this.trendPest, required this.trendWater, required this.chartLabels,
  });

  static ReportStats empty() => const ReportStats(
    total: 0, disease: 0, pest: 0, critical: 0,
    byCategory: {}, bySeverity: {}, topGreenhouses: [],
    trendDisease: [0,0,0,0,0,0,0], trendPest: [0,0,0,0,0,0,0],
    trendWater: [0,0,0,0,0,0,0],
    chartLabels: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
  );

  factory ReportStats.fromInspections(
    List<InspectionRecord> ins, String period, DateTime since,
  ) {
    int disease = 0, pest = 0, critical = 0;
    final byCategory = <String, int>{};
    final bySeverity = <String, int>{};
    final byGh = <String, Map<String, int>>{};

    for (final r in ins) {
      final cat = r.category.toLowerCase();
      final sev = r.severity.toLowerCase();
      if (cat.contains('disease')) disease++;
      if (cat.contains('pest')) pest++;
      if (sev == 'critical') critical++;
      byCategory[r.category] = (byCategory[r.category] ?? 0) + 1;
      bySeverity[r.severity] = (bySeverity[r.severity] ?? 0) + 1;
      byGh.putIfAbsent(r.gh, () => {});
      byGh[r.gh]![r.category] = (byGh[r.gh]![r.category] ?? 0) + 1;
    }

    final topGh = byGh.entries.map((e) {
      final tot = e.value.values.fold(0, (a, b) => a + b);
      final top = e.value.entries.reduce((a, b) => a.value >= b.value ? a : b);
      return GreenhouseRank(e.key, tot, top.key);
    }).toList()
      ..sort((a, b) => b.findings.compareTo(a.findings));

    final buckets = _buildTrend(ins, period, since);

    return ReportStats(
      total: ins.length, disease: disease, pest: pest, critical: critical,
      byCategory: byCategory, bySeverity: bySeverity,
      topGreenhouses: topGh.take(5).toList(),
      trendDisease: List<double>.from(buckets['disease']!),
      trendPest: List<double>.from(buckets['pest']!),
      trendWater: List<double>.from(buckets['water']!),
      chartLabels: List<String>.from(buckets['labels']!),
    );
  }

  static Map<String, List<dynamic>> _buildTrend(
    List<InspectionRecord> ins, String period, DateTime since,
  ) {
    late List<String> labels;
    late int n;
    if (period == 'today') {
      labels = ['6am','8am','10am','12pm','2pm','4pm','6pm']; n = 7;
    } else if (period == '30days') {
      labels = ['W1','W2','W3','W4','W5']; n = 5;
    } else if (period == '3months') {
      labels = ['M1','M2','M3']; n = 3;
    } else {
      labels = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']; n = 7;
    }

    final d = List<double>.filled(n, 0.0);
    final p = List<double>.filled(n, 0.0);
    final w = List<double>.filled(n, 0.0);

    for (final r in ins) {
      int idx;
      if (period == 'today') {
        idx = ((r.dateTime.hour - 6) / 2).floor().clamp(0, n - 1);
      } else if (period == '30days') {
        final days = r.dateTime.difference(since).inDays;
        idx = (days / 7).floor().clamp(0, n - 1);
      } else if (period == '3months') {
        final days = r.dateTime.difference(since).inDays;
        idx = (days / 30).floor().clamp(0, n - 1);
      } else {
        idx = (r.dateTime.weekday - 1).clamp(0, n - 1);
      }
      final cat = r.category.toLowerCase();
      if (cat.contains('disease')) {
        d[idx]++;
      } else if (cat.contains('pest')) {
        p[idx]++;
      } else if (cat.contains('water')) {
        w[idx]++;
      }
    }
    return {'disease': d, 'pest': p, 'water': w, 'labels': labels};
  }
}

class AnalyticsFilter {
  final String period;
  final String? farmId;
  final String? greenhouseId;
  final String? variety;

  const AnalyticsFilter({
    this.period = '7days',
    this.farmId,
    this.greenhouseId,
    this.variety,
  });

  DateTime get since {
    final now = DateTime.now();
    switch (period) {
      case 'today': return DateTime(now.year, now.month, now.day);
      case '30days': return now.subtract(const Duration(days: 30));
      case '3months': return now.subtract(const Duration(days: 90));
      default: return now.subtract(const Duration(days: 7));
    }
  }

  @override
  bool operator ==(Object other) =>
      other is AnalyticsFilter &&
      other.period == period &&
      other.farmId == farmId &&
      other.greenhouseId == greenhouseId &&
      other.variety == variety;

  @override
  int get hashCode => Object.hash(period, farmId, greenhouseId, variety);
}

// ── Fetcher ─────────────────────────────────────────────────────────────

Future<List<InspectionRecord>> fetchInspectionRecords(
  SupabaseClient db,
  AnalyticsFilter filter,
) async {
  var q = db.from('inspection_reports').select(\'\'\'
    id, submitted_at, started_at, variety_name, greenhouse_id, scout_id,
    greenhouses!inner(code, farm_id),
    inspection_findings(category, severity)
  \'\'\').gte('submitted_at', filter.since.toIso8601String());

  if (filter.greenhouseId != null) {
    q = q.eq('greenhouse_id', filter.greenhouseId!);
  } else if (filter.farmId != null) {
    q = q.eq('greenhouses.farm_id', filter.farmId!);
  }
  if (filter.variety != null) {
    q = q.eq('variety_name', filter.variety!);
  }

  final rows = await q.order('submitted_at', ascending: false).limit(500);
  return (rows as List).map((r) {
    final row = Map<String, dynamic>.from(r as Map);
    final ghData = row['greenhouses'];
    if (ghData is Map) {
      row['greenhouse_code'] = ghData['code'];
    }
    return InspectionRecord.fromRow(row);
  }).toList();
}

// ── Providers ───────────────────────────────────────────────────────────

final inspectionRecordsProvider =
    FutureProvider.family<List<InspectionRecord>, AnalyticsFilter>((ref, filter) async {
  final db = ref.watch(supabaseClientProvider);
  return fetchInspectionRecords(db, filter);
});

final reportStatsProvider =
    FutureProvider.family<ReportStats, AnalyticsFilter>((ref, filter) async {
  final records = await ref.watch(inspectionRecordsProvider(filter).future);
  return ReportStats.fromInspections(records, filter.period, filter.since);
});
"""

p.write_text(content, encoding='utf-8')
print(f"Created {p} ({len(content)} chars)")