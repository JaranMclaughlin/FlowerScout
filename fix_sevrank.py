import pathlib
p = pathlib.Path('lib/shared/providers/analytics_data.dart')
text = p.read_text(encoding='utf-8')
text = text.replace("const _sevRank = ", "const sevRank = ")
text = text.replace("_sevRank[fm[", "sevRank[fm[")
text = text.replace("_sevRank[worst[", "sevRank[worst[")
p.write_text(text, encoding='utf-8')
print("Done.")