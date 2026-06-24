import pathlib, re

# ── 1. Fix trail_tracking_controller.dart imports ──────────────────────
ctrl = pathlib.Path('lib/shared/trail/trail_tracking_controller.dart')
txt = ctrl.read_text(encoding='utf-8')
txt = txt.replace("import '../data/trail_repository.dart';",
                  "import 'data/trail_repository.dart';")
txt = txt.replace("import 'trail_providers.dart';",
                  "import 'providers/trail_providers.dart';")
txt = txt.replace("import '../../providers/farm_providers.dart';",
                  "import '../providers/farm_providers.dart';")
ctrl.write_text(txt, encoding='utf-8')
print('Fixed: trail_tracking_controller.dart')

# ── 2. Fix maps_screen.dart — add missing imports ───────────────────────
maps = pathlib.Path('lib/features/maps/presentation/maps_screen.dart')
txt = maps.read_text(encoding='utf-8')
needed = [
    "import '../../../shared/trail/models/scout_trail.dart';",
    "import '../../../shared/trail/providers/trail_providers.dart';",
    "import '../../../shared/trail/data/trail_repository.dart';",
    "import '../../../core/session/user_session.dart';",
]
# Insert after the last existing import line
last_import = max(i for i, l in enumerate(txt.splitlines()) if l.startswith('import '))
lines = txt.splitlines()
for imp in reversed(needed):
    if imp not in txt:
        lines.insert(last_import + 1, imp)
maps.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('Fixed: maps_screen.dart imports')

# ── 3. Rename backup dart files so analyzer ignores them ────────────────
import os
backups = [
    'lib/features/auth/presentation/login_screen.roles.backup.dart',
    'lib/features/auth/presentation/login_screen.roles.backup2.dart',
    'lib/features/auth/presentation/login_screen.backup.dart',
    'lib/features/maps/presentation/maps_screen.backup.dart',
]
for b in backups:
    p = pathlib.Path(b)
    if p.exists():
        p.rename(str(p).replace('.dart', '.dart.bak'))
        print(f'Renamed: {b}')

print('All done.')