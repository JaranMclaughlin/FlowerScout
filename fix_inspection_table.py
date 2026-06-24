import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

# 1. Add state field
old_fields = """  String _activeFilter='all';
  List<_Inspection> _inspections=[];"""
new_fields = """  String _activeFilter='all';
  bool _showAllInspections=false;
  List<_Inspection> _inspections=[];"""
if old_fields not in text:
    raise SystemExit("State fields anchor not found - aborting.")
text = text.replace(old_fields, new_fields, 1)

# 2. Reset the toggle whenever a new load starts (filter changed)
old_load = """  Future<void> _load() async {
    setState((){_loading=true;_error=null;});"""
new_load = """  Future<void> _load() async {
    setState((){_loading=true;_error=null;_showAllInspections=false;});"""
if old_load not in text:
    raise SystemExit("_load anchor not found - aborting.")
text = text.replace(old_load, new_load, 1)

# 3. Show 5 by default, expand to all on tap
old_table = """  Widget _buildInspectionTable(AppStrings s) {
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
          _buildTableRows(rows),
      ]),
    );
  }"""

new_table = """  Widget _buildInspectionTable(AppStrings s) {
    final rows=_filtered;
    final displayRows=_showAllInspections?rows:rows.take(5).toList();
    return Container(
      decoration:_card(),
      child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
        Padding(padding:const EdgeInsets.fromLTRB(20,20,20,12),
          child:Row(children:[
            Expanded(child:Text(s.recentInspections,
              style:const TextStyle(fontSize:15,fontWeight:FontWeight.w700,color:_P.ink))),
            if(_activeFilter!='all')
              GestureDetector(onTap:()=>setState((){_activeFilter='all';_showAllInspections=false;}),
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
        else ...[
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
        ],
      ]),
    );
  }"""

if old_table not in text:
    raise SystemExit("_buildInspectionTable anchor not found - aborting, no changes made.")
text = text.replace(old_table, new_table, 1)

p.write_text(text, encoding='utf-8')
print("reports_screen.dart updated: Recent Inspections now shows 5 by default with expand/collapse.")