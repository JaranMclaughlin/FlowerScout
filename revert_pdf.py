import pathlib

p = pathlib.Path('pubspec.yaml')
text = p.read_text(encoding='utf-8')

old1 = "  pdf: ^3.13.0"
new1 = "  pdf: ^3.12.0"
if old1 in text:
    text = text.replace(old1, new1, 1)
    print("Reverted pdf to 3.12.0")

old2 = "  printing: ^5.15.0"
new2 = "  printing: ^5.14.3"
if old2 in text:
    text = text.replace(old2, new2, 1)
    print("Reverted printing to 5.14.3")

p.write_text(text, encoding='utf-8')