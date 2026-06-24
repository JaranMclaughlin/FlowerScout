import pathlib

locale_content = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../l10n/app_strings.dart';

// SharedPreferences on Flutter Web prefixes all keys with 'flutter.'
// Use a top-level const so the key is consistent everywhere.
const _kLocaleKey = 'locale';

class LocaleNotifier extends Notifier<String> {
  final String _initial;

  LocaleNotifier() : _initial = 'en';
  LocaleNotifier.withInitial(String initial) : _initial = initial;

  @override
  String build() {
    print('[LocaleNotifier] build() -> initial=$_initial');
    return _initial;
  }

  Future<void> setLocale(String locale) async {
    print('[LocaleNotifier] setLocale($locale)');
    state = locale;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_kLocaleKey, locale);
    // Debug: print all keys to confirm what is actually stored
    print('[LocaleNotifier] all prefs keys: ${prefs.getKeys()}');
    print('[LocaleNotifier] read back: ${prefs.getString(_kLocaleKey)}');
  }

  Future<void> setLanguage(String locale) => setLocale(locale);
}

final localeProvider = NotifierProvider<LocaleNotifier, String>(LocaleNotifier.new);

final stringsProvider = Provider<AppStrings>((ref) {
  final code = ref.watch(localeProvider);
  print('[stringsProvider] language code = $code');
  return AppStrings.of(code);
});

Future<void> initLocale() async {
  final prefs = await SharedPreferences.getInstance();
  // Print ALL keys so we can see exactly what is stored
  print('[initLocale] all keys in prefs: \${prefs.getKeys()}');
  final saved = prefs.getString(_kLocaleKey);
  print('[initLocale] getString(${'_kLocaleKey'}) = $saved');
  _savedLocale = saved ?? 'en';
  print('[initLocale] _savedLocale set to $_savedLocale');
}

String _savedLocale = 'en';
String get initialLocale => _savedLocale;
"""

pathlib.Path('lib/shared/providers/locale_provider.dart').write_text(locale_content, encoding='utf-8')
print('Done')