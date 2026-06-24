import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

count = text.count('Â·')
text = text.replace('Â·', '·')

p.write_text(text, encoding='utf-8')
print(f"Replaced {count} occurrence(s) of mojibake with proper middle dot.")