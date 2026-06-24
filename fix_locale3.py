import pathlib

# Add back stringsProvider and setLanguage alias to locale_provider.dart
locale = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'app_strings.dart';

class LocaleNotifier extends Notifier<String> {
  @override
  String build() => _savedLocale;

  Future<void> setLocale(String locale) async {
    state = locale;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('locale', locale);
  }

  // Alias kept for backward compatibility with login_screen & settings_screen
  Future<void> setLanguage(String locale) => setLocale(locale);

  Future<void> loadSaved() async {
    final prefs = await SharedPreferences.getInstance();
    state = prefs.getString('locale') ?? 'en';
  }
}

final localeProvider = NotifierProvider<LocaleNotifier, String>(LocaleNotifier.new);

// Derived provider so screens can just watch stringsProvider
final stringsProvider = Provider<AppStrings>((ref) {
  return AppStrings.of(ref.watch(localeProvider));
});

Future<void> initLocale() async {
  final prefs = await SharedPreferences.getInstance();
  _savedLocale = prefs.getString('locale') ?? 'en';
}

String _savedLocale = 'en';
String get initialLocale => _savedLocale;
"""

p = pathlib.Path('lib/shared/providers/locale_provider.dart')
p.write_text(locale, encoding='utf-8')
print('Done')