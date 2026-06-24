import pathlib

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
txt = p.read_text(encoding='utf-8')

txt = txt.replace(
    'AppStrings get s => AppStrings.of(ref.read(localeProvider));',
    'AppStrings get s => AppStrings.of(ref.watch(localeProvider));'
)

p.write_text(txt, encoding='utf-8')
print('done')