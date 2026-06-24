import pathlib

p = pathlib.Path('lib/features/auth/presentation/login_screen.dart')
txt = p.read_text(encoding='utf-8')

# Replace the corrupted LangBtn section with clean ASCII
import re

old = re.search(
    r'// Language toggle.*?const SizedBox\(height: 20\),',
    txt, re.DOTALL
)
if old:
    print('Found corrupted section, replacing...')
    txt = txt[:old.start()] + """// Language toggle — above logo
                  Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                    _LangBtn(label: 'EN', flag: '\u{1F1EC}\u{1F1E7}', active: lang == 'en',
                        onTap: () => ref.read(localeProvider.notifier).setLanguage('en')),
                    const SizedBox(width: 10),
                    _LangBtn(label: 'SW', flag: '\u{1F1F0}\u{1F1EA}', active: lang == 'sw',
                        onTap: () => ref.read(localeProvider.notifier).setLanguage('sw')),
                  ]),
                  const SizedBox(height: 20),""" + txt[old.end():]
else:
    print('Pattern not found, rewriting entire file')

p.write_text(txt, encoding='utf-8')