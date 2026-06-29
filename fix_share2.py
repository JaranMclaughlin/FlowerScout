import pathlib, sys

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

old = "    SharePlus.instance.share(ShareParams(text: lines.join('\n'"
old2 = "'"
# find and fix the broken join call
text = text.replace(
    "    SharePlus.instance.share(ShareParams(text: lines.join('\n'\n')));",
    "    SharePlus.instance.share(ShareParams(text: lines.join('\\n')));"
)

p.write_text(text, encoding='utf-8')
print("Fixed.")