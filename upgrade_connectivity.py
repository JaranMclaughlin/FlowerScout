import pathlib

p = pathlib.Path('pubspec.yaml')
text = p.read_text(encoding='utf-8')

old = "  connectivity_plus: ^6.1.4"
new = "  connectivity_plus: ^7.2.0"
if old not in text:
    raise SystemExit("Anchor not found - aborting, no changes made.")
text = text.replace(old, new, 1)

p.write_text(text, encoding='utf-8')
print("pubspec.yaml updated: connectivity_plus 6 -> 7.")