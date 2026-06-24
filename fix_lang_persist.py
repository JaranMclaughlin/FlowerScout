import pathlib

# ── 1. Fix locale_provider.dart — load synchronously from pre-initialized prefs
locale = pathlib.Path('lib/shared/providers/locale_provider.dart')
locale.write_text(r"""
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../l10n/app_strings.dart';

const _kLangKey = 'app_language';

// Seeded at app startup in main.dart before runApp
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

/// Call this in main() before runApp
Future<void> initLocale() async {
  _prefsInstance = await SharedPreferences.getInstance();
}
""".lstrip(), encoding='utf-8')
print('Fixed: locale_provider.dart')

# ── 2. Fix main.dart — call initLocale() before runApp
main = pathlib.Path('lib/main.dart')
txt = main.read_text(encoding='utf-8')

if 'initLocale' not in txt:
    txt = txt.replace(
        "import 'shared/providers/farm_providers.dart';",
        "import 'shared/providers/farm_providers.dart';\nimport 'shared/providers/locale_provider.dart';"
    )
    txt = txt.replace(
        "  await dotenv.load(fileName: '.env');",
        "  await dotenv.load(fileName: '.env');\n  await initLocale();"
    )
    main.write_text(txt, encoding='utf-8')
    print('Fixed: main.dart')
else:
    print('main.dart already has initLocale')

# ── 3. Fix login_screen.dart — center toggle above logo, fix layout
login = pathlib.Path('lib/features/auth/presentation/login_screen.dart')
txt = login.read_text(encoding='utf-8')

old_layout = """                // Language toggle
                Row(mainAxisAlignment: MainAxisAlignment.end, children: [
                  _LangBtn(label: 'EN', flag: '🇬🇧', active: lang == 'en',
                      onTap: () => ref.read(localeProvider.notifier).setLanguage('en')),
                  const SizedBox(width: 8),
                  _LangBtn(label: 'SW', flag: '🇰🇪', active: lang == 'sw',
                      onTap: () => ref.read(localeProvider.notifier).setLanguage('sw')),
                ]),
                const SizedBox(height: 16),
                Center(child: Column(children: ["""

new_layout = """                Center(child: Column(children: [
                  // Language toggle — above logo
                  Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                    _LangBtn(label: 'EN', flag: '🇬🇧', active: lang == 'en',
                        onTap: () => ref.read(localeProvider.notifier).setLanguage('en')),
                    const SizedBox(width: 10),
                    _LangBtn(label: 'SW', flag: '🇰🇪', active: lang == 'sw',
                        onTap: () => ref.read(localeProvider.notifier).setLanguage('sw')),
                  ]),
                  const SizedBox(height: 20),"""

# Also fix the closing of the Center(child: Column — need to close it properly
old_close = """                ])),
                const SizedBox(height: 32),
                Container(
                  padding: const EdgeInsets.all(28),"""

new_close = """                ])),
                const SizedBox(height: 32),
                Container(
                  padding: const EdgeInsets.all(28),"""

if old_layout in txt:
    txt = txt.replace(old_layout, new_layout)
    # Now fix the Center column closing — the old code had Center wrapping just
    # the logo section and closing before the card. We need to close it.
    # The new_layout opens Center(child: Column(children: [ but never closes the extra level
    # Actually we just moved the toggle inside the existing Center column, so let's just
    # remove the duplicate closing
    print('Fixed: login toggle layout')
else:
    print('WARNING: old_layout pattern not found — checking alternate...')
    # Try to find and replace just the Row alignment
    txt = txt.replace(
        'Row(mainAxisAlignment: MainAxisAlignment.end, children: [',
        'Row(mainAxisAlignment: MainAxisAlignment.center, children: ['
    )
    print('Fixed: toggle alignment only')

login.write_text(txt, encoding='utf-8')
print('Written: login_screen.dart')