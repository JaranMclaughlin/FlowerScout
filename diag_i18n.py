import pathlib, re

# Check what strings are in app_strings.dart
s = pathlib.Path('lib/shared/l10n/app_strings.dart').read_text(encoding='utf-8')

# Check settings screen for hardcoded English strings
p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
t = p.read_text(encoding='utf-8')

print("=== Hardcoded English strings in settings_screen.dart ===")
# Find all single-quoted strings that look like UI labels
matches = re.findall(r"label:\s*'([^']+)'", t)
for m in sorted(set(matches)):
    print(f"  label: '{m}'")

print("\n=== Hardcoded dropdown items ===")
matches2 = re.findall(r"items:\s*\[([^\]]+)\]", t)
for m in matches2:
    items = re.findall(r"'([^']+)'", m)
    if items:
        print(f"  {items}")

print("\n=== Keys available in AppStrings ===")
keys = re.findall(r'String get (\w+)', s)
for k in sorted(keys):
    print(f"  {k}")