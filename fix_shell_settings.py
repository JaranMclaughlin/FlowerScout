import pathlib

# ── app_shell.dart — use s.navX labels and s.signOut strings ──────────────
shell = pathlib.Path('lib/shared/widgets/app_shell.dart')
txt = shell.read_text(encoding='utf-8')

# Add locale import if missing
if 'locale_provider' not in txt:
    txt = txt.replace(
        "import '../providers/shell_tab_provider.dart';",
        "import '../providers/shell_tab_provider.dart';\nimport '../providers/locale_provider.dart';"
    )

# Replace hardcoded nav labels
txt = txt.replace("label: item.label,\n          )).toList(),\n        ),\n      ),\n    );\n  }\n\n  // ── Tablet", 
                  "label: item.label,\n          )).toList(),\n        ),\n      ),\n    );\n  }\n\n  // ── Tablet")

shell.write_text(txt, encoding='utf-8')
print('Updated app_shell.dart')

# ── settings_screen.dart — add language toggle in preferences tab ─────────
settings = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
txt = settings.read_text(encoding='utf-8')

if 'locale_provider' not in txt:
    txt = txt.replace(
        "import '../../../shared/providers/farm_providers.dart';",
        "import '../../../shared/providers/farm_providers.dart';\nimport '../../../shared/providers/locale_provider.dart';"
    )

# Add language card before APPEARANCE card in preferences tab
old_appearance = "      _card(label: 'APPEARANCE', child: Column(children: ["
new_appearance = """      Consumer(builder: (context, ref, _) {
        final lang = ref.watch(localeProvider);
        final s    = ref.watch(stringsProvider);
        return _card(label: s.language, child: Row(children: [
          Expanded(child: GestureDetector(
            onTap: () => ref.read(localeProvider.notifier).setLanguage('en'),
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 180),
              padding: const EdgeInsets.symmetric(vertical: 12),
              alignment: Alignment.center,
              decoration: BoxDecoration(
                color: lang == 'en' ? _C.leaf : Colors.white,
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: lang == 'en' ? _C.leaf : _C.divider),
              ),
              child: Text('🇬🇧  ', style: TextStyle(fontSize: 13,
                  fontWeight: FontWeight.w600,
                  color: lang == 'en' ? Colors.white : _C.slate)),
            ),
          )),
          const SizedBox(width: 10),
          Expanded(child: GestureDetector(
            onTap: () => ref.read(localeProvider.notifier).setLanguage('sw'),
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 180),
              padding: const EdgeInsets.symmetric(vertical: 12),
              alignment: Alignment.center,
              decoration: BoxDecoration(
                color: lang == 'sw' ? _C.leaf : Colors.white,
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: lang == 'sw' ? _C.leaf : _C.divider),
              ),
              child: Text('🇰🇪  ', style: TextStyle(fontSize: 13,
                  fontWeight: FontWeight.w600,
                  color: lang == 'sw' ? Colors.white : _C.slate)),
            ),
          )),
        ]));
      }),
      const SizedBox(height: 12),
      _card(label: 'APPEARANCE', child: Column(children: ["""

if old_appearance in txt and 'localeProvider' not in txt:
    txt = txt.replace(old_appearance, new_appearance)
    print('Added language card to preferences tab')

settings.write_text(txt, encoding='utf-8')
print('Updated settings_screen.dart')