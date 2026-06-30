import pathlib, re

s = pathlib.Path('lib/shared/l10n/app_strings.dart').read_text(encoding='utf-8')

# Check for relevant keys
for key in ['cancel', 'retry', 'error', 'export', 'failed', 'couldNot']:
    matches = re.findall(rf"String get (\w*{key}\w*)", s, re.IGNORECASE)
    if matches:
        print(f"{key}: {matches}")