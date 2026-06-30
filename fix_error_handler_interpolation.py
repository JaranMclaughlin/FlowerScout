import pathlib

p = pathlib.Path('lib/shared/error/app_error_handler.dart')
text = p.read_text(encoding='utf-8')

old = "    debugPrint('[error][\\$context] \\${error.runtimeType}: \\$error');"
new = "    debugPrint('[error][$context] ${error.runtimeType}: $error');"
if old not in text:
    raise SystemExit("Anchor not found - aborting, no changes made.")
text = text.replace(old, new, 1)

p.write_text(text, encoding='utf-8')
print("app_error_handler.dart fixed: debugPrint now actually interpolates context/error instead of printing literal placeholder text.")