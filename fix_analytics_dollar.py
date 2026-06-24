import pathlib

p = pathlib.Path('lib/features/analytics/presentation/analytics_screen.dart')
text = p.read_text(encoding='utf-8')

count = text.count('\\$')
text = text.replace('\\$', '$')

p.write_text(text, encoding='utf-8')
print(f"Fixed {count} occurrence(s) of stray backslash before $.")