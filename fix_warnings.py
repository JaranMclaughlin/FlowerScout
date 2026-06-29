import pathlib, shutil

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
shutil.copy(p, p.with_suffix('.dart.bak5'))
text = p.read_text(encoding='utf-8')
original = text

old_heading = "  static const heading = TextStyle(fontFamily: 'Georgia', fontSize: 20,"
new_heading = "  // ignore: unused_field\n  static const heading = TextStyle(fontFamily: 'Georgia', fontSize: 20,"
if old_heading in text:
    text = text.replace(old_heading, new_heading, 1)
    print("Fix 1 done")
else:
    print("ERROR: heading not found"); raise SystemExit(1)

old_s = "        final s    = ref.watch(stringsProvider);\n"
alt_s = "        final s = ref.watch(stringsProvider);\n"
if old_s in text:
    text = text.replace(old_s, "", 1)
    print("Fix 2 done")
elif alt_s in text:
    text = text.replace(alt_s, "", 1)
    print("Fix 2 alt done")
else:
    print("ERROR: s line not found"); raise SystemExit(1)

p.write_text(text, encoding='utf-8')
print("Saved.")