import pathlib, re

# --- 1. Fix locale_provider.dart (add back initLocale as a top-level function) ---
locale = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LocaleNotifier extends Notifier<String> {
  @override
  String build() => 'en';

  Future<void> setLocale(String locale) async {
    state = locale;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('locale', locale);
  }

  Future<void> loadSaved() async {
    final prefs = await SharedPreferences.getInstance();
    state = prefs.getString('locale') ?? 'en';
  }
}

final localeProvider = NotifierProvider<LocaleNotifier, String>(LocaleNotifier.new);

// Called from main() before runApp so the saved locale is restored at startup
Future<void> initLocale() async {
  final prefs = await SharedPreferences.getInstance();
  _savedLocale = prefs.getString('locale') ?? 'en';
}

String _savedLocale = 'en';
String get initialLocale => _savedLocale;
"""
pathlib.Path('lib/shared/providers/locale_provider.dart').write_text(locale, encoding='utf-8')

# --- 2. Patch main.dart: seed the notifier with the saved locale after ProviderScope exists ---
main = pathlib.Path('lib/main.dart').read_text(encoding='utf-8')

# Replace the build method of FlowerScoutApp to seed locale on first build
old = """  @override
  Widget build(BuildContext context, WidgetRef ref) {
    ref.watch(localeProvider); // force rebuild on language change
    return MaterialApp("""

new = """  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Seed saved locale into the notifier once on startup
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ref.read(localeProvider.notifier).loadSaved();
    });
    ref.watch(localeProvider);
    return MaterialApp("""

main = main.replace(old, new)
pathlib.Path('lib/main.dart').write_text(main, encoding='utf-8')
print('Done')