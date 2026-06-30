import pathlib, re

s = pathlib.Path('lib/shared/l10n/app_strings.dart').read_text(encoding='utf-8')

# Show relevant key values in both languages
for key in ['cancel', 'errorUnexpected', 'errorLoadReports', 'couldNotLoad']:
    # Find English value
    m = re.search(rf"'{key}':\s*AppStrings\(([^)]+)\)", s)
    # Just show the getter
    m2 = re.search(rf"String get {key} => ([^\n]+)", s)
    if m2:
        print(f"{key}: {m2.group(1).strip()}")

# Show structure of app_strings to understand how to add keys
lines = s.split('\n')
print("\n=== First 30 lines of app_strings.dart ===")
for i, l in enumerate(lines[:30], 1):
    print(f"{i}: {l}")