import pathlib
p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
t = p.read_text(encoding='utf-8')
old = "      const Padding(\n        padding: EdgeInsets.fromLTRB(20, 20, 20, 12),\nchild: Text(s.settingsTitle, style: const TextStyle(fontFamily: 'Georgia',\n            fontSize: 22, fontWeight: FontWeight.w700, color: _C.ink)),\n      ),"
new = "      Padding(\n        padding: const EdgeInsets.fromLTRB(20, 20, 20, 12),\n        child: Text(s.settingsTitle, style: const TextStyle(fontFamily: 'Georgia',\n            fontSize: 22, fontWeight: FontWeight.w700, color: _C.ink)),\n      ),"
if old not in t: raise SystemExit('anchor not found')
t = t.replace(old, new, 1)
p.write_text(t, encoding='utf-8')
print('Fixed.')