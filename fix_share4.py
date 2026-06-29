import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

# Find and replace the broken two-line SharePlus call
# The file literally has: lines.join('\n'));\n  where \n is a real newline mid-string
broken = "    SharePlus.instance.share(ShareParams(text: lines.join('\n')));"
fixed  = "    SharePlus.instance.share(ShareParams(text: lines.join('\\n')));"

if broken in text:
    text = text.replace(broken, fixed)
    p.write_text(text, encoding='utf-8')
    print("Fixed via direct match.")
else:
    # Manual line-level fix
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if "SharePlus.instance.share(ShareParams(text: lines.join('" == line.strip():
            # next line is just "')));"
            if i+1 < len(lines) and lines[i+1].strip() == "')));":
                indent = len(line) - len(line.lstrip())
                lines[i] = " " * indent + "SharePlus.instance.share(ShareParams(text: lines.join('\\n')));"
                lines[i+1] = ""
                print(f"Fixed at line {i+1}")
                break
    text = '\n'.join(lines)
    p.write_text(text, encoding='utf-8')
    print("Done via line scan.")