import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
t = p.read_text(encoding='utf-8')

# 1. Fix _Inspection.fromRow to accept lang param
old1 = "  factory _Inspection.fromRow(Map<String, dynamic> r) {"
new1 = "  factory _Inspection.fromRow(Map<String, dynamic> r, {String lang='en'}) {"
if old1 not in t: raise SystemExit('anchor 1 not found')
t = t.replace(old1, new1, 1)

# 2. Fix _currentLang in fromRow
old2 = "        final months = AppStrings.of(_currentLang).monthsShort;"
new2 = "        final months = AppStrings.of(lang).monthsShort;"
if old2 not in t: raise SystemExit('anchor 2 not found')
t = t.replace(old2, new2, 1)

# 3. Fix empty() default chart labels
old3 = "    chartLabels:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],"
new3 = "    chartLabels:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], // default; overridden at runtime"
if old3 not in t: raise SystemExit('anchor 3 not found')
t = t.replace(old3, new3, 1)

# 4. Fix fromRpcJson to accept lang param
old4 = "  factory _ReportStats.fromRpcJson(Map<String,dynamic> json, String period) {"
new4 = "  factory _ReportStats.fromRpcJson(Map<String,dynamic> json, String period, {String lang='en'}) {"
if old4 not in t: raise SystemExit('anchor 4 not found')
t = t.replace(old4, new4, 1)

# 5. Fix _currentLang in fromRpcJson
old5 = "    final _s=AppStrings.of(_currentLang);"
new5 = "    final _s=AppStrings.of(lang);"
if old5 not in t: raise SystemExit('anchor 5 not found')
t = t.replace(old5, new5, 1)

# 6. Fix second chart labels block (_fetchReportStatsRpc)
old6 = "    final _s2=AppStrings.of(_currentLang);"
new6 = "    // chart labels handled in fromRpcJson"
if old6 not in t: raise SystemExit('anchor 6 not found')
t = t.replace(old6, new6, 1)

# 7. Fix second chart labels usage after anchor 6
old7 = """    if (period=='today') { labels=_s2.chartLabelsToday; n=7; }
    else if (period=='30days') { labels=_s2.chartLabels30Days; n=5; }
    else if (period=='3months') { labels=_s2.chartLabels3Months; n=3; }
    else { labels=_s2.chartLabelsWeek; n=7; }"""
new7 = """    if (period=='today') { labels=['6am','8am','10am','12pm','2pm','4pm','6pm']; n=7; }
    else if (period=='30days') { labels=['W1','W2','W3','W4','W5']; n=5; }
    else if (period=='3months') { labels=['M1','M2','M3']; n=3; }
    else { labels=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']; n=7; }"""
if old7 not in t: raise SystemExit('anchor 7 not found')
t = t.replace(old7, new7, 1)

p.write_text(t, encoding='utf-8')
print('Step 1 done - factory params fixed.')