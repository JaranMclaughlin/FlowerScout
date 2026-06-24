import pathlib

locale_content = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../l10n/app_strings.dart';

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
    await prefs.setString('locale', locale);
    final check = prefs.getString('locale');
    print('[LocaleNotifier] saved and re-read: $check');
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
  final saved = prefs.getString('locale');
  print('[initLocale] saved locale from prefs = $saved');
  _savedLocale = saved ?? 'en';
  print('[initLocale] _savedLocale set to $_savedLocale');
}

String _savedLocale = 'en';
String get initialLocale => _savedLocale;
"""

pathlib.Path('lib/shared/providers/locale_provider.dart').write_text(locale_content, encoding='utf-8')
print('Done')