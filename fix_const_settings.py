import pathlib

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
txt = p.read_text(encoding='utf-8')

txt = txt.replace(
    "        const Padding(\n          padding: EdgeInsets.fromLTRB(20, 28, 20, 16),\n          child: Text(s.settingsTitle, style: TextStyle(fontFamily: 'Georgia',\n              fontSize: 22, fontWeight: FontWeight.w700, color: _C.ink)),\n        ),",
    "        Padding(\n          padding: const EdgeInsets.fromLTRB(20, 28, 20, 16),\n          child: Text(s.settingsTitle, style: const TextStyle(fontFamily: 'Georgia',\n              fontSize: 22, fontWeight: FontWeight.w700, color: _C.ink)),\n        ),"
)

p.write_text(txt, encoding='utf-8')
print('done')