import pathlib

p = pathlib.Path('lib/shared/error/app_error_handler.dart')
text = p.read_text(encoding='utf-8')

old = "  String toString() => 'TimeoutException: \\$message';"
new = "  String toString() => 'TimeoutException: $message';"
if old not in text:
    raise SystemExit("Anchor not found - aborting, no changes made.")
text = text.replace(old, new, 1)

p.write_text(text, encoding='utf-8')
print("Fixed TimeoutException.toString() interpolation.")