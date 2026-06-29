import pathlib

p = pathlib.Path('lib/features/maps/presentation/maps_screen.dart')
txt = p.read_text(encoding='utf-8')

txt = txt.replace(
    '  Widget build(BuildContext context) {\n    final trailAsync = ref.watch(trailByIdProvider(widget.trailId));',
    '  Widget build(BuildContext context) {\n    final s = AppStrings.of(ref.watch(localeProvider));\n    final trailAsync = ref.watch(trailByIdProvider(widget.trailId));'
)

p.write_text(txt, encoding='utf-8')
print('done')