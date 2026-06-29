import pathlib, re

p = pathlib.Path('pubspec.yaml')
text = p.read_text(encoding='utf-8')

if 'assets/images/' not in text:
    text = text.replace(
        "  assets:\n    - .env",
        "  assets:\n    - .env\n    - assets/images/"
    )
    p.write_text(text, encoding='utf-8')
    print("pubspec.yaml: assets/images/ registered.")
else:
    print("Already registered.")