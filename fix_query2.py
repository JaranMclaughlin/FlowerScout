import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

old = "  var q=db.from('inspection_reports').select('''\n    id, submitted_at, started_at, variety_name, greenhouse_id, scout_id,\n    greenhouses!inner(code),\n    inspection_findings(category, severity)\n  ''').gte('submitted_at',since.toIso8601String());"

new = "  var q=db.from('inspection_reports').select('''\n    id, submitted_at, started_at, variety_name, greenhouse_id, scout_id, scout_name,\n    greenhouses!inner(code, farm_id),\n    inspection_findings(category, severity, issue, photo_urls)\n  ''').gte('submitted_at',since.toIso8601String());"

if old not in text:
    import sys; sys.exit("Anchor not found.")

text = text.replace(old, new)
p.write_text(text, encoding='utf-8')
print("Fixed: scout_name, farm_id, issue, photo_urls added to query.")