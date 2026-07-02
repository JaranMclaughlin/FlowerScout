import pathlib

p = pathlib.Path('.github/workflows/ci.yml')
text = p.read_text(encoding='utf-8')

old = "        run: flutter analyze --no-pub --fatal-infos=false --fatal-warnings=false"
new = "        run: flutter analyze --no-pub --no-fatal-infos --no-fatal-warnings"
if old not in text:
    raise SystemExit("Anchor not found - aborting.")
text = text.replace(old, new, 1)

p.write_text(text, encoding='utf-8')
print("Fixed: using --no-fatal-infos and --no-fatal-warnings flags.")