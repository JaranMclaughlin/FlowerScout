import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

# 1. Add pagination state fields
old_fields = """  String _activeFilter='all';
  bool _showAllInspections=false;
  List<_Inspection> _inspections=[];"""
new_fields = """  String _activeFilter='all';
  bool _showAllInspections=false;
  bool _loadingMore=false;
  bool _hasMore=true;
  static const _pageSize=50;
  List<_Inspection> _inspections=[];"""
if old_fields not in text:
    raise SystemExit("State fields anchor not found - aborting.")
text = text.replace(old_fields, new_fields, 1)

# 2. Replace _fetchInspections to support offset/limit via .range()
old_fetch = """Future<List<_Inspection>> _fetchInspections(String period,
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
  var q=db.from('inspection_reports').select('''
    id, submitted_at, started_at, variety_name, greenhouse_id, scout_id,
    greenhouses!inner(code),
    inspection_findings(category, severity)
  ''').gte('submitted_at',since.toIso8601String());
  if (greenhouseId!=null) { q=q.eq('greenhouse_id',greenhouseId); }
  else if (farmId!=null) { q=q.eq('greenhouses.farm_id',farmId); }
  if (variety!=null) { q=q.eq('variety_name',variety); }
  final rows=await q.order('submitted_at',ascending:false).limit(200);
  return (rows as List).map((r){
    final row=Map<String,dynamic>.from(r as Map);
    final gh=row['greenhouses'];
    if (gh is Map) row['greenhouse_code']=gh['code'];
    return _Inspection.fromRow(row);
  }).toList();
}"""

new_fetch = """Future<List<_Inspection>> _fetchInspections(String period,
    {String? farmId, String? greenhouseId, String? variety,
     int offset=0, int limit=50}) async {
  final db=Supabase.instance.client;
  final now=DateTime.now();
  late DateTime since;
  switch(period){
    case 'today':   since=DateTime(now.year,now.month,now.day); break;
    case '30days':  since=now.subtract(const Duration(days:30)); break;
    case '3months': since=now.subtract(const Duration(days:90)); break;
    default:        since=now.subtract(const Duration(days:7));
  }
  var q=db.from('inspection_reports').select('''
    id, submitted_at, started_at, variety_name, greenhouse_id, scout_id,
    greenhouses!inner(code),
    inspection_findings(category, severity)
  ''').gte('submitted_at',since.toIso8601String());
  if (greenhouseId!=null) { q=q.eq('greenhouse_id',greenhouseId); }
  else if (farmId!=null) { q=q.eq('greenhouses.farm_id',farmId); }
  if (variety!=null) { q=q.eq('variety_name',variety); }
  final rows=await q.order('submitted_at',ascending:false).range(offset,offset+limit-1);
  return (rows as List).map((r){
    final row=Map<String,dynamic>.from(r as Map);
    final gh=row['greenhouses'];
    if (gh is Map) row['greenhouse_code']=gh['code'];
    return _Inspection.fromRow(row);
  }).toList();
}"""

if old_fetch not in text:
    raise SystemExit("_fetchInspections anchor not found - aborting, no changes made.")
text = text.replace(old_fetch, new_fetch, 1)

# 3. Update _load() to fetch first page only, and add _loadMore()
old_load = """  Future<void> _load() async {
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

new_load = """  Future<void> _load() async {
    setState((){_loading=true;_error=null;_showAllInspections=false;_hasMore=true;});
    try {
      final results=await Future.wait([
        _fetchInspections(_period,farmId:_farmId,greenhouseId:_greenhouseId,variety:_variety,
          offset:0,limit:_pageSize),
        _fetchReportStatsRpc(_period,farmId:_farmId,greenhouseId:_greenhouseId,variety:_variety),
      ]);
      final data=results[0] as List<_Inspection>;
      final statsJson=results[1] as Map<String,dynamic>;
      if(mounted) setState((){
        _inspections=data;
        _hasMore=data.length==_pageSize;
        _stats=_ReportStats.fromRpcJson(statsJson,_period);
        _loading=false;
      });
    } catch(e){ if(mounted) setState((){_error=e.toString();_loading=false;}); }
  }

  Future<void> _loadMore() async {
    if(_loadingMore || !_hasMore) return;
    setState(()=>_loadingMore=true);
    try {
      final more=await _fetchInspections(_period,
        farmId:_farmId,greenhouseId:_greenhouseId,variety:_variety,
        offset:_inspections.length,limit:_pageSize);
      if(mounted) setState((){
        _inspections=[..._inspections,...more];
        _hasMore=more.length==_pageSize;
        _loadingMore=false;
      });
    } catch(e){ if(mounted) setState(()=>_loadingMore=false); }
  }"""

if old_load not in text:
    raise SystemExit("_load anchor not found - aborting, no changes made.")
text = text.replace(old_load, new_load, 1)

# 4. Update _buildInspectionTable to add "Load more" when expanded and more data exists
old_table_tail = """        else ...[
          _buildTableRows(displayRows),
          if(rows.length>5)
            InkWell(
              onTap:()=>setState(()=>_showAllInspections=!_showAllInspections),
              child:Padding(
                padding:const EdgeInsets.symmetric(vertical:14),
                child:Row(mainAxisAlignment:MainAxisAlignment.center,children:[
                  Text(_showAllInspections?'Show less':'Show all (${rows.length})',
                    style:const TextStyle(fontSize:12,fontWeight:FontWeight.w600,color:_P.forest)),
                  const SizedBox(width:4),
                  Icon(_showAllInspections?Icons.keyboard_arrow_up_rounded:Icons.keyboard_arrow_down_rounded,
                    size:16,color:_P.forest),
                ]),
              ),
            ),
        ],"""

new_table_tail = """        else ...[
          _buildTableRows(displayRows),
          if(rows.length>5)
            InkWell(
              onTap:()=>setState(()=>_showAllInspections=!_showAllInspections),
              child:Padding(
                padding:const EdgeInsets.symmetric(vertical:14),
                child:Row(mainAxisAlignment:MainAxisAlignment.center,children:[
                  Text(_showAllInspections?'Show less':'Show all (${rows.length})',
                    style:const TextStyle(fontSize:12,fontWeight:FontWeight.w600,color:_P.forest)),
                  const SizedBox(width:4),
                  Icon(_showAllInspections?Icons.keyboard_arrow_up_rounded:Icons.keyboard_arrow_down_rounded,
                    size:16,color:_P.forest),
                ]),
              ),
            ),
          if(_showAllInspections && _hasMore && _activeFilter=='all')
            InkWell(
              onTap:_loadingMore?null:_loadMore,
              child:Padding(
                padding:const EdgeInsets.symmetric(vertical:14),
                child:Row(mainAxisAlignment:MainAxisAlignment.center,children:[
                  if(_loadingMore)
                    const SizedBox(width:14,height:14,
                      child:CircularProgressIndicator(strokeWidth:2,color:_P.forest))
                  else
                    const Text('Load more',
                      style:TextStyle(fontSize:12,fontWeight:FontWeight.w600,color:_P.forest)),
                ]),
              ),
            ),
        ],"""

if old_table_tail not in text:
    raise SystemExit("Table tail anchor not found - aborting, no changes made.")
text = text.replace(old_table_tail, new_table_tail, 1)

p.write_text(text, encoding='utf-8')
print("reports_screen.dart updated: real pagination via .range(), with Load more button.")