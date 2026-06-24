import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

# 1. Add dateTime field to _Inspection
old_model = """class _Inspection {
  final String id, date, gh, variety, category, severity, inspectorId;
  const _Inspection({
    required this.id, required this.date, required this.gh,
    required this.variety, required this.category,
    required this.severity, required this.inspectorId,
  });

  factory _Inspection.fromRow(Map<String, dynamic> r) {
    final raw = r['submitted_at'] as String? ?? r['started_at'] as String? ?? '';
    String date = '';
    if (raw.isNotEmpty) {
      final dt = DateTime.tryParse(raw);
      if (dt != null) {
        const months = ['Jan','Feb','Mar','Apr','May','Jun',
                        'Jul','Aug','Sep','Oct','Nov','Dec'];
        date = '${dt.day.toString().padLeft(2,'0')} ${months[dt.month-1]} ${dt.year}';
      }
    }
    final findings = r['inspection_findings'] as List?;
    final topCat = findings != null && findings.isNotEmpty
        ? (findings.first['category'] as String? ?? 'Other') : 'Other';
    final topSev = findings != null && findings.isNotEmpty
        ? (findings.first['severity'] as String? ?? 'Low') : 'Low';
    final scoutId = r['scout_id']?.toString() ?? '';
    return _Inspection(
      id: r['id']?.toString() ?? '',
      date: date,
      gh: r['greenhouse_code'] as String? ?? r['greenhouse_id']?.toString() ?? '\u2014',
      variety: r['variety_name'] as String? ?? '\u2014',
      category: topCat, severity: topSev,
      inspectorId: scoutId.length >= 8 ? scoutId.substring(0, 8) : scoutId,
    );
  }
}"""

new_model = """class _Inspection {
  final String id, date, gh, variety, category, severity, inspectorId;
  final DateTime dateTime;
  const _Inspection({
    required this.id, required this.date, required this.gh,
    required this.variety, required this.category,
    required this.severity, required this.inspectorId,
    required this.dateTime,
  });

  factory _Inspection.fromRow(Map<String, dynamic> r) {
    final raw = r['submitted_at'] as String? ?? r['started_at'] as String? ?? '';
    String date = '';
    DateTime parsedDateTime = DateTime.now();
    if (raw.isNotEmpty) {
      final dt = DateTime.tryParse(raw);
      if (dt != null) {
        parsedDateTime = dt;
        const months = ['Jan','Feb','Mar','Apr','May','Jun',
                        'Jul','Aug','Sep','Oct','Nov','Dec'];
        date = '${dt.day.toString().padLeft(2,'0')} ${months[dt.month-1]} ${dt.year}';
      }
    }
    final findings = r['inspection_findings'] as List?;
    final topCat = findings != null && findings.isNotEmpty
        ? (findings.first['category'] as String? ?? 'Other') : 'Other';
    final topSev = findings != null && findings.isNotEmpty
        ? (findings.first['severity'] as String? ?? 'Low') : 'Low';
    final scoutId = r['scout_id']?.toString() ?? '';
    return _Inspection(
      id: r['id']?.toString() ?? '',
      date: date,
      dateTime: parsedDateTime,
      gh: r['greenhouse_code'] as String? ?? r['greenhouse_id']?.toString() ?? '\u2014',
      variety: r['variety_name'] as String? ?? '\u2014',
      category: topCat, severity: topSev,
      inspectorId: scoutId.length >= 8 ? scoutId.substring(0, 8) : scoutId,
    );
  }
}"""

if old_model not in text:
    raise SystemExit("_Inspection anchor not found - aborting, no changes made.")
text = text.replace(old_model, new_model, 1)

# 2. Fix _buildTrend bucketing
old_trend = """  static Map<String,List<dynamic>> _buildTrend(List<_Inspection> ins, String period) {
    late List<String> labels; late int n;
    if (period=='today') { labels=['6am','8am','10am','12pm','2pm','4pm','6pm']; n=7; }
    else if (period=='30days') { labels=['W1','W2','W3','W4','W5']; n=5; }
    else if (period=='3months') { labels=['M1','M2','M3']; n=3; }
    else { labels=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']; n=7; }
    final d=List<double>.filled(n,0.0), p=List<double>.filled(n,0.0), w=List<double>.filled(n,0.0);
    for (final r in ins) {
      final cat=r.category.toLowerCase();
      if (cat.contains('disease')) { d[0]++; }
      else if (cat.contains('pest')) { p[0]++; }
      else if (cat.contains('water')) { w[0]++; }
    }
    return {'disease':d,'pest':p,'water':w,'labels':labels};
  }"""

new_trend = """  static Map<String,List<dynamic>> _buildTrend(List<_Inspection> ins, String period) {
    late List<String> labels; late int n;
    if (period=='today') { labels=['6am','8am','10am','12pm','2pm','4pm','6pm']; n=7; }
    else if (period=='30days') { labels=['W1','W2','W3','W4','W5']; n=5; }
    else if (period=='3months') { labels=['M1','M2','M3']; n=3; }
    else { labels=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']; n=7; }
    final now=DateTime.now();
    late DateTime since;
    switch(period){
      case 'today':   since=DateTime(now.year,now.month,now.day); break;
      case '30days':  since=now.subtract(const Duration(days:30)); break;
      case '3months': since=now.subtract(const Duration(days:90)); break;
      default:        since=now.subtract(const Duration(days:7));
    }
    final d=List<double>.filled(n,0.0), p=List<double>.filled(n,0.0), w=List<double>.filled(n,0.0);
    for (final r in ins) {
      int idx;
      if (period=='today') {
        idx=((r.dateTime.hour-6)/2).floor().clamp(0,n-1);
      } else if (period=='30days') {
        idx=(r.dateTime.difference(since).inDays/7).floor().clamp(0,n-1);
      } else if (period=='3months') {
        idx=(r.dateTime.difference(since).inDays/30).floor().clamp(0,n-1);
      } else {
        idx=(r.dateTime.weekday-1).clamp(0,n-1);
      }
      final cat=r.category.toLowerCase();
      if (cat.contains('disease')) { d[idx]++; }
      else if (cat.contains('pest')) { p[idx]++; }
      else if (cat.contains('water')) { w[idx]++; }
    }
    return {'disease':d,'pest':p,'water':w,'labels':labels};
  }"""

if old_trend not in text:
    raise SystemExit("_buildTrend anchor not found - aborting, no changes made.")
text = text.replace(old_trend, new_trend, 1)

p.write_text(text, encoding='utf-8')
print("reports_screen.dart updated: dateTime field added, _buildTrend bucketing fixed.")