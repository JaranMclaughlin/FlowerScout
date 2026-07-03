import pathlib

p = pathlib.Path('pubspec.yaml')
text = p.read_text(encoding='utf-8')

old1 = "  pdf: ^3.12.0"
new1 = "  pdf: ^3.13.0"
if old1 not in text:
    raise SystemExit("pdf anchor not found - aborting.")
text = text.replace(old1, new1, 1)

old2 = "  printing: ^5.14.3"
new2 = "  printing: ^5.15.0"
if old2 not in text:
    raise SystemExit("printing anchor not found - aborting.")
text = text.replace(old2, new2, 1)

p.write_text(text, encoding='utf-8')
print("pubspec.yaml updated: pdf 3.12->3.13, printing 5.14->5.15.")