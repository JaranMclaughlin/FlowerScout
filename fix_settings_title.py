import pathlib

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
txt = p.read_text(encoding='utf-8')

txt = txt.replace(
    "          child: Text('Settings', style: TextStyle(fontFamily: 'Georgia',\n              fontSize: 22, fontWeight: FontWeight.w700, color: _C.ink)),",
    "          child: Text(s.settingsTitle, style: TextStyle(fontFamily: 'Georgia',\n              fontSize: 22, fontWeight: FontWeight.w700, color: _C.ink)),"
)
txt = txt.replace(
    "          'Manage your farms and growing locations.',",
    "          s.farmGhConfigDesc,"
)

p.write_text(txt, encoding='utf-8')
print('done')