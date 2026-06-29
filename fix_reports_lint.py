import pathlib, re, sys

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
if not p.exists():
    sys.exit(f"Not found: {p}")

text = p.read_text(encoding='utf-8')
original = text

# 1. _s → s
text = re.sub(r'\bfinal _s\b', 'final s', text)
text = re.sub(r'(?<![.\w])_s(?![\w])', 's', text)

# 2. __ → _
text = re.sub(r'\b__\b', '_', text)

# 3. if bodies without braces
text = re.sub(
    r'(?m)\b((?:else\s+)?if)\s*(\([^)]*\))\s*\r?\n(\s+[^\n{][^\n]*;)',
    lambda m: f"{m.group(1)}{m.group(2)} {{\n{m.group(3)}\n}}",
    text
)

# 4. for bodies without braces
text = re.sub(
    r'(?m)\b(for\s*\([^)]*\))\s*\r?\n(\s+[^\n{][^\n]*;)',
    lambda m: f"{m.group(1)} {{\n{m.group(2)}\n}}",
    text
)

if text == original:
    print("No changes — already fixed or anchors differ.")
else:
    p.write_text(text, encoding='utf-8')
    print("Done: _s->s, __->_, if/for braces added.")