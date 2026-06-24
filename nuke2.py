import pathlib
pathlib.Path('lib/shared/providers/locale_provider.dart').write_text(
"""import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../l10n/app_strings.dart';

final localeProvider = StateProvider<String>((ref) => 'en');

final stringsProvider = Provider<AppStrings>((ref) {
  return AppStrings.of(ref.watch(localeProvider));
});

Future<void> initLocale() async {}
""", encoding='utf-8')
print('Done')