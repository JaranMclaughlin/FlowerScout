import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

# Fix PDF header — remove the over-escaped dollar sign
old_pdf = '\'Generated \\${DateTime.now().toString().split(".").first}\','
new_pdf = "'Generated \\${DateTime.now().toString().split(\\\".\\\").first}',"
# Simpler: just target the literal broken text directly
text = text.replace(
    "pw.Text('Generated \\\\${DateTime.now().toString().split(\".\").first}',",
    "pw.Text('Generated ${DateTime.now().toString().split(\".\").first}',"
)

# Fix Excel header — same over-escaping issue
text = text.replace(
    "TextCellValue('Generated: \\\\${DateTime.now().toString().split(\\\\' \\\\').first}');",
    "TextCellValue('Generated: ${DateTime.now().toString().split(' ').first}');"
)

p.write_text(text, encoding='utf-8')
print("Done — verifying result below.")