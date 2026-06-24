import pathlib

p = pathlib.Path('lib/shared/providers/locale_provider.dart')
p.write_text(
"""import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../l10n/app_strings.dart';

const _kLangKey = 'flowerscout_language';

SharedPreferences? _prefsInstance;

class LocaleNotifier extends Notifier<String> {
  @override
  String build() {
    return _prefsInstance?.getString(_kLangKey) ?? 'en';
  }

  Future<void> setLanguage(String code) async {
    state = code;
    _prefsInstance ??= await SharedPreferences.getInstance();
    await _prefsInstance!.setString(_kLangKey, code);
  }
}

final localeProvider = NotifierProvider<LocaleNotifier, String>(
  LocaleNotifier.new,
);

final stringsProvider = Provider<AppStrings>((ref) {
  final code = ref.watch(localeProvider);
  return AppStrings.of(code);
});

Future<void> initLocale() async {
  _prefsInstance = await SharedPreferences.getInstance();
}
""", encoding='utf-8')
print('Done')