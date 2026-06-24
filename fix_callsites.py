import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
t = p.read_text(encoding='utf-8')

# 1. fromRow call - get lang from ref at call site
old1 = "    return _Inspection.fromRow(row);"
new1 = "    return _Inspection.fromRow(row, lang: _lang);"
if old1 not in t: raise SystemExit('anchor 1 (fromRow call) not found')
t = t.replace(old1, new1, 1)

# 2. fromRpcJson call
old2 = "        _stats=_ReportStats.fromRpcJson(statsJson,_period);"
new2 = "        _stats=_ReportStats.fromRpcJson(statsJson,_period,lang:ref.read(localeProvider));"
if old2 not in t: raise SystemExit('anchor 2 (fromRpcJson call) not found')
t = t.replace(old2, new2, 1)

p.write_text(t, encoding='utf-8')
print('Call sites updated.')