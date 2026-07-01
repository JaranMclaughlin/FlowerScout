import pathlib

p = pathlib.Path('pubspec.yaml')
text = p.read_text(encoding='utf-8')

old = "  excel: ^4.0.6\n"
new = "  excel: ^4.0.6\n  sentry_flutter: ^9.6.0\n"
if old not in text:
    raise SystemExit("Anchor not found - aborting, no changes made.")
text = text.replace(old, new, 1)

p.write_text(text, encoding='utf-8')
print("pubspec.yaml updated: added sentry_flutter dependency.")