import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

idx = text.find('SnackBar(')
snippet = text[idx:idx+150]
print(repr(snippet))