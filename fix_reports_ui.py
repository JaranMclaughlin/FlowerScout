import pathlib

reports = r"""import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../../../shared/theme/app_colors.dart';
import '../../../shared/providers/farm_providers.dart';
import '../../../shared/providers/farm_repository.dart';
import '../../../shared/providers/locale_provider.dart';
import '../../../shared/l10n/app_strings.dart';

// ── Palette ───────────────────────────────────────────────────────────────────
class _P {
  static const bg        = Color(0xFFF5F6F8);
  static const surface   = Color(0xFFFFFFFF);
  static const border    = Color(0xFFE8ECE8);
  static const ink       = Color(0xFF0F1F12);
  static const graphite  = Color(0xFF3D4F42);
  static const slate     = Color(0xFF7A8C7E);
  static const forest    = Color(0xFF1B4332);
  static const canopy    = Color(0xFF2D6A4F);
  static const leaf      = Color(0xFF40916C);
  static const mint      = Color(0xFF74C69D);
  static const mist      = Color(0xFFD8F3DC);
  static const red       = Color(0xFFB53030);
  static const redBg     = Color(0xFFFDF0F0);
  static const amber     = Color(0xFF9A5C00);
  static const amberBg   = Color(0xFFFFF8ED);
  static const blue      = Color(0xFF1565C0);
  static const blueBg    = Color(0xFFEEF4FF);
  static const divider   = Color(0xFFEDF1ED);
}

// ── Data models ───────────────────────────────────────────────────────────────
class _Inspection {
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
      gh: r['greenhouse_code'] as String? ?? r['greenhouse_id']?.toString() ?? '—',
      variety: r['variety_name'] as String? ?? '—',
      category: topCat, severity: topSev,
      inspectorId: scoutId.length >= 8 ? scoutId.substring(0, 8) : scoutId,
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
  factory _ReportStats.fromInspections(List<_Inspection> ins, String period) {
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
    final buckets=_buildTrend(ins,period);
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
  static Map<String,List<dynamic>> _buildTrend(List<_Inspection> ins, String period) {
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
  }
}

// ── Fetcher ───────────────────────────────────────────────────────────────────
Future<List<_Inspection>> _fetchInspections(String period,
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
}

// ── Screen ────────────────────────────────────────────────────────────────────
class ReportsScreen extends ConsumerStatefulWidget {
  const ReportsScreen({super.key});
  @override ConsumerState<ReportsScreen> createState()=>_ReportsScreenState();
}

class _ReportsScreenState extends ConsumerState<ReportsScreen> {
  String _period='7days';
  String? _farmId, _greenhouseId, _variety;
  String _chartType='Bar';
  String _activeFilter='all';
  List<_Inspection> _inspections=[];
  _ReportStats _stats=_ReportStats.empty();
  bool _loading=true;
  String? _error;

  @override void initState(){ super.initState(); _load(); }

  Future<void> _load() async {
    setState((){_loading=true;_error=null;});
    try {
      final data=await _fetchInspections(_period,
          farmId:_farmId,greenhouseId:_greenhouseId,variety:_variety);
      if(mounted) setState((){_inspections=data;_stats=_ReportStats.fromInspections(data,_period);_loading=false;});
    } catch(e){ if(mounted) setState((){_error=e.toString();_loading=false;}); }
  }

  List<_Inspection> get _filtered {
    if (_activeFilter=='all') return _inspections;
    if (_activeFilter=='critical') return _inspections.where((r)=>r.severity.toLowerCase()=='critical').toList();
    return _inspections.where((r)=>r.category.toLowerCase().contains(_activeFilter)).toList();
  }

  Color _catColor(String cat) {
    final c=cat.toLowerCase();
    if (c.contains('disease')) return _P.red;
    if (c.contains('pest')) return _P.amber;
    if (c.contains('water')) return _P.blue;
    if (c.contains('nutri')) return _P.leaf;
    if (c.contains('irrig')) return const Color(0xFF00838F);
    return _P.slate;
  }

  Color _sevColor(String s) => switch(s.toLowerCase()){
    'critical'=>const Color(0xFF7A1F1F),
    'high'=>_P.red,
    'medium'=>_P.amber,
    _=>_P.leaf,
  };

  @override
  Widget build(BuildContext context) {
    final farmsAsync=ref.watch(farmsProvider);
    final s=ref.watch(stringsProvider);
    return Container(
      color: _P.bg,
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
    final farmItems=<String,String?>{'All Farms':null};
    for(final f in farms) farmItems[f.name]=f.id;
    final ghItems=<String,String?>{'All':null};
    if(_farmId!=null){
      final farm=farms.firstWhere((f)=>f.id==_farmId,orElse:()=>farms.first);
      for(final g in farm.greenhouses) ghItems[g.code]=g.id;
    }
    final varItems=<String,String?>{'All':null};
    if(_greenhouseId!=null){
      for(final f in farms) for(final g in f.greenhouses){
        if(g.id==_greenhouseId) for(final v in g.varietyNames) varItems[v]=v;
      }
    }
    final periodItems={s.today:'today',s.last7Days:'7days',s.last30Days:'30days',s.last3Months:'3months'};

    return Container(
      color:_P.surface,
      padding:const EdgeInsets.fromLTRB(24,24,24,20),
      child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
        Row(children:[
          Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
            Text(s.reportsAnalytics,
              style:const TextStyle(fontSize:26,fontWeight:FontWeight.w800,
                color:_P.ink,letterSpacing:-0.5)),
            const SizedBox(height:4),
            Text(s.reportsSubtitle,
              style:const TextStyle(fontSize:13,color:_P.slate)),
          ])),
          const SizedBox(width:16),
          _exportChip(Icons.picture_as_pdf_outlined,'PDF',_P.red,()=>_showExport('pdf',s)),
          const SizedBox(width:8),
          _exportChip(Icons.table_chart_outlined,'Excel',_P.leaf,()=>_showExport('excel',s)),
        ]),
        const SizedBox(height:20),
        const Divider(height:1,color:_P.divider),
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
      decoration:BoxDecoration(color:_P.bg,borderRadius:BorderRadius.circular(8),
        border:Border.all(color:_P.border)),
      child:DropdownButtonHideUnderline(child:DropdownButton<String>(
        value:items.contains(value)?value:items.first,
        isDense:true,
        style:const TextStyle(fontSize:12,color:_P.ink,fontWeight:FontWeight.w500),
        icon:const Icon(Icons.keyboard_arrow_down_rounded,size:16,color:_P.slate),
        items:items.map((e)=>DropdownMenuItem(value:e,child:Text(e))).toList(),
        onChanged:onChanged,
      )),
    );

  // ── KPI row ──────────────────────────────────────────────────────────────
  Widget _buildKpiRow(AppStrings s) {
    final kpis=[
      _KpiData(id:'all',    label:s.inspections, value:_stats.total,
        icon:Icons.assignment_outlined,      color:_P.forest,  bg:_P.mist),
      _KpiData(id:'disease',label:s.disease,     value:_stats.disease,
        icon:Icons.coronavirus_outlined,     color:_P.red,     bg:_P.redBg),
      _KpiData(id:'pest',   label:s.pests,       value:_stats.pest,
        icon:Icons.bug_report_outlined,      color:_P.amber,   bg:_P.amberBg),
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
          color:active?k.color:_P.surface,
          borderRadius:BorderRadius.circular(14),
          border:Border.all(color:active?k.color:_P.border,width:active?2:1),
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
              color:active?Colors.white:_P.ink,height:1)),
            const SizedBox(height:2),
            Text(k.label,style:TextStyle(fontSize:11,color:active?Colors.white70:_P.slate,
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
              style:const TextStyle(fontSize:15,fontWeight:FontWeight.w700,color:_P.ink)),
            const SizedBox(height:2),
            Text('By category over period',
              style:const TextStyle(fontSize:11,color:_P.slate)),
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
          color:active?_P.forest:Colors.transparent,
          borderRadius:BorderRadius.circular(6),
          border:Border.all(color:active?_P.forest:_P.border),
        ),
        child:Text(t,style:TextStyle(fontSize:11,fontWeight:FontWeight.w600,
          color:active?Colors.white:_P.slate))));
  }).toList());

  Widget _legend(AppStrings s)=>Wrap(spacing:16,children:[
    (_P.leaf,s.disease),(_P.amber,s.pests),(_P.blue,'Water'),
  ].map((i)=>Row(mainAxisSize:MainAxisSize.min,children:[
    Container(width:8,height:8,decoration:BoxDecoration(color:i.$1,shape:BoxShape.circle)),
    const SizedBox(width:4),
    Text(i.$2,style:const TextStyle(fontSize:11,color:_P.slate)),
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
        getDrawingHorizontalLine:(_)=>FlLine(color:_P.divider,strokeWidth:1)),
      borderData:FlBorderData(show:false),
      titlesData:FlTitlesData(
        leftTitles:AxisTitles(sideTitles:SideTitles(showTitles:false)),
        rightTitles:AxisTitles(sideTitles:SideTitles(showTitles:false)),
        topTitles:AxisTitles(sideTitles:SideTitles(showTitles:false)),
        bottomTitles:AxisTitles(sideTitles:SideTitles(showTitles:true,reservedSize:24,
          getTitlesWidget:(v,_){
            final i=v.toInt();
            if(i<0||i>=labels.length) return const SizedBox();
            return Padding(padding:const EdgeInsets.only(top:4),
              child:Text(labels[i],style:const TextStyle(fontSize:9,color:_P.slate)));
          }))),
      barGroups:List.generate(labels.length,(i)=>BarChartGroupData(x:i,barRods:[
        BarChartRodData(toY:d.trendDisease[i],color:_P.leaf,width:4,borderRadius:BorderRadius.circular(3)),
        BarChartRodData(toY:d.trendPest[i],color:_P.amber,width:4,borderRadius:BorderRadius.circular(3)),
        BarChartRodData(toY:d.trendWater[i],color:_P.blue,width:4,borderRadius:BorderRadius.circular(3)),
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
      dotData:FlDotData(show:true,getDotPainter:(s,_,__,___)=>
        FlDotCirclePainter(radius:3,color:c,strokeWidth:0,strokeColor:c)),
      belowBarData:BarAreaData(show:true,color:c.withValues(alpha:0.06)));
    return LineChart(LineChartData(
      minY:0,maxY:maxY<1?5:maxY,
      lineTouchData:const LineTouchData(enabled:false),
      gridData:FlGridData(drawVerticalLine:false,
        getDrawingHorizontalLine:(_)=>FlLine(color:_P.divider,strokeWidth:1)),
      borderData:FlBorderData(show:false),
      titlesData:FlTitlesData(
        leftTitles:AxisTitles(sideTitles:SideTitles(showTitles:false)),
        rightTitles:AxisTitles(sideTitles:SideTitles(showTitles:false)),
        topTitles:AxisTitles(sideTitles:SideTitles(showTitles:false)),
        bottomTitles:AxisTitles(sideTitles:SideTitles(showTitles:true,reservedSize:24,
          getTitlesWidget:(v,_){
            final i=v.toInt();
            if(i<0||i>=labels.length) return const SizedBox();
            return Padding(padding:const EdgeInsets.only(top:4),
              child:Text(labels[i],style:const TextStyle(fontSize:9,color:_P.slate)));
          }))),
      lineBarsData:[
        series(d.trendDisease,_P.leaf),
        series(d.trendPest,_P.amber),
        series(d.trendWater,_P.blue),
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
      ('High',    pct('High'),    _P.red),
      ('Medium',  pct('Medium'),  _P.amber),
      ('Low',     pct('Low'),     _P.leaf),
    ];
    return Container(
      padding:const EdgeInsets.all(20),
      decoration:_card(),
      child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
        Text(s.severityBreakdown,
          style:const TextStyle(fontSize:15,fontWeight:FontWeight.w700,color:_P.ink)),
        const SizedBox(height:16),
        if(total==0)
          Center(child:Padding(padding:const EdgeInsets.all(20),
            child:Text('No data',style:const TextStyle(color:_P.slate,fontSize:13))))
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
                  style:const TextStyle(fontSize:12,color:_P.graphite))),
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
          style:const TextStyle(fontSize:15,fontWeight:FontWeight.w700,color:_P.ink)),
        const SizedBox(height:16),
        if(top.isEmpty)
          Center(child:Padding(padding:const EdgeInsets.all(16),
            child:Text('No data',style:const TextStyle(color:_P.slate,fontSize:13))))
        else ...top.asMap().entries.map((e){
          final rank=e.key+1;
          final gh=e.value;
          final maxF=top.first.findings.toDouble();
          final pct=maxF>0?gh.findings/maxF:0.0;
          final medals=[const Color(0xFFD4AF37),const Color(0xFF9EA09E),const Color(0xFFCD7F32)];
          return Padding(padding:const EdgeInsets.only(bottom:14),
            child:Row(children:[
              Container(width:22,height:22,
                decoration:BoxDecoration(color:medals[rank-1].withValues(alpha:0.15),
                  shape:BoxShape.circle),
                child:Center(child:Text('$rank',
                  style:TextStyle(fontSize:10,fontWeight:FontWeight.w800,
                    color:medals[rank-1])))),
              const SizedBox(width:10),
              Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                Row(mainAxisAlignment:MainAxisAlignment.spaceBetween,children:[
                  Text(gh.gh,style:const TextStyle(fontSize:13,fontWeight:FontWeight.w600,color:_P.ink)),
                  Text('${gh.findings}',
                    style:const TextStyle(fontSize:13,fontWeight:FontWeight.w700,color:_P.graphite)),
                ]),
                const SizedBox(height:5),
                ClipRRect(borderRadius:BorderRadius.circular(3),
                  child:LinearProgressIndicator(value:pct,minHeight:4,
                    backgroundColor:_P.bg,
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
          style:const TextStyle(fontSize:15,fontWeight:FontWeight.w700,color:_P.ink)),
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
                style:const TextStyle(fontSize:12,color:_P.graphite),
                overflow:TextOverflow.ellipsis)),
              Expanded(child:ClipRRect(borderRadius:BorderRadius.circular(3),
                child:LinearProgressIndicator(value:pct,minHeight:5,
                  backgroundColor:_P.bg,
                  valueColor:AlwaysStoppedAnimation<Color>(color)))),
              const SizedBox(width:10),
              SizedBox(width:32,child:Text('${(pct*100).toInt()}%',
                style:const TextStyle(fontSize:11,fontWeight:FontWeight.w700,
                  color:_P.graphite),textAlign:TextAlign.right)),
              const SizedBox(width:6),
              SizedBox(width:24,child:Text('${e.value}',
                style:const TextStyle(fontSize:11,color:_P.slate),
                textAlign:TextAlign.right)),
            ]));
        }),
      ]),
    );
  }

  // ── Inspection table ──────────────────────────────────────────────────────
  Widget _buildInspectionTable(AppStrings s) {
    final rows=_filtered;
    return Container(
      decoration:_card(),
      child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
        Padding(padding:const EdgeInsets.fromLTRB(20,20,20,12),
          child:Row(children:[
            Expanded(child:Text(s.recentInspections,
              style:const TextStyle(fontSize:15,fontWeight:FontWeight.w700,color:_P.ink))),
            if(_activeFilter!='all')
              GestureDetector(onTap:()=>setState(()=>_activeFilter='all'),
                child:Container(
                  padding:const EdgeInsets.symmetric(horizontal:10,vertical:4),
                  decoration:BoxDecoration(color:_P.mist,borderRadius:BorderRadius.circular(20)),
                  child:Row(mainAxisSize:MainAxisSize.min,children:[
                    Text(_activeFilter,style:const TextStyle(fontSize:11,color:_P.forest,
                      fontWeight:FontWeight.w600)),
                    const SizedBox(width:4),
                    const Icon(Icons.close_rounded,size:12,color:_P.forest),
                  ]))),
          ])),
        const Divider(height:1,color:_P.divider),
        if(rows.isEmpty)
          Padding(padding:const EdgeInsets.all(32),
            child:Center(child:Column(children:[
              const Icon(Icons.search_off_rounded,size:32,color:_P.slate),
              const SizedBox(height:8),
              Text(s.noReportsYet,style:const TextStyle(color:_P.slate,fontSize:13)),
            ])))
        else
          // Table header
          Column(children:[
            Padding(padding:const EdgeInsets.symmetric(horizontal:20,vertical:10),
              child:Row(children:[
                _th('Date',flex:2),_th('GH',flex:1),_th('Variety',flex:2),
                _th('Category',flex:2),_th('Severity',flex:2),
              ])),
            const Divider(height:1,color:_P.divider),
            ...rows.asMap().entries.map((entry){
              final i=entry.key; final r=entry.value;
              final catColor=_catColor(r.category);
              final sevColor=_sevColor(r.severity);
              return Column(children:[
                Material(color:Colors.transparent,
                  child:InkWell(
                    onTap:()=>ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                      content:Text('${r.date} · ${r.gh} · ${r.variety}'),
                      behavior:SnackBarBehavior.floating,
                      shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(10)),
                    )),
                    child:Padding(padding:const EdgeInsets.symmetric(horizontal:20,vertical:12),
                      child:Row(children:[
                        Expanded(flex:2,child:Text(r.date,
                          style:const TextStyle(fontSize:12,color:_P.graphite))),
                        Expanded(flex:1,child:Container(
                          padding:const EdgeInsets.symmetric(horizontal:6,vertical:2),
                          decoration:BoxDecoration(color:_P.mist,borderRadius:BorderRadius.circular(4)),
                          child:Text(r.gh,style:const TextStyle(fontSize:11,
                            fontWeight:FontWeight.w600,color:_P.forest),
                            overflow:TextOverflow.ellipsis))),
                        Expanded(flex:2,child:Text(r.variety,
                          style:const TextStyle(fontSize:12,color:_P.graphite),
                          overflow:TextOverflow.ellipsis)),
                        Expanded(flex:2,child:Container(
                          padding:const EdgeInsets.symmetric(horizontal:7,vertical:3),
                          decoration:BoxDecoration(
                            color:catColor.withValues(alpha:0.1),
                            borderRadius:BorderRadius.circular(4)),
                          child:Text(r.category,style:TextStyle(fontSize:10,
                            fontWeight:FontWeight.w600,color:catColor),
                            overflow:TextOverflow.ellipsis))),
                        Expanded(flex:2,child:Row(children:[
                          Container(width:6,height:6,
                            decoration:BoxDecoration(color:sevColor,shape:BoxShape.circle)),
                          const SizedBox(width:5),
                          Text(r.severity,style:TextStyle(fontSize:11,
                            color:sevColor,fontWeight:FontWeight.w600)),
                        ])),
                      ]))),
                  )),
                if(i<rows.length-1) const Divider(height:1,color:_P.divider,indent:20,endIndent:20),
              ]);
            }),
          ]),
      ]),
    );
  }

  Widget _th(String label,{int flex=1})=>Expanded(flex:flex,child:
    Text(label,style:const TextStyle(fontSize:10,fontWeight:FontWeight.w700,
      letterSpacing:0.8,color:_P.slate)));

  // ── States ────────────────────────────────────────────────────────────────
  Widget _buildSkeleton()=>Column(children:[
    const SizedBox(height:20),
    ...List.generate(3,(_)=>Container(
      margin:const EdgeInsets.only(bottom:12),height:80,
      decoration:BoxDecoration(color:_P.surface,borderRadius:BorderRadius.circular(14),
        border:Border.all(color:_P.border)))),
  ]);

  Widget _buildError(AppStrings s)=>Center(child:Padding(
    padding:const EdgeInsets.symmetric(vertical:60),
    child:Column(mainAxisSize:MainAxisSize.min,children:[
      Container(width:56,height:56,
        decoration:const BoxDecoration(color:_P.redBg,shape:BoxShape.circle),
        child:const Icon(Icons.error_outline_rounded,color:_P.red,size:28)),
      const SizedBox(height:16),
      Text(s.errorLoadReports,
        style:const TextStyle(fontSize:16,fontWeight:FontWeight.w700,color:_P.ink)),
      const SizedBox(height:6),
      Text(_error!,style:const TextStyle(fontSize:12,color:_P.slate),
        textAlign:TextAlign.center,maxLines:3,overflow:TextOverflow.ellipsis),
      const SizedBox(height:20),
      ElevatedButton.icon(
        onPressed:_load,
        icon:const Icon(Icons.refresh_rounded,size:16),
        label:const Text('Retry'),
        style:ElevatedButton.styleFrom(backgroundColor:_P.forest,foregroundColor:Colors.white,
          shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(10)),elevation:0)),
    ])));

  // ── Export ────────────────────────────────────────────────────────────────
  void _showExport(String type, AppStrings s){
    showDialog(context:context,builder:(ctx)=>AlertDialog(
      shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(16)),
      title:Text(type=='pdf'?s.exportPdf:s.exportExcel,
        style:const TextStyle(fontFamily:'Georgia',fontSize:18)),
      content:Text(type=='pdf'?s.exportPdfDesc:s.exportExcelDesc),
      actions:[
        TextButton(onPressed:()=>Navigator.pop(ctx),child:Text(s.cancel)),
        ElevatedButton(
          onPressed:(){Navigator.pop(ctx);
            ScaffoldMessenger.of(context).showSnackBar(SnackBar(
              content:Text('${type=='pdf'?s.exportPdf:s.exportExcel} — coming soon'),
              behavior:SnackBarBehavior.floating,
              shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(10))));},
          style:ElevatedButton.styleFrom(backgroundColor:_P.forest,foregroundColor:Colors.white,
            elevation:0,shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(8))),
          child:Text(s.download)),
      ]));
  }

  BoxDecoration _card()=>BoxDecoration(
    color:_P.surface,borderRadius:BorderRadius.circular(14),
    border:Border.all(color:_P.border),
    boxShadow:[BoxShadow(color:Colors.black.withValues(alpha:0.03),
      blurRadius:8,offset:const Offset(0,2))]);
}

class _KpiData {
  final String id,label; final int value; final IconData icon; final Color color,bg;
  const _KpiData({required this.id,required this.label,required this.value,
    required this.icon,required this.color,required this.bg});
}
"""

pathlib.Path('lib/features/reports/presentation/reports_screen.dart').write_text(reports, encoding='utf-8')
print('done')