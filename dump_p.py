import pathlib, re

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

# Find the _P class
m = re.search(r'\nclass _P \{.*?\}\n', text, flags=re.DOTALL)
if m:
    print("_P class found:")
    print(m.group())
else:
    print("_P class NOT found — may have different name")

# Show all _P.x tokens used
tokens = sorted(set(re.findall(r'_P\.\w+', text)))
print("\nTokens used:", tokens)