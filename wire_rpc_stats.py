import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

# 1. Add fromRpcJson factory right after _ReportStats.empty()
old_empty = """  static _ReportStats empty() => const _ReportStats(
    total:0, disease:0, pest:0, critical:0,
    byCategory:{}, bySeverity:{}, topGreenhouses:[],
    trendDisease:[0,0,0,0,0,0,0], trendPest:[0,0,0,0,0,0,0],
    trendWater:[0,0,0,0,0,0,0],
    chartLabels:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
  );"""

new_empty = """  static _ReportStats empty() => const _ReportStats(
    total:0, disease:0, pest:0, critical:0,
    byCategory:{}, bySeverity:{}, topGreenhouses:[],
    trendDisease:[0,0,0,0,0,0,0], trendPest:[0,0,0,0,0,0,0],
    trendWater:[0,0,0,0,0,0,0],
    chartLabels:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
  );

  factory _ReportStats.fromRpcJson(Map<String,dynamic> json, String period) {
    late List<String> labels; late int n;
    if (period=='today') { labels=['6am','8am','10am','12pm','2pm','4pm','6pm']; n=7; }
    else if (period=='30days') { labels=['W1','W2','W3','W4','W5']; n=5; }
    else if (period=='3months') { labels=['M1','M2','M3']; n=3; }
    else { labels=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']; n=7; }

    final d=List<double>.filled(n,0.0), p=List<double>.filled(n,0.0), w=List<double>.filled(n,0.0);
    final trendList=json['trend'] as List? ?? [];
    for (final t in trendList) {
      final idx=(t['idx'] as num).toInt().clamp(0,n-1);
      d[idx]=(t['disease'] as num? ?? 0).toDouble();
      p[idx]=(t['pest'] as num? ?? 0).toDouble();
      w[idx]=(t['water'] as num? ?? 0).toDouble();
    }

    final byCatRaw=json['by_category'] as Map<String,dynamic>? ?? {};
    final byCategory=byCatRaw.map((k,v)=>MapEntry(k,(v as num).toInt()));

    final bySevRaw=json['by_severity'] as Map<String,dynamic>? ?? {};
    final bySeverity=bySevRaw.map((k,v)=>MapEntry(k,(v as num).toInt()));

    final topGhRaw=json['top_greenhouses'] as List? ?? [];
    final topGreenhouses=topGhRaw.map((g)=>_GhRank(
      g['gh'] as String? ?? '\u2014',
      (g['findings'] as num? ?? 0).toInt(),
      g['top_issue'] as String? ?? 'Other',
    )).toList();

    return _ReportStats(
      total:(json['total'] as num? ?? 0).toInt(),
      disease:(json['disease'] as num? ?? 0).toInt(),
      pest:(json['pest'] as num? ?? 0).toInt(),
      critical:(json['critical'] as num? ?? 0).toInt(),
      byCategory:byCategory, bySeverity:bySeverity,
      topGreenhouses:topGreenhouses,
      trendDisease:d, trendPest:p, trendWater:w,
      chartLabels:labels,
    );
  }"""

if old_empty not in text:
    raise SystemExit("empty() anchor not found - aborting, no changes made.")
text = text.replace(old_empty, new_empty, 1)

# 2. Add the RPC fetch function right before the ReportsScreen class
old_class = "class ReportsScreen extends ConsumerStatefulWidget {"

new_class = """Future<Map<String,dynamic>> _fetchReportStatsRpc(String period,
    {String? farmId, String? greenhouseId, String? variety}) async {
  final db=Supabase.instance.client;
  final now=DateTime.now();
  late DateTime since;
  switch(period){
    case 'today':   since=DateTime(now.year,now.month,now.day); break;
    case '30days':  since=now.subtract(const Duration(days:30)); break;
    case '3months': since=now.subtract(const Duration(days:90)); break;
    default:        since=now.subtract(const Duration(days:7));
  }
  final result=await db.rpc('get_report_stats', params: {
    'p_since': since.toIso8601String(),
    'p_farm_id': farmId,
    'p_greenhouse_id': greenhouseId,
    'p_variety': variety,
    'p_period': period,
  });
  return result as Map<String,dynamic>;
}

class ReportsScreen extends ConsumerStatefulWidget {"""

if old_class not in text:
    raise SystemExit("ReportsScreen class anchor not found - aborting, no changes made.")
text = text.replace(old_class, new_class, 1)

# 3. Update _load() to fetch table rows and RPC stats in parallel
old_load = """  Future<void> _load() async {
    setState((){_loading=true;_error=null;_showAllInspections=false;});
    try {
      final data=await _fetchInspections(_period,
          farmId:_farmId,greenhouseId:_greenhouseId,variety:_variety);
      if(mounted) setState((){_inspections=data;_stats=_ReportStats.fromInspections(data,_period);_loading=false;});
    } catch(e){ if(mounted) setState((){_error=e.toString();_loading=false;}); }
  }"""

new_load = """  Future<void> _load() async {
    setState((){_loading=true;_error=null;_showAllInspections=false;});
    try {
      final results=await Future.wait([
        _fetchInspections(_period,farmId:_farmId,greenhouseId:_greenhouseId,variety:_variety),
        _fetchReportStatsRpc(_period,farmId:_farmId,greenhouseId:_greenhouseId,variety:_variety),
      ]);
      final data=results[0] as List<_Inspection>;
      final statsJson=results[1] as Map<String,dynamic>;
      if(mounted) setState((){
        _inspections=data;
        _stats=_ReportStats.fromRpcJson(statsJson,_period);
        _loading=false;
      });
    } catch(e){ if(mounted) setState((){_error=e.toString();_loading=false;}); }
  }"""

if old_load not in text:
    raise SystemExit("_load anchor not found - aborting, no changes made.")
text = text.replace(old_load, new_load, 1)

p.write_text(text, encoding='utf-8')
print("reports_screen.dart updated: KPIs/charts now powered by get_report_stats RPC, fetched in parallel with table rows.")