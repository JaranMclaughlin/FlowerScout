import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
t = p.read_text(encoding='utf-8')

# 1. Months array — make it use AppStrings
old1 = """        const months = ['Jan','Feb','Mar','Apr','May','Jun',
                        'Jul','Aug','Sep','Oct','Nov','Dec'];
        date = '${dt.day.toString().padLeft(2,'0')} ${months[dt.month-1]} ${dt.year}';"""
new1 = """        final months = AppStrings.of(_currentLang).monthsShort;
        date = '${dt.day.toString().padLeft(2,'0')} ${months[dt.month-1]} ${dt.year}';"""
if old1 not in t: raise SystemExit('anchor 1 (months) not found')
t = t.replace(old1, new1, 1)

# 2. Chart labels block 1
old2 = """    if (period=='today') { labels=['6am','8am','10am','12pm','2pm','4pm','6pm']; n=7; }
    else if (period=='30days') { labels=['W1','W2','W3','W4','W5']; n=5; }
    else if (period=='3months') { labels=['M1','M2','M3']; n=3; }
    else { labels=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']; n=7; }"""
new2 = """    final _s=AppStrings.of(_currentLang);
    if (period=='today') { labels=_s.chartLabelsToday; n=7; }
    else if (period=='30days') { labels=_s.chartLabels30Days; n=5; }
    else if (period=='3months') { labels=_s.chartLabels3Months; n=3; }
    else { labels=_s.chartLabelsWeek; n=7; }"""
if old2 not in t: raise SystemExit('anchor 2 (chart labels 1) not found')
t = t.replace(old2, new2, 1)

# 3. Chart labels block 2 (second occurrence)
old3 = """    if (period=='today') { labels=['6am','8am','10am','12pm','2pm','4pm','6pm']; n=7; }
    else if (period=='30days') { labels=['W1','W2','W3','W4','W5']; n=5; }
    else if (period=='3months') { labels=['M1','M2','M3']; n=3; }
    else { labels=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']; n=7; }"""
new3 = """    final _s2=AppStrings.of(_currentLang);
    if (period=='today') { labels=_s2.chartLabelsToday; n=7; }
    else if (period=='30days') { labels=_s2.chartLabels30Days; n=5; }
    else if (period=='3months') { labels=_s2.chartLabels3Months; n=3; }
    else { labels=_s2.chartLabelsWeek; n=7; }"""
if old3 not in t: raise SystemExit('anchor 3 (chart labels 2) not found')
t = t.replace(old3, new3, 1)

# 4. Table headers
old4 = "      _th('Date', flex: 2), _th('GH', flex: 1), _th('Variety', flex: 2),\n        _th('Category', flex: 2), _th('Severity', flex: 2),"
new4 = "      _th(s.colDate, flex: 2), _th(s.colGh, flex: 1), _th(s.colVariety, flex: 2),\n        _th(s.colCategory, flex: 2), _th(s.colSeverity, flex: 2),"
if old4 not in t: raise SystemExit('anchor 4 (table headers) not found')
t = t.replace(old4, new4, 1)

# 5. Show all / Show less
old5 = "Text(_showAllInspections?'Show less':'Show all (${rows.length})',"
new5 = "Text(_showAllInspections?s.showLess:'${s.showAll} (${rows.length})',"
if old5 not in t: raise SystemExit('anchor 5 (show all/less) not found')
t = t.replace(old5, new5, 1)

# 6. Load more
old6 = "                    const Text('Load more',\n                      style:TextStyle(fontSize:12,fontWeight:FontWeight.w600,color:_P.forest)),"
new6 = "                    Text(s.loadMore,\n                      style:const TextStyle(fontSize:12,fontWeight:FontWeight.w600,color:_P.forest)),"
if old6 not in t: raise SystemExit('anchor 6 (load more) not found')
t = t.replace(old6, new6, 1)

# 7. No data
old7 = "child:Text('No data',style:const TextStyle(color:_P.slate,fontSize:13))"
new7 = "child:Text(s.noData,style:const TextStyle(color:_P.slate,fontSize:13))"
if old7 not in t: raise SystemExit('anchor 7 (no data) not found')
t = t.replace(old7, new7, 1)

p.write_text(t, encoding='utf-8')
print('reports_screen.dart updated.')