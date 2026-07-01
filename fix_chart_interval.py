import pathlib, sys

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

old = "bottomTitles:AxisTitles(sideTitles:SideTitles(showTitles:true,reservedSize:24,"
new = "bottomTitles:AxisTitles(sideTitles:SideTitles(showTitles:true,reservedSize:24,interval:1,"

count = text.count(old)
if count == 0:
    sys.exit("Anchor not found.")

text = text.replace(old, new)
p.write_text(text, encoding='utf-8')
print(f"Fixed {count} chart axis(es): interval:1 added to prevent repeated day labels.")