import pathlib

p = pathlib.Path('lib/shared/error/app_error_handler.dart')
lines = p.read_text(encoding='utf-8').splitlines(keepends=True)

for i, line in enumerate(lines):
    print(f"{i}: {line!r}")