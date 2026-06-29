import pathlib

# Fix 1: analytics_data.dart - add missing import
p1 = pathlib.Path('lib/shared/providers/analytics_data.dart')
text1 = p1.read_text(encoding='utf-8')
old_import = "import 'farm_providers.dart';"
new_import = "import 'farm_providers.dart';\nimport 'locale_provider.dart';"
if old_import not in text1:
    raise SystemExit("Import anchor not found in analytics_data.dart - aborting.")
text1 = text1.replace(old_import, new_import, 1)
p1.write_text(text1, encoding='utf-8')
print("analytics_data.dart: added locale_provider.dart import.")

# Fix 2: analytics_screen.dart - remove invalid const wrappers (3 occurrences)
p2 = pathlib.Path('lib/features/analytics/presentation/analytics_screen.dart')
text2 = p2.read_text(encoding='utf-8')
old_const = "const Center(child: Padding(padding: EdgeInsets.all(20), child: Text(s.noData, style: TextStyle(color: _AP.slate, fontSize: 13))))"
new_const = "Center(child: Padding(padding: const EdgeInsets.all(20), child: Text(s.noData, style: const TextStyle(color: _AP.slate, fontSize: 13))))"
count = text2.count(old_const)
if count == 0:
    raise SystemExit("const wrapper anchor not found in analytics_screen.dart - aborting.")
text2 = text2.replace(old_const, new_const)
p2.write_text(text2, encoding='utf-8')
print(f"analytics_screen.dart: fixed {count} invalid const wrapper(s).")