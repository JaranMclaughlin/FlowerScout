import pathlib

locale_content = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../l10n/app_strings.dart';

class LocaleNotifier extends Notifier<String> {
  final String _initial;

  LocaleNotifier() : _initial = 'en';
  LocaleNotifier.withInitial(String initial) : _initial = initial;

  @override
  String build() => _initial;

  Future<void> setLocale(String locale) async {
    state = locale;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('locale', locale);
  }

  // Alias for backward compat
  Future<void> setLanguage(String locale) => setLocale(locale);
}

final localeProvider = NotifierProvider<LocaleNotifier, String>(LocaleNotifier.new);

final stringsProvider = Provider<AppStrings>((ref) {
  return AppStrings.of(ref.watch(localeProvider));
});

// Called from main() before runApp - reads saved locale into [initialLocale]
Future<void> initLocale() async {
  final prefs = await SharedPreferences.getInstance();
  _savedLocale = prefs.getString('locale') ?? 'en';
}

String _savedLocale = 'en';
String get initialLocale => _savedLocale;
"""

pathlib.Path('lib/shared/providers/locale_provider.dart').write_text(locale_content, encoding='utf-8')
print('locale_provider.dart done')