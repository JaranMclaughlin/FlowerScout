import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
t = p.read_text(encoding='utf-8')

# 1. Fix _fetchInspections signature
old1 = "Future<List<_Inspection>> _fetchInspections(String period,\n    {String? farmId, String? greenhouseId, String? variety,\n     int offset=0, int limit=50}) async {"
new1 = "Future<List<_Inspection>> _fetchInspections(String period,\n    {String? farmId, String? greenhouseId, String? variety,\n     int offset=0, int limit=50, String lang='en'}) async {"
if old1 not in t: raise SystemExit('anchor 1 not found')
t = t.replace(old1, new1, 1)

# 2. Fix fromRow call to use lang param
old2 = "    return _Inspection.fromRow(row, lang: _lang);"
new2 = "    return _Inspection.fromRow(row, lang: lang);"
if old2 not in t: raise SystemExit('anchor 2 not found')
t = t.replace(old2, new2, 1)

# 3. Pass lang at _load() call site
old3 = "_fetchInspections(_period,farmId:_farmId,greenhouseId:_greenhouseId,variety:_variety,\n          offset:0,limit:_pageSize),"
new3 = "_fetchInspections(_period,farmId:_farmId,greenhouseId:_greenhouseId,variety:_variety,\n          offset:0,limit:_pageSize,lang:ref.read(localeProvider)),"
if old3 not in t: raise SystemExit('anchor 3 not found')
t = t.replace(old3, new3, 1)

# 4. Pass lang at _loadMore() call site
old4 = "      final more=await _fetchInspections(_period,\n        farmId:_farmId,greenhouseId:_greenhouseId,variety:_variety,\n        offset:_inspections.length,limit:_pageSize);"
new4 = "      final more=await _fetchInspections(_period,\n        farmId:_farmId,greenhouseId:_greenhouseId,variety:_variety,\n        offset:_inspections.length,limit:_pageSize,lang:ref.read(localeProvider));"
if old4 not in t: raise SystemExit('anchor 4 not found')
t = t.replace(old4, new4, 1)

p.write_text(t, encoding='utf-8')
print('lang threaded through _fetchInspections.')