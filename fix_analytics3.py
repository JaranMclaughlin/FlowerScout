import pathlib
p = pathlib.Path('lib/features/analytics/presentation/analytics_screen.dart')
t = p.read_text(encoding='utf-8')

# Add s getter to state class before build
old = "  @override\n  Widget build(BuildContext context) {\n    final s = ref.watch(stringsProvider);"
new = "  AppStrings get s => AppStrings.of(ref.read(localeProvider));\n\n  @override\n  Widget build(BuildContext context) {\n    final s = ref.watch(stringsProvider);"
if old not in t: raise SystemExit('anchor not found')
t = t.replace(old, new, 1)

# Remove s param from _segmented and _legend since they can now use the getter
old2 = "  Widget _segmented(AppStrings s) =>"
new2 = "  Widget _segmented() =>"
t = t.replace(old2, new2, 1)

old3 = "  Widget _legend(AppStrings s) =>"
new3 = "  Widget _legend() =>"
t = t.replace(old3, new3, 1)

# Fix call sites
t = t.replace('_segmented(s),', '_segmented(),')
t = t.replace('_legend(s),', '_legend(),')

# Make sure AppStrings is imported
if 'app_strings' not in t:
    old4 = "import '../../../shared/providers/locale_provider.dart';"
    new4 = "import '../../../shared/providers/locale_provider.dart';\nimport '../../../shared/l10n/app_strings.dart';"
    t = t.replace(old4, new4, 1)

# Add s to all helper methods that use it by passing via getter (already works via class getter)
# But _buildHeader, _buildKpiRow etc need s passed or use getter
# Since getter is on class, s. calls in those methods will work automatically
# EXCEPT they shadow s with local var - remove local s in build to avoid conflict
old5 = "    final s = ref.watch(stringsProvider);\n"
new5 = "    ref.watch(stringsProvider); // keep reactive - use getter s\n"
if old5 in t:
    t = t.replace(old5, new5, 1)

p.write_text(t, encoding='utf-8')
print('analytics_screen.dart fixed.')