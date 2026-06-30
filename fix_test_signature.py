import pathlib

p = pathlib.Path('test/shared/analytics_data_test.dart')
text = p.read_text(encoding='utf-8')

replacements = [
    ("ReportStats.fromInspections(records, 'today', base);",
     "ReportStats.fromInspections(records, 'today', base, 'en');"),
    ("ReportStats.fromInspections(records, '7days', monday);",
     "ReportStats.fromInspections(records, '7days', monday, 'en');"),
    ("ReportStats.fromInspections(records, '30days', since);",
     "ReportStats.fromInspections(records, '30days', since, 'en');"),
    ("ReportStats.fromInspections(records, '3months', since);",
     "ReportStats.fromInspections(records, '3months', since, 'en');"),
    ("ReportStats.fromInspections([], '7days', DateTime(2026, 6, 29));",
     "ReportStats.fromInspections([], '7days', DateTime(2026, 6, 29), 'en');"),
]

total = 0
for old, new in replacements:
    count = text.count(old)
    if count == 0:
        raise SystemExit(f"Anchor not found: {old!r} - aborting, no changes made.")
    text = text.replace(old, new)
    total += count

# The two 'now' calls (both identical text) - replace all occurrences
old_now = "ReportStats.fromInspections(records, '7days', now);"
new_now = "ReportStats.fromInspections(records, '7days', now, 'en');"
count_now = text.count(old_now)
if count_now == 0:
    raise SystemExit("'now' anchor not found - aborting, no changes made.")
text = text.replace(old_now, new_now)
total += count_now

p.write_text(text, encoding='utf-8')
print(f"Fixed {total} call site(s) in analytics_data_test.dart - added missing lang argument.")