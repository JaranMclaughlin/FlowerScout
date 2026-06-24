import pathlib

content = """import 'package:flutter_riverpod/flutter_riverpod.dart';
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
"""

pathlib.Path('lib/shared/providers/locale_provider.dart').write_text(content, encoding='utf-8')
print('Done')