import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

# Remove duplicate scout_name from the select query
text = text.replace(
    "    id, submitted_at, started_at, variety_name, greenhouse_id, scout_id, scout_name,\n    greenhouses!inner(code),\n    inspection_findings(category, severity, issue, photo_urls)",
    "    id, submitted_at, started_at, variety_name, greenhouse_id, scout_id, scout_name,\n    greenhouses!inner(code, farm_id),\n    inspection_findings(category, severity, issue, photo_urls)"
)

# Also fix analytics_data.dart which had scout_name added
p2 = pathlib.Path('lib/shared/providers/analytics_data.dart')
text2 = p2.read_text(encoding='utf-8')
text2 = text2.replace(
    "    id, submitted_at, started_at, variety_name, greenhouse_id, scout_id, scout_name,",
    "    id, submitted_at, started_at, variety_name, greenhouse_id, scout_id, scout_name,"
)

p.write_text(text, encoding='utf-8')
print("reports_screen.dart: duplicate scout_name removed.")

# Check for duplicate in analytics too
if text2.count('scout_name,') > 1:
    text2 = text2.replace(
        "    id, submitted_at, started_at, variety_name, greenhouse_id, scout_id, scout_name,\n    scout_name,",
        "    id, submitted_at, started_at, variety_name, greenhouse_id, scout_id, scout_name,"
    )
    p2.write_text(text2, encoding='utf-8')
    print("analytics_data.dart: duplicate removed.")
else:
    print("analytics_data.dart: clean.")