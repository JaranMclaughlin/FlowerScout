  // ignore: unused_field
import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../../../shared/error/app_error_handler.dart';
import 'dart:typed_data';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;
import 'package:printing/printing.dart';
import 'package:share_plus/share_plus.dart';
import 'package:excel/excel.dart' hide Border;
import '../../../shared/theme/app_colors.dart';
import '../../../shared/providers/farm_providers.dart';
import '../../../shared/providers/farm_repository.dart';
import '../../../shared/providers/locale_provider.dart';
import '../../../shared/l10n/app_strings.dart';

// ── Palette ───────────────────────────────────────────────────────────────────

// ── Data models ───────────────────────────────────────────────────────────────
class _Inspection {
  final String id, date, gh, variety, category, severity, inspectorId, inspectorName;
  final DateTime dateTime;
  final List<Map<String,dynamic>> findings;
  const _Inspection({
    required this.id, required this.date, required this.gh,
    required this.variety, required this.category,
    required this.severity, required this.inspectorId,
    this.inspectorName = '',
    this.findings = const [],
    required this.dateTime,
  });

  factory _Inspection.fromRow(Map<String, dynamic> r, {String lang='en'}) {
    final raw = r['submitted_at'] as String? ?? r['started_at'] as String? ?? '';
    String date = '';
    DateTime parsedDateTime = DateTime.now();
    if (raw.isNotEmpty) {
      final dt = DateTime.tryParse(raw);
      if (dt != null) {
        parsedDateTime = dt;
        final months = AppStrings.of(lang).monthsShort;
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
      gh: r['greenhouse_code'] as String? ?? r['greenhouse_id']?.toString() ?? '—',
      variety: r['variety_name'] as String? ?? '—',
      category: topCat, severity: topSev,
      inspectorId: scoutId.length >= 8 ? scoutId.substring(0, 8) : scoutId,
      inspectorName: r['scout_name'] as String? ?? (r['user_profiles'] as Map?)?['full_name'] as String? ?? '',
      findings: (r['inspection_findings'] as List? ?? [])
          .map((f) => Map<String,dynamic>.from(f as Map)).toList(),
    );
  }
}

class _GhRank { final String gh, topIssue; final int findings;
  const _GhRank(this.gh, this.findings, this.topIssue); }

class _ReportStats {
  final int total, disease, pest, critical;
  final Map<String, int> byCategory, bySeverity;
  final List<_GhRank> topGreenhouses;
  final List<double> trendDisease, trendPest, trendWater;
  final List<String> chartLabels;
  const _ReportStats({
    required this.total, required this.disease, required this.pest,
    required this.critical, required this.byCategory, required this.bySeverity,
    required this.topGreenhouses, required this.trendDisease,
    required this.trendPest, required this.trendWater, required this.chartLabels,
  });
  static _ReportStats empty() => const _ReportStats(
    total:0, disease:0, pest:0, critical:0,
    byCategory:{}, bySeverity:{}, topGreenhouses:[],
    trendDisease:[0,0,0,0,0,0,0], trendPest:[0,0,0,0,0,0,0],
    trendWater:[0,0,0,0,0,0,0],
    chartLabels:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
  );

  factory _ReportStats.fromRpcJson(Map<String,dynamic> json, String period, {String lang='en'}) {
    late List<String> labels; late int n;
    final s=AppStrings.of(lang);
    if (period=='today') { labels=s.chartLabelsToday; n=7; }
    else if (period=='30days') { labels=s.chartLabels30Days; n=5; }
    else if (period=='3months') { labels=s.chartLabels3Months; n=3; }
    else { labels=s.chartLabelsWeek; n=7; }

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
      g['gh'] as String? ?? '—',
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
  }
  // ignore: unused_element
  factory _ReportStats.fromInspections(List<_Inspection> ins, String period, {String lang='en'}) {
    int disease=0, pest=0, critical=0;
    final byCategory=<String,int>{}, bySeverity=<String,int>{}, byGh=<String,Map<String,int>>{};
    for (final r in ins) {
      final cat=r.category.toLowerCase(), sev=r.severity.toLowerCase();
      if (cat.contains('disease')) disease++;
      if (cat.contains('pest')) pest++;
      if (sev=='critical') critical++;
      byCategory[r.category]=(byCategory[r.category]??0)+1;
      bySeverity[r.severity]=(bySeverity[r.severity]??0)+1;
      byGh.putIfAbsent(r.gh,()=>{});
      byGh[r.gh]![r.category]=(byGh[r.gh]![r.category]??0)+1;
    }
    final topGh=byGh.entries.map((e){
      final tot=e.value.values.fold(0,(a,b)=>a+b);
      final top=e.value.entries.reduce((a,b)=>a.value>=b.value?a:b);
      return _GhRank(e.key,tot,top.key);
    }).toList()..sort((a,b)=>b.findings.compareTo(a.findings));
    final buckets=_buildTrend(ins,period,lang);
    return _ReportStats(
      total:ins.length, disease:disease, pest:pest, critical:critical,
      byCategory:byCategory, bySeverity:bySeverity,
      topGreenhouses:topGh.take(3).toList(),
      trendDisease:List<double>.from(buckets['disease']!),
      trendPest:List<double>.from(buckets['pest']!),
      trendWater:List<double>.from(buckets['water']!),
      chartLabels:List<String>.from(buckets['labels']!),
    );
  }
  static Map<String,List<dynamic>> _buildTrend(List<_Inspection> ins, String period, String lang) {
    late List<String> labels; late int n;
    // chart labels handled in fromRpcJson
    if (period=='today') { labels=['6am','8am','10am','12pm','2pm','4pm','6pm']; n=7; }
    else if (period=='30days') { labels=['W1','W2','W3','W4','W5']; n=5; }
    else if (period=='3months') { labels=['M1','M2','M3']; n=3; }
    else { labels=AppStrings.of(lang).chartLabelsWeek; n=7; }
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
  }
}

// ── Fetcher ───────────────────────────────────────────────────────────────────
Future<List<_Inspection>> _fetchInspections(String period,
    {String? farmId, String? greenhouseId, String? variety,
     int offset=0, int limit=50, String lang='en'}) async {
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
    user_profiles!inspection_reports_scout_id_profiles_fkey(full_name),
    greenhouses!inner(code, farm_id),
    inspection_findings(category, severity, issue, photo_urls)
  ''').gte('submitted_at',since.toIso8601String());
  if (greenhouseId!=null) { q=q.eq('greenhouse_id',greenhouseId); }
  else if (farmId!=null) { q=q.eq('greenhouses.farm_id',farmId); }
  if (variety!=null) { q=q.eq('variety_name',variety); }
  final rows=await q.order('submitted_at',ascending:false).range(offset,offset+limit-1);
  return (rows as List).map((r){
    final row=Map<String,dynamic>.from(r as Map);
    final gh=row['greenhouses'];
    if (gh is Map) row['greenhouse_code']=gh['code'];
    return _Inspection.fromRow(row, lang: lang);
  }).toList();
}

// ── Screen ────────────────────────────────────────────────────────────────────
Future<Map<String,dynamic>> _fetchReportStatsRpc(String period,
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

class ReportsScreen extends ConsumerStatefulWidget {
  const ReportsScreen({super.key});
  @override ConsumerState<ReportsScreen> createState()=>_ReportsScreenState();
}

class _ReportsScreenState extends ConsumerState<ReportsScreen> {
  String _period='7days';
  String? _farmId, _greenhouseId, _variety;
  String _chartType='Bar';
  String _activeFilter='all';
  bool _showAllInspections=false;
  bool _loadingMore=false;
  bool _hasMore=true;
  static const _pageSize=50;
  List<_Inspection> _inspections=[];
  _ReportStats _stats=_ReportStats.empty();
  bool _loading=true;
  String? _error;

  @override void initState(){ super.initState(); _load(); }

  Future<void> _load() async {
    setState((){_loading=true;_error=null;_showAllInspections=false;_hasMore=true;});
    try {
      final results=await Future.wait([
        _fetchInspections(_period,farmId:_farmId,greenhouseId:_greenhouseId,variety:_variety,
          offset:0,limit:_pageSize,lang:ref.read(localeProvider)),
        _fetchReportStatsRpc(_period,farmId:_farmId,greenhouseId:_greenhouseId,variety:_variety),
      ]);
      final data=results[0] as List<_Inspection>;
      final statsJson=results[1] as Map<String,dynamic>;
      if(mounted) {
        setState((){
          _inspections=data;
          _hasMore=data.length==_pageSize;
          _stats=_ReportStats.fromRpcJson(statsJson,_period,lang:ref.read(localeProvider));
          _loading=false;
        });
      }
    } catch(e){ if(mounted) setState((){_error=e.toString();_loading=false;}); }
  }

  Future<void> _loadMore() async {
    if(_loadingMore || !_hasMore) return;
    setState(()=>_loadingMore=true);
    try {
      final more=await _fetchInspections(_period,
        farmId:_farmId,greenhouseId:_greenhouseId,variety:_variety,
        offset:_inspections.length,limit:_pageSize,lang:ref.read(localeProvider));
      if(mounted) {
        setState((){
          _inspections=[..._inspections,...more];
          _hasMore=more.length==_pageSize;
          _loadingMore=false;
        });
      }
    } catch(e){ if(mounted) setState(()=>_loadingMore=false); }
  }

  // Export needs every matching record, not just whatever page is loaded
  // on screen - fetch fresh, independent of the table's pagination state.
  Future<List<_Inspection>> _fetchAllForExport() async {
    const cap=2000, batch=200;
    final all=<_Inspection>[];
    int offset=0;
    while(true){
      final page=await _fetchInspections(_period,
          farmId:_farmId,greenhouseId:_greenhouseId,variety:_variety,
          offset:offset,limit:batch,lang:ref.read(localeProvider));
      all.addAll(page);
      if(page.length<batch || all.length>=cap) break;
      offset+=batch;
    }
    return all;
  }

  List<_Inspection> _applyActiveFilter(List<_Inspection> source) {
    if (_activeFilter=='all') return source;
    if (_activeFilter=='critical') return source.where((r)=>r.severity.toLowerCase()=='critical').toList();
    return source.where((r)=>r.category.toLowerCase().contains(_activeFilter)).toList();
  }
  List<_Inspection> get _filtered => _applyActiveFilter(_inspections);

  Color _catColor(String cat) {
    final c=cat.toLowerCase();
    if (c.contains('disease')) return AppColors.disease;
    if (c.contains('pest')) return AppColors.warning;
    if (c.contains('water')) return AppColors.info;
    if (c.contains('nutri')) return AppColors.leaf;
    if (c.contains('irrig')) return const Color(0xFF00838F);
    return AppColors.slate;
  }

  Color _sevColor(String s) => switch(s.toLowerCase()){
    'critical'=>const Color(0xFF7A1F1F),
    'high'=>AppColors.disease,
    'medium'=>AppColors.warning,
    _=>AppColors.leaf,
  };

  @override
  Widget build(BuildContext context) {
    final farmsAsync=ref.watch(farmsProvider);
    final s=ref.watch(stringsProvider);
    return Container(
      color: AppColors.background,
      child: farmsAsync.when(
        loading:()=>const Center(child:CircularProgressIndicator(color:AppColors.leaf)),
        error:(e,_)=>Center(child:Text('Error: $e')),
        data:(farms)=>RefreshIndicator(
          color:AppColors.leaf,
          onRefresh:_load,
          child:SingleChildScrollView(
            physics:const AlwaysScrollableScrollPhysics(),
            child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
              _buildHeader(s, farms),
              const SizedBox(height:24),
              Padding(
                padding:const EdgeInsets.symmetric(horizontal:24),
                child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                  if(_loading) _buildSkeleton()
                  else if(_error!=null) _buildError(s)
                  else ...[
                    _buildKpiRow(s),
                    const SizedBox(height:24),
                    _buildChartCard(s),
                    const SizedBox(height:24),
                    Row(crossAxisAlignment:CrossAxisAlignment.start,children:[
                      Expanded(flex:5,child:_buildSeverityCard(s)),
                      const SizedBox(width:16),
                      Expanded(flex:5,child:_buildTopGhCard(s)),
                    ]),
                    const SizedBox(height:24),
                    _buildCategoryCard(s),
                    const SizedBox(height:24),
                    _buildInspectionTable(s),
                  ],
                  const SizedBox(height:40),
                ]),
              ),
            ]),
          ),
        ),
      ),
    );
  }

  // ── Header with filters ──────────────────────────────────────────────────
  Widget _buildHeader(AppStrings s, List<FarmModel> farms) {
    final farmItems=<String,String?>{s.allFarms:null};
    for(final f in farms) { farmItems[f.name]=f.id; }
    final ghItems=<String,String?>{'All':null};
    if(_farmId!=null){
      final farm=farms.firstWhere((f)=>f.id==_farmId,orElse:()=>farms.first);
      for(final g in farm.greenhouses) { ghItems[g.code]=g.id; }
    }
    final varItems=<String,String?>{'All':null};
    if(_greenhouseId!=null){
      for(final f in farms) { for(final g in f.greenhouses){
        if(g.id==_greenhouseId) { for(final v in g.varietyNames) { varItems[v]=v; } }
      } }
    }
    final periodItems={s.today:'today',s.last7Days:'7days',s.last30Days:'30days',s.last3Months:'3months'};

    return Container(
      color:AppColors.surface,
      padding:const EdgeInsets.fromLTRB(24,24,24,20),
      child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
        Row(children:[
          Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
            Text(s.reportsAnalytics,
              style:const TextStyle(fontSize:26,fontWeight:FontWeight.w800,
                color:AppColors.ink,letterSpacing:-0.5)),
            const SizedBox(height:4),
            Text(s.reportsSubtitle,
              style:const TextStyle(fontSize:13,color:AppColors.slate)),
          ])),
          const SizedBox(width:16),
          _exportChip(Icons.picture_as_pdf_outlined,'PDF',AppColors.disease,()=>_showExport('pdf',s)),
          const SizedBox(width:8),
          _exportChip(Icons.table_chart_outlined,'Excel',AppColors.leaf,()=>_showExport('excel',s)),
          const SizedBox(width:8),
          _exportChip(Icons.share_rounded,'Share',const Color(0xFF25D366),()=>_shareWhatsApp(s)),
        ]),
        const SizedBox(height:20),
        const Divider(height:1,color:AppColors.divider),
        const SizedBox(height:16),
        SingleChildScrollView(scrollDirection:Axis.horizontal,
          child:Row(children:[
            _filterPill(s.dateRange,
              periodItems.entries.firstWhere((e)=>e.value==_period,
                orElse:()=>periodItems.entries.first).key,
              periodItems.keys.toList(),(v){
                _period=periodItems[v]!; _load();
              }),
            const SizedBox(width:10),
            _filterPill('Farm',
              farmItems.entries.firstWhere((e)=>e.value==_farmId,
                orElse:()=>farmItems.entries.first).key,
              farmItems.keys.toList(),(v){
                setState((){_farmId=farmItems[v!];_greenhouseId=null;_variety=null;});
                _load();
              }),
            const SizedBox(width:10),
            _filterPill('Greenhouse',
              ghItems.entries.firstWhere((e)=>e.value==_greenhouseId,
                orElse:()=>ghItems.entries.first).key,
              ghItems.keys.toList(),(v){
                setState((){_greenhouseId=ghItems[v!];_variety=null;});
                _load();
              }),
            const SizedBox(width:10),
            _filterPill('Variety',
              varItems.entries.firstWhere((e)=>e.value==_variety,
                orElse:()=>varItems.entries.first).key,
              varItems.keys.toList(),(v){
                setState(()=>_variety=varItems[v!]);
                _load();
              }),
          ])),
      ]),
    );
  }

  Widget _exportChip(IconData icon, String label, Color color, VoidCallback onTap)=>
    Material(color:color.withValues(alpha:0.08),borderRadius:BorderRadius.circular(8),
      child:InkWell(borderRadius:BorderRadius.circular(8),onTap:onTap,
        child:Padding(padding:const EdgeInsets.symmetric(horizontal:12,vertical:8),
          child:Row(mainAxisSize:MainAxisSize.min,children:[
            Icon(icon,size:15,color:color),
            const SizedBox(width:5),
            Text(label,style:TextStyle(fontSize:12,fontWeight:FontWeight.w600,color:color)),
          ]))));

  Widget _filterPill(String label, String value, List<String> items, ValueChanged<String?> onChanged)=>
    Container(
      padding:const EdgeInsets.symmetric(horizontal:12,vertical:6),
      decoration:BoxDecoration(color:AppColors.background,borderRadius:BorderRadius.circular(8),
        border:Border.all(color:AppColors.border)),
      child:DropdownButtonHideUnderline(child:DropdownButton<String>(
        value:items.contains(value)?value:items.first,
        isDense:true,
        style:const TextStyle(fontSize:12,color:AppColors.ink,fontWeight:FontWeight.w500),
        icon:const Icon(Icons.keyboard_arrow_down_rounded,size:16,color:AppColors.slate),
        items:items.map((e)=>DropdownMenuItem(value:e,child:Text(e))).toList(),
        onChanged:onChanged,
      )),
    );

  // ── KPI row ──────────────────────────────────────────────────────────────
  Widget _buildKpiRow(AppStrings s) {
    final kpis=[
      _KpiData(id:'all',    label:s.inspections, value:_stats.total,
        icon:Icons.assignment_outlined,      color:AppColors.forest,  bg:AppColors.mist),
      _KpiData(id:'disease',label:s.disease,     value:_stats.disease,
        icon:Icons.coronavirus_outlined,     color:AppColors.disease,     bg:AppColors.diseaseBg),
      _KpiData(id:'pest',   label:s.pests,       value:_stats.pest,
        icon:Icons.bug_report_outlined,      color:AppColors.warning,   bg:AppColors.warningBg),
      _KpiData(id:'critical',label:s.critical,   value:_stats.critical,
        icon:Icons.warning_amber_rounded,    color:const Color(0xFF7A1F1F), bg:const Color(0xFFFDE8E8)),
    ];
    return LayoutBuilder(builder:(_,con){
      if(con.maxWidth>600){
        return Row(children:kpis.expand((k)=>[
          Expanded(child:_kpiCard(k)),const SizedBox(width:12)]).toList()..removeLast());
      }
      return GridView.count(crossAxisCount:2,shrinkWrap:true,
        physics:const NeverScrollableScrollPhysics(),
        crossAxisSpacing:12,mainAxisSpacing:12,childAspectRatio:1.8,
        children:kpis.map((k)=>_kpiCard(k)).toList());
    });
  }

  Widget _kpiCard(_KpiData k) {
    final active=_activeFilter==k.id;
    return GestureDetector(
      onTap:()=>setState(()=>_activeFilter=k.id),
      child:AnimatedContainer(duration:const Duration(milliseconds:180),
        padding:const EdgeInsets.all(16),
        decoration:BoxDecoration(
          color:active?k.color:AppColors.surface,
          borderRadius:BorderRadius.circular(14),
          border:Border.all(color:active?k.color:AppColors.border,width:active?2:1),
          boxShadow:active?[BoxShadow(color:k.color.withValues(alpha:0.2),blurRadius:12,offset:const Offset(0,4))]:
            [BoxShadow(color:Colors.black.withValues(alpha:0.03),blurRadius:6,offset:const Offset(0,2))],
        ),
        child:Row(children:[
          Container(width:40,height:40,
            decoration:BoxDecoration(color:active?Colors.white.withValues(alpha:0.2):k.bg,
              borderRadius:BorderRadius.circular(10)),
            child:Icon(k.icon,color:active?Colors.white:k.color,size:20)),
          const SizedBox(width:12),
          Column(crossAxisAlignment:CrossAxisAlignment.start,mainAxisSize:MainAxisSize.min,children:[
            Text('${k.value}',style:TextStyle(fontSize:24,fontWeight:FontWeight.w800,
              color:active?Colors.white:AppColors.ink,height:1)),
            const SizedBox(height:2),
            Text(k.label,style:TextStyle(fontSize:11,color:active?Colors.white70:AppColors.slate,
              fontWeight:FontWeight.w500)),
          ]),
        ]),
      ),
    );
  }

  // ── Trend chart ───────────────────────────────────────────────────────────
  Widget _buildChartCard(AppStrings s) {
    return Container(
      padding:const EdgeInsets.all(20),
      decoration:_card(),
      child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
        Row(children:[
          Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
            Text(s.findingsTrend,
              style:const TextStyle(fontSize:15,fontWeight:FontWeight.w700,color:AppColors.ink)),
            const SizedBox(height:2),
            Text(s.findingsTrendSub,
              style:const TextStyle(fontSize:11,color:AppColors.slate)),
          ])),
          _segmented(),
        ]),
        const SizedBox(height:6),
        _legend(s),
        const SizedBox(height:16),
        SizedBox(height:200,
          child:_chartType=='Bar'?_barChart():_lineChart()),
      ]),
    );
  }

  Widget _segmented()=>Row(children:['Bar','Line'].map((t){
    final active=_chartType==t;
    return GestureDetector(
      onTap:()=>setState(()=>_chartType=t),
      child:Container(
        margin:const EdgeInsets.only(left:4),
        padding:const EdgeInsets.symmetric(horizontal:10,vertical:5),
        decoration:BoxDecoration(
          color:active?AppColors.forest:Colors.transparent,
          borderRadius:BorderRadius.circular(6),
          border:Border.all(color:active?AppColors.forest:AppColors.border),
        ),
        child:Text(t,style:TextStyle(fontSize:11,fontWeight:FontWeight.w600,
          color:active?Colors.white:AppColors.slate))));
  }).toList());

  Widget _legend(AppStrings s)=>Wrap(spacing:16,children:[
    (AppColors.leaf,s.disease),(AppColors.warning,s.pests),(AppColors.info,'Water'),
  ].map((i)=>Row(mainAxisSize:MainAxisSize.min,children:[
    Container(width:8,height:8,decoration:BoxDecoration(color:i.$1,shape:BoxShape.circle)),
    const SizedBox(width:4),
    Text(i.$2,style:const TextStyle(fontSize:11,color:AppColors.slate)),
  ])).toList());

  Widget _barChart(){
    final d=_stats; final labels=d.chartLabels;
    final maxY=[...d.trendDisease,...d.trendPest,...d.trendWater]
      .fold(0.0,(a,b)=>a>b?a:b)*1.3;
    return BarChart(BarChartData(
      alignment:BarChartAlignment.spaceAround,
      maxY:maxY<1?5:maxY,
      barTouchData:BarTouchData(enabled:false),
      gridData:FlGridData(drawVerticalLine:false,
        getDrawingHorizontalLine:(_)=>FlLine(color:AppColors.divider,strokeWidth:1)),
      borderData:FlBorderData(show:false),
      titlesData:FlTitlesData(
        leftTitles:AxisTitles(sideTitles:SideTitles(showTitles:false)),
        rightTitles:AxisTitles(sideTitles:SideTitles(showTitles:false)),
        topTitles:AxisTitles(sideTitles:SideTitles(showTitles:false)),
        bottomTitles:AxisTitles(sideTitles:SideTitles(showTitles:true,reservedSize:24,interval:1,
          getTitlesWidget:(v,_){
            final i=v.toInt();
            if(i<0||i>=labels.length) return const SizedBox();
            final lbl=labels[i].length>3?labels[i].substring(0,3):labels[i];
            return Padding(padding:const EdgeInsets.only(top:4),
              child:Text(lbl,style:const TextStyle(fontSize:9,color:AppColors.slate)));
          }))),
      barGroups:List.generate(labels.length,(i)=>BarChartGroupData(x:i,barRods:[
        BarChartRodData(toY:d.trendDisease[i],color:AppColors.leaf,width:4,borderRadius:BorderRadius.circular(3)),
        BarChartRodData(toY:d.trendPest[i],color:AppColors.warning,width:4,borderRadius:BorderRadius.circular(3)),
        BarChartRodData(toY:d.trendWater[i],color:AppColors.info,width:4,borderRadius:BorderRadius.circular(3)),
      ])),
    ));
  }

  Widget _lineChart(){
    final d=_stats; final labels=d.chartLabels;
    final maxY=[...d.trendDisease,...d.trendPest,...d.trendWater]
      .fold(0.0,(a,b)=>a>b?a:b)*1.3;
    series(List<double> v,Color c)=>LineChartBarData(
      spots:v.asMap().entries.map((e)=>FlSpot(e.key.toDouble(),e.value)).toList(),
      isCurved:true,color:c,barWidth:2,
      dotData:FlDotData(show:true,getDotPainter:(s,_,_,_)=>
        FlDotCirclePainter(radius:3,color:c,strokeWidth:0,strokeColor:c)),
      belowBarData:BarAreaData(show:true,color:c.withValues(alpha:0.06)));
    return LineChart(LineChartData(
      minY:0,maxY:maxY<1?5:maxY,
      lineTouchData:const LineTouchData(enabled:false),
      gridData:FlGridData(drawVerticalLine:false,
        getDrawingHorizontalLine:(_)=>FlLine(color:AppColors.divider,strokeWidth:1)),
      borderData:FlBorderData(show:false),
      titlesData:FlTitlesData(
        leftTitles:AxisTitles(sideTitles:SideTitles(showTitles:false)),
        rightTitles:AxisTitles(sideTitles:SideTitles(showTitles:false)),
        topTitles:AxisTitles(sideTitles:SideTitles(showTitles:false)),
        bottomTitles:AxisTitles(sideTitles:SideTitles(showTitles:true,reservedSize:24,interval:1,
          getTitlesWidget:(v,_){
            final i=v.toInt();
            if(i<0||i>=labels.length) return const SizedBox();
            final lbl=labels[i].length>3?labels[i].substring(0,3):labels[i];
            return Padding(padding:const EdgeInsets.only(top:4),
              child:Text(lbl,style:const TextStyle(fontSize:9,color:AppColors.slate)));
          }))),
      lineBarsData:[
        series(d.trendDisease,AppColors.leaf),
        series(d.trendPest,AppColors.warning),
        series(d.trendWater,AppColors.info),
      ],
    ));
  }

  // ── Severity donut ────────────────────────────────────────────────────────
  Widget _buildSeverityCard(AppStrings s) {
    final sev=_stats.bySeverity;
    final total=sev.values.fold(0,(a,b)=>a+b);
    pct(String k)=>total==0?0.0:(sev[k]??0)/total*100;
    final sevs=[
      ('Critical',pct('Critical'),const Color(0xFF7A1F1F)),
      ('High',    pct('High'),    AppColors.disease),
      ('Medium',  pct('Medium'),  AppColors.warning),
      ('Low',     pct('Low'),     AppColors.leaf),
    ];
    return Container(
      padding:const EdgeInsets.all(20),
      decoration:_card(),
      child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
        Text(s.severityBreakdown,
          style:const TextStyle(fontSize:15,fontWeight:FontWeight.w700,color:AppColors.ink)),
        const SizedBox(height:16),
        if(total==0)
          Center(child:Padding(padding:const EdgeInsets.all(20),
            child:Text(s.noData,style:const TextStyle(color:AppColors.slate,fontSize:13))))
        else
          Row(children:[
            SizedBox(width:100,height:100,child:PieChart(PieChartData(
              sections:sevs.map((s)=>PieChartSectionData(
                value:s.$2,color:s.$3,title:'',radius:38,
              )).toList(),
              sectionsSpace:2,centerSpaceRadius:24,
              borderData:FlBorderData(show:false),
            ))),
            const SizedBox(width:16),
            Expanded(child:Column(children:sevs.map((item)=>Padding(
              padding:const EdgeInsets.symmetric(vertical:4),
              child:Row(children:[
                Container(width:8,height:8,
                  decoration:BoxDecoration(color:item.$3,shape:BoxShape.circle)),
                const SizedBox(width:8),
                Expanded(child:Text(item.$1,
                  style:const TextStyle(fontSize:12,color:AppColors.graphite))),
                Text('${item.$2.toInt()}%',
                  style:TextStyle(fontSize:12,fontWeight:FontWeight.w700,color:item.$3)),
              ]),
            )).toList())),
          ]),
      ]),
    );
  }

  // ── Top greenhouses ───────────────────────────────────────────────────────
  Widget _buildTopGhCard(AppStrings s) {
    final top=_stats.topGreenhouses;
    return Container(
      padding:const EdgeInsets.all(20),
      decoration:_card(),
      child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
        Text(s.topGhByFindings,
          style:const TextStyle(fontSize:15,fontWeight:FontWeight.w700,color:AppColors.ink)),
        const SizedBox(height:16),
        if(top.isEmpty)
          Center(child:Padding(padding:const EdgeInsets.all(16),
            child:Text(s.noData,style:const TextStyle(color:AppColors.slate,fontSize:13))))
        else ...top.asMap().entries.map((e){
          final rank=e.key+1;
          final gh=e.value;
          final maxF=top.first.findings.toDouble();
          final pct=maxF>0?gh.findings/maxF:0.0;
          final medals=[const Color(0xFFD4AF37),const Color(0xFF9EA09E),const Color(0xFFCD7F32)];
          return Padding(padding:const EdgeInsets.only(bottom:14),
            child:Row(children:[
              Container(width:22,height:22,
                decoration:BoxDecoration(color:medals[(rank-1).clamp(0,2)].withValues(alpha:0.15),
                  shape:BoxShape.circle),
                child:Center(child:Text('$rank',
                  style:TextStyle(fontSize:10,fontWeight:FontWeight.w800,
                    color:medals[(rank-1).clamp(0,2)])))),
              const SizedBox(width:10),
              Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                Row(mainAxisAlignment:MainAxisAlignment.spaceBetween,children:[
                  Text(gh.gh,style:const TextStyle(fontSize:13,fontWeight:FontWeight.w600,color:AppColors.ink)),
                  Text('${gh.findings}',
                    style:const TextStyle(fontSize:13,fontWeight:FontWeight.w700,color:AppColors.graphite)),
                ]),
                const SizedBox(height:5),
                ClipRRect(borderRadius:BorderRadius.circular(3),
                  child:LinearProgressIndicator(value:pct,minHeight:4,
                    backgroundColor:AppColors.background,
                    valueColor:AlwaysStoppedAnimation<Color>(_catColor(gh.topIssue)))),
                const SizedBox(height:4),
                Text(gh.topIssue,style:TextStyle(fontSize:10,color:_catColor(gh.topIssue),
                  fontWeight:FontWeight.w500)),
              ])),
            ]));
        }),
      ]),
    );
  }

  // ── Category breakdown ────────────────────────────────────────────────────
  Widget _buildCategoryCard(AppStrings s) {
    final cats=_stats.byCategory;
    if(cats.isEmpty) return const SizedBox();
    final total=cats.values.fold(0,(a,b)=>a+b);
    final sorted=cats.entries.toList()..sort((a,b)=>b.value.compareTo(a.value));
    return Container(
      padding:const EdgeInsets.all(20),
      decoration:_card(),
      child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
        Text(s.topProblemCats,
          style:const TextStyle(fontSize:15,fontWeight:FontWeight.w700,color:AppColors.ink)),
        const SizedBox(height:16),
        ...sorted.map((e){
          final pct=total==0?0.0:e.value/total;
          final color=_catColor(e.key);
          return Padding(padding:const EdgeInsets.only(bottom:12),
            child:Row(children:[
              Container(width:8,height:8,
                decoration:BoxDecoration(color:color,shape:BoxShape.circle)),
              const SizedBox(width:10),
              SizedBox(width:90,child:Text(e.key,
                style:const TextStyle(fontSize:12,color:AppColors.graphite),
                overflow:TextOverflow.ellipsis)),
              Expanded(child:ClipRRect(borderRadius:BorderRadius.circular(3),
                child:LinearProgressIndicator(value:pct,minHeight:5,
                  backgroundColor:AppColors.background,
                  valueColor:AlwaysStoppedAnimation<Color>(color)))),
              const SizedBox(width:10),
              SizedBox(width:32,child:Text('${(pct*100).toInt()}%',
                style:const TextStyle(fontSize:11,fontWeight:FontWeight.w700,
                  color:AppColors.graphite),textAlign:TextAlign.right)),
              const SizedBox(width:6),
              SizedBox(width:24,child:Text('${e.value}',
                style:const TextStyle(fontSize:11,color:AppColors.slate),
                textAlign:TextAlign.right)),
            ]));
        }),
      ]),
    );
  }

  // ── Inspection table ──────────────────────────────────────────────────────
  Widget _buildInspectionTable(AppStrings s) {
    final rows=_filtered;
    final displayRows=_showAllInspections?rows:rows.take(5).toList();
    return Container(
      decoration:_card(),
      child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
        Padding(padding:const EdgeInsets.fromLTRB(20,20,20,12),
          child:Row(children:[
            Expanded(child:Text(s.recentInspections,
              style:const TextStyle(fontSize:15,fontWeight:FontWeight.w700,color:AppColors.ink))),
            if(_activeFilter!='all')
              GestureDetector(
                onTap:()=>setState((){_activeFilter='all';_showAllInspections=false;}),
                child:Container(
                  padding:const EdgeInsets.symmetric(horizontal:10,vertical:4),
                  decoration:BoxDecoration(color:AppColors.mist,borderRadius:BorderRadius.circular(20)),
                  child:Row(mainAxisSize:MainAxisSize.min,children:[
                    Text(_activeFilter,style:const TextStyle(fontSize:11,color:AppColors.forest,
                      fontWeight:FontWeight.w600)),
                    const SizedBox(width:4),
                    const Icon(Icons.close_rounded,size:12,color:AppColors.forest),
                  ]))),
          ])),
        const Divider(height:1,color:AppColors.divider),
        if(rows.isEmpty)
          Padding(padding:const EdgeInsets.all(32),
            child:Center(child:Column(children:[
              const Icon(Icons.search_off_rounded,size:32,color:AppColors.slate),
              const SizedBox(height:8),
              Text(s.noReportsYet,style:const TextStyle(color:AppColors.slate,fontSize:13)),
            ])))
        else ...[
          _buildTableRows(displayRows, s),
          if(rows.length>5)
            InkWell(
              onTap:()=>setState(()=>_showAllInspections=!_showAllInspections),
              child:Padding(
                padding:const EdgeInsets.symmetric(vertical:14),
                child:Row(mainAxisAlignment:MainAxisAlignment.center,children:[
                  Text(_showAllInspections?s.showLess:'${s.showAll} (${rows.length})',
                    style:const TextStyle(fontSize:12,fontWeight:FontWeight.w600,color:AppColors.forest)),
                  const SizedBox(width:4),
                  Icon(_showAllInspections?Icons.keyboard_arrow_up_rounded:Icons.keyboard_arrow_down_rounded,
                    size:16,color:AppColors.forest),
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
                      child:CircularProgressIndicator(strokeWidth:2,color:AppColors.forest))
                  else
                    Text(s.loadMore,
                      style:const TextStyle(fontSize:12,fontWeight:FontWeight.w600,color:AppColors.forest)),
                ]),
              ),
            ),
        ],
      ]),
    );
  }


  Widget _buildTableRows(List<_Inspection> rows, AppStrings s) {
    final header = Padding(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
      child: Row(children: [
              Expanded(flex: 2, child: Text('Scout',
                style: const TextStyle(fontSize: 10, fontWeight: FontWeight.w700,
                    letterSpacing: 0.5, color: AppColors.slate))),
        _th(s.colDate, flex: 2), _th(s.colGh, flex: 1), _th(s.colVariety, flex: 2),
        _th(s.colCategory, flex: 2), _th(s.colSeverity, flex: 2),
      ]),
    );
    final items = <Widget>[header, const Divider(height: 1, color: AppColors.divider)];
    for (int i = 0; i < rows.length; i++) {
      final r = rows[i];
      final catColor = _catColor(r.category);
      final sevColor = _sevColor(r.severity);
      items.add(Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: () => _showInspectionDetail(context, r, s),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
            child: Row(children: [
              Expanded(flex: 2, child: Text(
                r.inspectorName.isNotEmpty ? r.inspectorName : r.inspectorId,
                style: const TextStyle(fontSize: 11, color: AppColors.forest,
                    fontWeight: FontWeight.w600),
                overflow: TextOverflow.ellipsis)),
              Expanded(flex: 2, child: Text(r.date,
                style: const TextStyle(fontSize: 12, color: AppColors.graphite))),
              Expanded(flex: 1, child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                decoration: BoxDecoration(color: AppColors.mist, borderRadius: BorderRadius.circular(4)),
                child: Text(r.gh, style: const TextStyle(fontSize: 11,
                  fontWeight: FontWeight.w600, color: AppColors.forest),
                  overflow: TextOverflow.ellipsis))),
              Expanded(flex: 2, child: Text(r.variety,
                style: const TextStyle(fontSize: 12, color: AppColors.graphite),
                overflow: TextOverflow.ellipsis)),
              Expanded(flex: 2, child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 3),
                decoration: BoxDecoration(
                  color: catColor.withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(4)),
                child: Text(r.category, style: TextStyle(fontSize: 10,
                  fontWeight: FontWeight.w600, color: catColor),
                  overflow: TextOverflow.ellipsis))),
              Expanded(flex: 2, child: Row(children: [
                Container(width: 6, height: 6,
                  decoration: BoxDecoration(color: sevColor, shape: BoxShape.circle)),
                const SizedBox(width: 5),
                Text(r.severity, style: TextStyle(fontSize: 11,
                  color: sevColor, fontWeight: FontWeight.w600)),
              ])),
            ]),
          ),
        ),
      ));
      if (i < rows.length - 1) {
        items.add(const Divider(height: 1, color: AppColors.divider, indent: 20, endIndent: 20));
      }
    }
    return Column(children: items);
  }

  Widget _th(String label, {int flex = 1}) {
    return Expanded(flex: flex, child: Text(label,
      style: const TextStyle(fontSize:10, fontWeight:FontWeight.w700,
        letterSpacing:0.8, color:AppColors.slate)));
  }

  // ── States ────────────────────────────────────────────────────────────────
  Widget _buildSkeleton()=>Column(children:[
    const SizedBox(height:20),
    ...List.generate(3,(_)=>Container(
      margin:const EdgeInsets.only(bottom:12),height:80,
      decoration:BoxDecoration(color:AppColors.surface,borderRadius:BorderRadius.circular(14),
        border:Border.all(color:AppColors.border)))),
  ]);

  Widget _buildError(AppStrings s)=>Center(child:Padding(
    padding:const EdgeInsets.symmetric(vertical:60),
    child:Column(mainAxisSize:MainAxisSize.min,children:[
      Container(width:56,height:56,
        decoration:const BoxDecoration(color:AppColors.diseaseBg,shape:BoxShape.circle),
        child:const Icon(Icons.error_outline_rounded,color:AppColors.disease,size:28)),
      const SizedBox(height:16),
      Text(s.errorLoadReports,
        style:const TextStyle(fontSize:16,fontWeight:FontWeight.w700,color:AppColors.ink)),
      const SizedBox(height:6),
      Text(_error!,style:const TextStyle(fontSize:12,color:AppColors.slate),
        textAlign:TextAlign.center,maxLines:3,overflow:TextOverflow.ellipsis),
      const SizedBox(height:20),
      ElevatedButton.icon(
        onPressed:_load,
        icon:const Icon(Icons.refresh_rounded,size:16),
        label:const Text('Retry'),
        style:ElevatedButton.styleFrom(backgroundColor:AppColors.forest,foregroundColor:Colors.white,
          shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(10)),elevation:0)),
    ])));

  // ── Export ────────────────────────────────────────────────────────────────
  // ── PDF generation ─────────────────────────────────────────────
  pw.Widget _pdfKpi(String label, String value, PdfColor accent, PdfColor bg) => pw.Expanded(
        child: pw.Container(
          margin: const pw.EdgeInsets.only(right: 8),
          padding: const pw.EdgeInsets.all(10),
          decoration: pw.BoxDecoration(
            color: bg,
            borderRadius: pw.BorderRadius.circular(8),
            border: pw.Border.all(color: accent, width: 0.5),
          ),
          child: pw.Column(
            crossAxisAlignment: pw.CrossAxisAlignment.start,
            children: [
              pw.Text(value, style: pw.TextStyle(fontSize: 20, fontWeight: pw.FontWeight.bold, color: accent)),
              pw.SizedBox(height: 2),
              pw.Text(label, style: pw.TextStyle(fontSize: 9, color: PdfColors.grey700)),
            ],
          ),
        ),
      );

  PdfColor _pdfSeverityColor(String severity) {
    switch (severity.toLowerCase()) {
      case 'critical': return PdfColor.fromInt(0xFF7A1F1F);
      case 'high':      return PdfColor.fromInt(0xFFB53030);
      case 'medium':    return PdfColor.fromInt(0xFF9A5C00);
      default:          return PdfColor.fromInt(0xFF40916C);
    }
  }

  PdfColor _pdfCategoryColor(String category) {
    final c = category.toLowerCase();
    if (c.contains('disease')) return PdfColor.fromInt(0xFFB53030);
    if (c.contains('pest'))    return PdfColor.fromInt(0xFF9A5C00);
    if (c.contains('water'))   return PdfColor.fromInt(0xFF1565C0);
    return PdfColor.fromInt(0xFF40916C);
  }

  pw.Widget _pdfSeverityRow(String label, int value, int maxValue) {
    final color = _pdfSeverityColor(label);
    final pct = maxValue == 0 ? 0.0 : value / maxValue;
    return pw.Padding(
      padding: const pw.EdgeInsets.symmetric(vertical: 4),
      child: pw.Row(children: [
        pw.Container(width: 8, height: 8, decoration: pw.BoxDecoration(color: color, shape: pw.BoxShape.circle)),
        pw.SizedBox(width: 8),
        pw.SizedBox(width: 70, child: pw.Text(label, style: const pw.TextStyle(fontSize: 10))),
        pw.Expanded(
          child: pw.Container(
            height: 8,
            decoration: pw.BoxDecoration(color: PdfColors.grey200, borderRadius: pw.BorderRadius.circular(4)),
            child: pw.Row(children: [
              pw.Expanded(
                flex: (pct.clamp(0.02, 1.0) * 1000).round(),
                child: pw.Container(decoration: pw.BoxDecoration(color: color, borderRadius: pw.BorderRadius.circular(4))),
              ),
              pw.Expanded(
                flex: ((1 - pct.clamp(0.02, 1.0)) * 1000).round().clamp(1, 1000),
                child: pw.Container(),
              ),
            ]),
          ),
        ),
        pw.SizedBox(width: 8),
        pw.SizedBox(width: 24, child: pw.Text('$value', textAlign: pw.TextAlign.right,
            style: pw.TextStyle(fontSize: 10, fontWeight: pw.FontWeight.bold))),
      ]),
    );
  }

  pw.Widget _pdfCategoryRow(String label, int value, int maxValue) {
    final color = _pdfCategoryColor(label);
    final pct = maxValue == 0 ? 0.0 : value / maxValue;
    return pw.Padding(
      padding: const pw.EdgeInsets.symmetric(vertical: 4),
      child: pw.Row(children: [
        pw.SizedBox(width: 90, child: pw.Text(label, style: const pw.TextStyle(fontSize: 10))),
        pw.Expanded(
          child: pw.Container(
            height: 8,
            decoration: pw.BoxDecoration(color: PdfColors.grey200, borderRadius: pw.BorderRadius.circular(4)),
            child: pw.Row(children: [
              pw.Expanded(
                flex: (pct.clamp(0.02, 1.0) * 1000).round(),
                child: pw.Container(decoration: pw.BoxDecoration(color: color, borderRadius: pw.BorderRadius.circular(4))),
              ),
              pw.Expanded(
                flex: ((1 - pct.clamp(0.02, 1.0)) * 1000).round().clamp(1, 1000),
                child: pw.Container(),
              ),
            ]),
          ),
        ),
        pw.SizedBox(width: 8),
        pw.SizedBox(width: 24, child: pw.Text('$value', textAlign: pw.TextAlign.right,
            style: pw.TextStyle(fontSize: 10, fontWeight: pw.FontWeight.bold))),
      ]),
    );
  }

  Future<Uint8List> _generatePdfReport(AppStrings s, List<_Inspection> rows) async {
    final doc=pw.Document();
    final stats=_stats;
    const forest = PdfColor.fromInt(0xFF1B4332);
    const mist = PdfColor.fromInt(0xFFD8F3DC);
    const redAccent = PdfColor.fromInt(0xFFB53030);
    const redBg = PdfColor.fromInt(0xFFFDF0F0);
    const amberAccent = PdfColor.fromInt(0xFF9A5C00);
    const amberBg = PdfColor.fromInt(0xFFFFF8ED);
    const criticalAccent = PdfColor.fromInt(0xFF7A1F1F);
    const criticalBg = PdfColor.fromInt(0xFFFDE8E8);

    final maxSev = stats.bySeverity.values.isEmpty ? 1 : stats.bySeverity.values.reduce((a,b)=>a>b?a:b);
    final maxCat = stats.byCategory.values.isEmpty ? 1 : stats.byCategory.values.reduce((a,b)=>a>b?a:b);

    doc.addPage(pw.MultiPage(
      pageFormat: PdfPageFormat.a4,
      margin: const pw.EdgeInsets.all(28),
      header: (context) => pw.Container(
        padding: const pw.EdgeInsets.fromLTRB(20, 16, 20, 16),
        margin: const pw.EdgeInsets.only(bottom: 16),
        decoration: pw.BoxDecoration(
          color: forest,
          borderRadius: pw.BorderRadius.circular(10),
        ),
        child: pw.Row(
          mainAxisAlignment: pw.MainAxisAlignment.spaceBetween,
          children: [
            pw.Column(
              crossAxisAlignment: pw.CrossAxisAlignment.start,
              children: [
                pw.Text('Flower Scout', style: pw.TextStyle(fontSize: 20, fontWeight: pw.FontWeight.bold, color: PdfColors.white)),
                pw.Text('Inspection Report', style: pw.TextStyle(fontSize: 12, color: mist)),
              ],
            ),
            pw.Text('Generated ${DateTime.now().toString().split(".").first}',
                style: pw.TextStyle(fontSize: 9, color: mist)),
          ],
        ),
      ),
      build: (context) => [
        pw.Text('Summary', style: pw.TextStyle(fontSize: 14, fontWeight: pw.FontWeight.bold, color: forest)),
        pw.SizedBox(height: 8),
        pw.Row(children: [
          _pdfKpi('Inspections', '${stats.total}', forest, mist),
          _pdfKpi('Disease', '${stats.disease}', redAccent, redBg),
          _pdfKpi('Pests', '${stats.pest}', amberAccent, amberBg),
          _pdfKpi('Critical', '${stats.critical}', criticalAccent, criticalBg),
        ]),
        pw.SizedBox(height: 18),
        pw.Text('Severity Breakdown', style: pw.TextStyle(fontSize: 13, fontWeight: pw.FontWeight.bold, color: forest)),
        pw.SizedBox(height: 8),
        ...stats.bySeverity.entries.map((e) => _pdfSeverityRow(e.key, e.value, maxSev)),
        pw.SizedBox(height: 18),
        pw.Text('Findings by Category', style: pw.TextStyle(fontSize: 13, fontWeight: pw.FontWeight.bold, color: forest)),
        pw.SizedBox(height: 8),
        ...stats.byCategory.entries.map((e) => _pdfCategoryRow(e.key, e.value, maxCat)),
        pw.SizedBox(height: 18),
        pw.Text('Top Greenhouses', style: pw.TextStyle(fontSize: 13, fontWeight: pw.FontWeight.bold, color: forest)),
        pw.SizedBox(height: 8),
        pw.Table(
          columnWidths: const {0: pw.FlexColumnWidth(1), 1: pw.FlexColumnWidth(2), 2: pw.FlexColumnWidth(1)},
          children: stats.topGreenhouses.map((g) => pw.TableRow(children: [
            pw.Padding(padding: const pw.EdgeInsets.symmetric(vertical: 4),
                child: pw.Container(
                  padding: const pw.EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                  decoration: pw.BoxDecoration(color: mist, borderRadius: pw.BorderRadius.circular(4)),
                  child: pw.Text(g.gh, style: pw.TextStyle(fontSize: 9, fontWeight: pw.FontWeight.bold, color: forest)))),
            pw.Padding(padding: const pw.EdgeInsets.symmetric(vertical: 4),
                child: pw.Text(g.topIssue, style: const pw.TextStyle(fontSize: 10))),
            pw.Padding(padding: const pw.EdgeInsets.symmetric(vertical: 4),
                child: pw.Text('${g.findings} findings', style: pw.TextStyle(fontSize: 10, fontWeight: pw.FontWeight.bold), textAlign: pw.TextAlign.right)),
          ])).toList(),
        ),
        pw.SizedBox(height: 20),
        pw.Text('Inspection Records (${rows.length})', style: pw.TextStyle(fontSize: 13, fontWeight: pw.FontWeight.bold, color: forest)),
        pw.SizedBox(height: 8),
        pw.TableHelper.fromTextArray(
          headers: ['Scout', 'Date', 'GH', 'Variety', 'Category', 'Severity'],
          data: rows.map((r) => [r.inspectorName.isNotEmpty ? r.inspectorName : r.inspectorId, r.date, r.gh, r.variety, r.category, r.severity]).toList(),
          headerStyle: pw.TextStyle(fontWeight: pw.FontWeight.bold, fontSize: 9, color: PdfColors.white),
          cellStyle: const pw.TextStyle(fontSize: 9),
          headerDecoration: pw.BoxDecoration(color: forest),
          cellHeight: 22,
          rowDecoration: const pw.BoxDecoration(border: pw.Border(bottom: pw.BorderSide(color: PdfColors.grey300, width: 0.5))),
          oddRowDecoration: pw.BoxDecoration(color: PdfColor.fromInt(0xFFF5F6F8)),
          cellAlignments: const {0: pw.Alignment.centerLeft, 1: pw.Alignment.center, 2: pw.Alignment.centerLeft,
              3: pw.Alignment.centerLeft, 4: pw.Alignment.centerLeft},
        ),
      ],
    ));

    return doc.save();
  }

  void _showInspectionDetail(BuildContext context, _Inspection r, AppStrings s) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (_) => DraggableScrollableSheet(
        initialChildSize: 0.6,
        maxChildSize: 0.92,
        minChildSize: 0.4,
        builder: (_, ctrl) => Container(
          decoration: const BoxDecoration(
            color: AppColors.surface,
            borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
          ),
          child: Column(children: [
            Container(
              width: 40, height: 4,
              margin: const EdgeInsets.symmetric(vertical: 12),
              decoration: BoxDecoration(color: AppColors.divider, borderRadius: BorderRadius.circular(2)),
            ),
            Expanded(child: ListView(controller: ctrl, padding: const EdgeInsets.fromLTRB(20,0,20,32), children: [
              // Header
              Row(children: [
                Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text('${r.gh} · ${r.variety}', style: const TextStyle(fontSize: 16,
                      fontWeight: FontWeight.w700, color: AppColors.ink)),
                  const SizedBox(height: 4),
                  Text('${r.date}${r.inspectorName.isNotEmpty ? " · ${r.inspectorName}" : ""}',
                      style: const TextStyle(fontSize: 12, color: AppColors.slate)),
                ])),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: AppColors.severityBg(r.severity),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(r.severity, style: TextStyle(fontSize: 11,
                      fontWeight: FontWeight.w600, color: AppColors.severityColor(r.severity))),
                ),
              ]),
              const SizedBox(height: 20),
              const Divider(),
              const SizedBox(height: 12),
              // Findings
              if (r.findings.isEmpty)
                const Text('No findings recorded.', style: TextStyle(color: AppColors.slate))
              else
                ...r.findings.map((f) {
                  final cat = f['category'] as String? ?? '';
                  final sev = f['severity'] as String? ?? '';
                  final issue = f['issue'] as String? ?? '';
                  final photos = (f['photo_urls'] as List? ?? []).cast<String>();
                  return Container(
                    margin: const EdgeInsets.only(bottom: 16),
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: AppColors.background,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: AppColors.divider),
                    ),
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Row(children: [
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                          decoration: BoxDecoration(
                            color: AppColors.categoryColor(cat).withValues(alpha: 0.10),
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Text(cat, style: TextStyle(fontSize: 11,
                              fontWeight: FontWeight.w600, color: AppColors.categoryColor(cat))),
                        ),
                        const SizedBox(width: 8),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                          decoration: BoxDecoration(
                            color: AppColors.severityBg(sev),
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Text(sev, style: TextStyle(fontSize: 11,
                              fontWeight: FontWeight.w600, color: AppColors.severityColor(sev))),
                        ),
                      ]),
                      if (issue.isNotEmpty) ...[
                        const SizedBox(height: 8),
                        Text(issue, style: const TextStyle(fontSize: 13, color: AppColors.graphite, height: 1.4)),
                      ],
                      if (photos.isNotEmpty) ...[
                        const SizedBox(height: 12),
                        SizedBox(
                          height: 90,
                          child: ListView.separated(
                            scrollDirection: Axis.horizontal,
                            itemCount: photos.length,
                            separatorBuilder: (_, _) => const SizedBox(width: 8),
                            itemBuilder: (_, i) => ClipRRect(
                              borderRadius: BorderRadius.circular(8),
                              child: Image.network(photos[i],
                                width: 90, height: 90, fit: BoxFit.cover,
                                errorBuilder: (_, _, _) => Container(
                                  width: 90, height: 90,
                                  color: AppColors.surfaceAlt,
                                  child: const Icon(Icons.broken_image_rounded, color: AppColors.slate),
                                ),
                              ),
                            ),
                          ),
                        ),
                      ],
                    ]),
                  );
                }),
            ])),
          ]),
        ),
      ),
    );
  }

  Future<Uint8List> _generateExcelReport(AppStrings s, List<_Inspection> rows) async {
    final excel = Excel.createExcel();
    final sheet = excel['Inspections'];

    // Title row
    final titleCell = sheet.cell(CellIndex.indexByColumnRow(columnIndex: 0, rowIndex: 0));
    titleCell.value = TextCellValue('VP GROUP — FlowerScout Inspection Report');
    titleCell.cellStyle = CellStyle(
      bold: true,
      fontSize: 14,
      fontColorHex: ExcelColor.fromHexString('#1B4332'),
    );
    sheet.merge(CellIndex.indexByColumnRow(columnIndex: 0, rowIndex: 0),
                CellIndex.indexByColumnRow(columnIndex: 5, rowIndex: 0));

    final dateCell = sheet.cell(CellIndex.indexByColumnRow(columnIndex: 0, rowIndex: 1));
    dateCell.value = TextCellValue('Generated: ${DateTime.now().toString().split(' ').first}');
    dateCell.cellStyle = CellStyle(fontColorHex: ExcelColor.fromHexString('#6B7F6E'));
    sheet.merge(CellIndex.indexByColumnRow(columnIndex: 0, rowIndex: 1),
                CellIndex.indexByColumnRow(columnIndex: 5, rowIndex: 1));

    // Header row
    final headers = ['Date', 'Scout', 'GH', 'Variety', 'Category', 'Severity'];
    for (var i = 0; i < headers.length; i++) {
      final cell = sheet.cell(CellIndex.indexByColumnRow(columnIndex: i, rowIndex: 2));
      cell.value = TextCellValue(headers[i]);
      cell.cellStyle = CellStyle(
        bold: true,
        backgroundColorHex: ExcelColor.fromHexString('#1B4332'),
        fontColorHex: ExcelColor.fromHexString('#FFFFFF'),
      );
    }

    // Data rows
    for (var ri = 0; ri < rows.length; ri++) {
      final r = rows[ri];
      final rowData = [
        r.date,
        r.inspectorName.isNotEmpty ? r.inspectorName : r.inspectorId,
        r.gh,
        r.variety,
        r.category,
        r.severity,
      ];
      for (var ci = 0; ci < rowData.length; ci++) {
        final cell = sheet.cell(CellIndex.indexByColumnRow(columnIndex: ci, rowIndex: ri + 3));
        cell.value = TextCellValue(rowData[ci]);
        if (ri % 2 == 0) {
          cell.cellStyle = CellStyle(backgroundColorHex: ExcelColor.fromHexString('#F5F6F8'));
        }
      }
    }

    // Auto-fit columns
    sheet.setColumnWidth(0, 14);
    sheet.setColumnWidth(1, 20);
    sheet.setColumnWidth(2, 10);
    sheet.setColumnWidth(3, 18);
    sheet.setColumnWidth(4, 16);
    sheet.setColumnWidth(5, 12);

    final encoded = excel.encode();
    if (encoded == null) throw Exception('Failed to encode Excel file');
    return Uint8List.fromList(encoded);
  }

  void _shareWhatsApp(AppStrings s) {
    final stats = _stats;
    final period = {
      'today': s.today, '7days': s.last7Days,
      '30days': s.last30Days, '3months': s.last3Months,
    }[_period] ?? _period;
    final lines = [
      '*FlowerScout Report* — $period',
      '',
      '📊 *Summary*',
      '• Inspections: ${stats.total}',
      '• Disease: ${stats.disease}',
      '• Pests: ${stats.pest}',
      '• Critical: ${stats.critical}',
      '',
      '🏆 *Top Greenhouses*',
      ...stats.topGreenhouses.take(3).map((g) => '• ${g.gh}: ${g.findings} findings (${g.topIssue})'),
      '',
      '📅 Generated: ${DateTime.now().toString().split(' ').first}',
      '_via FlowerScout_',
    ];
    SharePlus.instance.share(ShareParams(text: lines.join('\n')));
  }

  void _showExport(String type, AppStrings s){
    showDialog(context:context,builder:(ctx)=>AlertDialog(
      shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(16)),
      title:Text(type=='pdf'?s.exportPdf:s.exportExcel,
        style:const TextStyle(fontFamily:'Georgia',fontSize:18)),
      content:Text(type=='pdf'?s.exportPdfDesc:s.exportExcelDesc),
      actions:[
        TextButton(onPressed:()=>Navigator.pop(ctx),child:Text(s.cancel)),
        ElevatedButton(
          onPressed:() async {
            Navigator.pop(ctx);
            if(type!='pdf'){
              Navigator.pop(ctx);
              try {
                final allRecords = await _fetchAllForExport();
                final filtered  = _applyActiveFilter(allRecords);
                final bytes     = await _generateExcelReport(s, filtered);
                final name      = 'FlowerScout_${DateTime.now().millisecondsSinceEpoch}.xlsx';
                await SharePlus.instance.share(ShareParams(
                  files: [XFile.fromData(bytes, name: name,
                    mimeType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')],
                  subject: name,
                ));
              } catch(e) {
                if(mounted) AppErrorHandler.showError(context, e, context2: 'excel export');
              }
              return;
            }
            showDialog(context:context,barrierDismissible:false,
              builder:(_)=>const Center(child:CircularProgressIndicator(color:AppColors.forest)));
            try {
              final allRecords=await _fetchAllForExport();
              final filtered=_applyActiveFilter(allRecords);
              final bytes=await _generatePdfReport(s,filtered);
              if(mounted) Navigator.pop(context);
              await Printing.layoutPdf(onLayout:(_) async => bytes,
                  name:'FlowerScout_Report_${DateTime.now().millisecondsSinceEpoch}.pdf');
            } catch(e){
              if(mounted) Navigator.pop(context);
              if(mounted) AppErrorHandler.showError(context, e, context2: 'pdf export');
            }
          },
          style:ElevatedButton.styleFrom(backgroundColor:AppColors.forest,foregroundColor:Colors.white,
            elevation:0,shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(8))),
          child:Text(s.download)),
      ]));
  }

  BoxDecoration _card()=>BoxDecoration(
    color:AppColors.surface,borderRadius:BorderRadius.circular(14),
    border:Border.all(color:AppColors.border),
    boxShadow:[BoxShadow(color:Colors.black.withValues(alpha:0.03),
      blurRadius:8,offset:const Offset(0,2))]);
}

class _KpiData {
  final String id,label; final int value; final IconData icon; final Color color,bg;
  const _KpiData({required this.id,required this.label,required this.value,
    required this.icon,required this.color,required this.bg});
}
