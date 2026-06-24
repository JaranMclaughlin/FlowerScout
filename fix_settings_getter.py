import pathlib
p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
t = p.read_text(encoding='utf-8')

# Add s getter to state class and fix Settings title
old1 = "  @override\n  Widget build(BuildContext context) {\n    // Populate profile fields once loaded"
new1 = "  AppStrings get s => AppStrings.of(ref.read(localeProvider));\n\n  @override\n  Widget build(BuildContext context) {\n    // Populate profile fields once loaded"
if old1 not in t: raise SystemExit('anchor 1 not found')
t = t.replace(old1, new1, 1)

# Fix hardcoded Settings title in rail
old2 = "child: Text('Settings', style: TextStyle(fontFamily: 'Georgia',\nfontSize: 22, fontWeight: FontWeight.w700, color: _C.ink)),"
if old2 not in t:
    old2 = "        child: Text('Settings', style: TextStyle(fontFamily: 'Georgia',\n            fontSize: 22, fontWeight: FontWeight.w700, color: _C.ink)),"
new2 = "child: Text(s.settingsTitle, style: const TextStyle(fontFamily: 'Georgia',\n            fontSize: 22, fontWeight: FontWeight.w700, color: _C.ink)),"
if old2 in t:
    t = t.replace(old2, new2, 1)

# Fix const issues - items with s. can't be const
t = t.replace("items: [s.", "items: [s.")  # already non-const
# Remove const from _buildRail Text
t = t.replace("const Padding(\n        padding: EdgeInsets.fromLTRB(20, 28, 20, 16),\n        child: Text('Settings'",
              "Padding(\n        padding: const EdgeInsets.fromLTRB(20, 28, 20, 16),\n        child: Text(s.settingsTitle")

# Add import for locale_provider if missing
if "locale_provider" not in t:
    old_imp = "import 'package:flutter_riverpod/flutter_riverpod.dart';"
    new_imp = "import 'package:flutter_riverpod/flutter_riverpod.dart';\nimport '../../../shared/providers/locale_provider.dart';"
    if old_imp in t:
        t = t.replace(old_imp, new_imp, 1)

# Add import for app_strings if missing  
if "app_strings" not in t:
    old_imp2 = "import '../../../shared/providers/locale_provider.dart';"
    new_imp2 = "import '../../../shared/providers/locale_provider.dart';\nimport '../../../shared/l10n/app_strings.dart';"
    if old_imp2 in t:
        t = t.replace(old_imp2, new_imp2, 1)

p.write_text(t, encoding='utf-8')
print('settings_screen.dart - s getter added.')