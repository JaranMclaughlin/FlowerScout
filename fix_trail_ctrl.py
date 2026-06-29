import pathlib

p = pathlib.Path('lib/shared/trail/trail_tracking_controller.dart')
text = p.read_text(encoding='utf-8')

old_import = "import '../providers/farm_providers.dart';"
new_import = """import '../providers/farm_providers.dart';
import '../../../core/session/user_session.dart';"""
text = text.replace(old_import, new_import, 1)

old_start = """    final trailId = await repo.startTrail(
      scoutId: scoutId,
      farmId: farmId,
      greenhouseId: greenhouseId,
    );"""
new_start = """    final trailId = await repo.startTrail(
      scoutId: scoutId,
      farmId: farmId,
      greenhouseId: greenhouseId,
      scoutName: UserSession.currentUser.isNotEmpty ? UserSession.currentUser : null,
    );"""

if old_start not in text:
    import sys; sys.exit("Anchor not found.")
text = text.replace(old_start, new_start, 1)
p.write_text(text, encoding='utf-8')
print("trail_tracking_controller.dart fixed.")