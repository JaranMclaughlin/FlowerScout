import pathlib

p = pathlib.Path('lib/features/scouting/presentation/topbar_widgets.dart')
txt = p.read_text(encoding='utf-8', errors='replace')

txt = txt.replace(
    "          const Text('All caught up!',\n              style: TextStyle(\n                  fontFamily: 'Georgia',\n                  fontSize: 18,\n                  fontWeight: FontWeight.w600,\n                  color: _C.ink)),\n          const SizedBox(height: 6),\n          const Text(s.noNewNotifications,",
    "          Text(s.allCaughtUp,\n              style: const TextStyle(\n                  fontFamily: 'Georgia',\n                  fontSize: 18,\n                  fontWeight: FontWeight.w600,\n                  color: _C.ink)),\n          const SizedBox(height: 6),\n          Text(s.noNewNotifications,"
)

p.write_text(txt, encoding='utf-8')
print('done')