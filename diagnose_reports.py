import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

before_len = len(text)
print(f"File size before: {before_len} chars")
print(f"Contains 'app_error_handler' import already: {'app_error_handler' in text}")
print(f"Contains old Excel catch block: {'Excel export failed' in text}")
print(f"Contains old PDF catch block: {'PDF export failed' in text}")