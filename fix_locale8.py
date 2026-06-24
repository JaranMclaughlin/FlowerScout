import pathlib

content = """import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../l10n/app_strings.dart';

// ignore: avoid_web_libraries_in_flutter
import 'dart:html' as html;

const _kLocaleKey = 'flutter.locale';

class LocaleNotifier extends Notifier<String> {
  final String _initial;
  LocaleNotifier() : _initial = 'en';
  LocaleNotifier.withInitial(String initial) : _initial = initial;

  @override
  String build() => _initial;

  Future<void> setLocale(String locale) async {
    state = locale;
    if (kIsWeb) {
      html.window.localStorage[_kLocaleKey] = locale;
      print('[LocaleNotifier] wrote to localStorage: $locale');
    } else {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('locale', locale);
    }
  }

  Future<void> setLanguage(String locale) => setLocale(locale);
}

final localeProvider = NotifierProvider<LocaleNotifier, String>(LocaleNotifier.new);

final stringsProvider = Provider<AppStrings>((ref) {
  return AppStrings.of(ref.watch(localeProvider));
});

Future<void> initLocale() async {
  if (kIsWeb) {
    final saved = html.window.localStorage[_kLocaleKey];
    print('[initLocale] localStorage[$_kLocaleKey] = $saved');
    _savedLocale = saved ?? 'en';
  } else {
    final prefs = await SharedPreferences.getInstance();
    await prefs.reload();
    _savedLocale = prefs.getString('locale') ?? 'en';
  }
  print('[initLocale] _savedLocale = $_savedLocale');
}

String _savedLocale = 'en';
String get initialLocale => _savedLocale;
"""

pathlib.Path('lib/shared/providers/locale_provider.dart').write_text(content, encoding='utf-8')
print('Done')