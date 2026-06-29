import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

# The broken two-line call
text = text.replace(
    "    SharePlus.instance.share(ShareParams(text: lines.join('\"\n\"')));" ,
    "    SharePlus.instance.share(ShareParams(text: lines.join('\\n')));"
)

# Try the exact repr we saw
text = text.replace(
    "    SharePlus.instance.share(ShareParams(text: lines.join('\n" + "'"  + "')));" ,
    "    SharePlus.instance.share(ShareParams(text: lines.join('\\n')));"
)

p.write_text(text, encoding='utf-8')
print("Done.")