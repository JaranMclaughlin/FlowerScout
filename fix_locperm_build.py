import pathlib
p = pathlib.Path('lib/features/auth/presentation/location_permission_screen.dart')
txt = p.read_text(encoding='utf-8', errors='replace')
txt = txt.replace(
    '  Widget build(BuildContext context) {\n    final isTablet = MediaQuery.of(context).size.shortestSide >= 600;',
    '  Widget build(BuildContext context) {\n    final s = AppStrings.of(ref.watch(localeProvider));\n    final isTablet = MediaQuery.of(context).size.shortestSide >= 600;'
)
p.write_text(txt, encoding='utf-8')
print('done')