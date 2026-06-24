import pathlib
rp = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
rc = rp.read_text(encoding='utf-8')

old = """        else
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
                      content:Text('\${r.date} · \${r.gh} · \${r.variety}'),
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
          ]),"""

new = """        else
          _buildTableRows(rows),"""

rc = rc.replace(old, new)

# Add the helper method before _th
helper = '''
  Widget _buildTableRows(List<_Inspection> rows) {
    final header = Padding(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
      child: Row(children: [
        _th('Date', flex: 2), _th('GH', flex: 1), _th('Variety', flex: 2),
        _th('Category', flex: 2), _th('Severity', flex: 2),
      ]),
    );
    final items = <Widget>[header, const Divider(height: 1, color: _P.divider)];
    for (int i = 0; i < rows.length; i++) {
      final r = rows[i];
      final catColor = _catColor(r.category);
      final sevColor = _sevColor(r.severity);
      items.add(Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: () => ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            content: Text('${r.date} · ${r.gh} · ${r.variety}'),
            behavior: SnackBarBehavior.floating,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
          )),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
            child: Row(children: [
              Expanded(flex: 2, child: Text(r.date,
                style: const TextStyle(fontSize: 12, color: _P.graphite))),
              Expanded(flex: 1, child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                decoration: BoxDecoration(color: _P.mist, borderRadius: BorderRadius.circular(4)),
                child: Text(r.gh, style: const TextStyle(fontSize: 11,
                  fontWeight: FontWeight.w600, color: _P.forest),
                  overflow: TextOverflow.ellipsis))),
              Expanded(flex: 2, child: Text(r.variety,
                style: const TextStyle(fontSize: 12, color: _P.graphite),
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
        items.add(const Divider(height: 1, color: _P.divider, indent: 20, endIndent: 20));
      }
    }
    return Column(children: items);
  }

'''

rc = rc.replace(
    "  Widget _th(String label,",
    helper + "  Widget _th(String label,"
)

rp.write_text(rc, encoding='utf-8')
print('done')