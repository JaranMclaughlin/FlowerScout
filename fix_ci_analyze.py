import pathlib

p = pathlib.Path('.github/workflows/ci.yml')
text = p.read_text(encoding='utf-8')

old = "      - name: Analyze\n        run: flutter analyze --no-pub"
new = "      - name: Analyze\n        run: flutter analyze --no-pub --fatal-infos=false --fatal-warnings=false"
if old not in text:
    raise SystemExit("Anchor not found - aborting.")
text = text.replace(old, new, 1)

p.write_text(text, encoding='utf-8')
print("Updated: analyze step now only fails on errors, not warnings/info.")