import pathlib, sys

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')
original = text

fixes = [
    # line 1124 - header date
    (r"pw.Text(\'Generated \${DateTime.now().toString().split(\".\").first}\'",
     r"pw.Text('Generated ${DateTime.now().toString().split(\".\").first}'"),

    # line 1133-1136 - KPI values
    ("_pdfKpi('Inspections', '\\${stats.total}', forest, mist),",
     "_pdfKpi('Inspections', '${stats.total}', forest, mist),"),

    ("_pdfKpi('Disease', '\\${stats.disease}', redAccent, redBg),",
     "_pdfKpi('Disease', '${stats.disease}', redAccent, redBg),"),

    ("_pdfKpi('Pests', '\\${stats.pest}', amberAccent, amberBg),",
     "_pdfKpi('Pests', '${stats.pest}', amberAccent, amberBg),"),

    ("_pdfKpi('Critical', '\\${stats.critical}', criticalAccent, criticalBg),",
     "_pdfKpi('Critical', '${stats.critical}', criticalAccent, criticalBg),"),

    # line 1160 - greenhouse findings
    ("pw.Text('\\${g.findings} findings'",
     "pw.Text('${g.findings} findings'"),

    # line 1164 - table heading
    ("pw.Text('Inspection Records (\\${rows.length})'",
     "pw.Text('Inspection Records (${rows.length})'"),
]

for old, new in fixes:
    if old in text:
        text = text.replace(old, new)
        print(f"Fixed: {old[:60]}...")
    else:
        print(f"MISSED: {old[:60]}...")

if text != original:
    p.write_text(text, encoding='utf-8')
    print("\nAll interpolation fixes written.")
else:
    print("\nNo changes made.")