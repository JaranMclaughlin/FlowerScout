import pathlib

main = pathlib.Path('lib/main.dart')
txt = main.read_text(encoding='utf-8')

old = '''class FlowerScoutApp extends StatelessWidget {
  const FlowerScoutApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Flower Scout',
      theme: AppTheme.lightTheme,
      home: const _AuthGate(),
    );
  }
}'''

new = '''class FlowerScoutApp extends ConsumerWidget {
  const FlowerScoutApp({super.key});
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    ref.watch(localeProvider); // rebuild entire app on language change
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Flower Scout',
      theme: AppTheme.lightTheme,
      home: const _AuthGate(),
    );
  }
}'''

if old in txt:
    txt = txt.replace(old, new)
    print('Fixed: FlowerScoutApp now watches localeProvider')
else:
    print('ERROR: pattern not found')

main.write_text(txt, encoding='utf-8')