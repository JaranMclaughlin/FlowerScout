import pathlib

locale_content = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../l10n/app_strings.dart';

const _kLocaleKey = 'locale';

class LocaleNotifier extends Notifier<String> {
  final String _initial;
  LocaleNotifier() : _initial = 'en';
  LocaleNotifier.withInitial(String initial) : _initial = initial;

  @override
  String build() => _initial;

  Future<void> setLocale(String locale) async {
    state = locale;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_kLocaleKey, locale);
  }

  Future<void> setLanguage(String locale) => setLocale(locale);
}

final localeProvider = NotifierProvider<LocaleNotifier, String>(LocaleNotifier.new);

final stringsProvider = Provider<AppStrings>((ref) {
  return AppStrings.of(ref.watch(localeProvider));
});

Future<void> initLocale() async {
  // reload() forces SharedPreferences to re-read from localStorage on web
  // instead of returning a stale in-memory cache from a previous instance
  final prefs = await SharedPreferences.getInstance();
  await prefs.reload();
  final saved = prefs.getString(_kLocaleKey);
  print('[initLocale] after reload, locale = $saved');
  _savedLocale = saved ?? 'en';
}

String _savedLocale = 'en';
String get initialLocale => _savedLocale;
"""

pathlib.Path('lib/shared/providers/locale_provider.dart').write_text(locale_content, encoding='utf-8')
print('Done')