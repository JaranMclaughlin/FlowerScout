import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
t = p.read_text(encoding='utf-8')

# 1. Replace _lang with ref.read(localeProvider) at the fromRow call site
old1 = "    return _Inspection.fromRow(row, lang: _lang);"
new1 = "    return _Inspection.fromRow(row, lang: _lang ?? 'en');"
# _lang is passed as param to _fetchInspections - add it there

# Actually fix _fetchInspections signature to accept lang
old2 = "Future<List<_Inspection>> _fetchInspections(String period,\n     {String? farmId, String? greenhouseId, String? variety,\n      int offset=0, int limit=50}) async {"
new2 = "Future<List<_Inspection>> _fetchInspections(String period,\n     {String? farmId, String? greenhouseId, String? variety,\n      int offset=0, int limit=50, String lang='en'}) async {"
if old2 not in t: raise SystemExit('anchor 2 (_fetchInspections sig) not found')
t = t.replace(old2, new2, 1)

# 2. Fix the fromRow call to use the lang param
old3 = "    return _Inspection.fromRow(row, lang: _lang ?? 'en');"
new3 = "    return _Inspection.fromRow(row, lang: lang);"
t = t.replace(old3, new3, 1)

old3b = "    return _Inspection.fromRow(row, lang: _lang);"
new3b = "    return _Inspection.fromRow(row, lang: lang);"
if old3b in t:
    t = t.replace(old3b, new3b, 1)

# 3. Pass lang at _fetchInspections call sites in _load()
old4 = "_fetchInspections(_period,farmId:_farmId,greenhouseId:_greenhouseId,variety:_variety,\n          offset:0,limit:_pageSize),"
new4 = "_fetchInspections(_period,farmId:_farmId,greenhouseId:_greenhouseId,variety:_variety,\n          offset:0,limit:_pageSize,lang:ref.read(localeProvider)),"
if old4 not in t: raise SystemExit('anchor 4 (_load fetchInspections) not found')
t = t.replace(old4, new4, 1)

# 4. Pass lang at _loadMore call site
old5 = "      final more=await _fetchInspections(_period,\n        farmId:_farmId,greenhouseId:_greenhouseId,variety:_variety,\n        offset:_inspections.length,limit:_pageSize);"
new5 = "      final more=await _fetchInspections(_period,\n        farmId:_farmId,greenhouseId:_greenhouseId,variety:_variety,\n        offset:_inspections.length,limit:_pageSize,lang:ref.read(localeProvider));"
if old5 not in t: raise SystemExit('anchor 5 (_loadMore fetchInspections) not found')
t = t.replace(old5, new5, 1)

p.write_text(t, encoding='utf-8')
print('lang param threaded through fetchInspections.')