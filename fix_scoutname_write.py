import pathlib, sys

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
text = p.read_text(encoding='utf-8')

# 1. Online submit path
old1 = "            'scout_id': user?.id,\n            'greenhouse_id': selectedGreenhouse!.id,"
new1 = "            'scout_id': user?.id,\n            'scout_name': UserSession.currentUser,\n            'greenhouse_id': selectedGreenhouse!.id,"
if old1 not in text:
    sys.exit("Anchor 1 not found.")
text = text.replace(old1, new1, 1)

# 2. Offline queue path
old2 = "          'scout_id': user?.id,\n          'greenhouse_id': selectedGreenhouse!.id,"
new2 = "          'scout_id': user?.id,\n          'scout_name': UserSession.currentUser,\n          'greenhouse_id': selectedGreenhouse!.id,"
if old2 not in text:
    sys.exit("Anchor 2 not found.")
text = text.replace(old2, new2, 1)

# 3. Ensure UserSession is imported
if "import '../../../core/session/user_session.dart';" not in text:
    text = text.replace(
        "import '../../../core/offline/offline_sync_service.dart';",
        "import '../../../core/offline/offline_sync_service.dart';\nimport '../../../core/session/user_session.dart';"
    )

p.write_text(text, encoding='utf-8')
print("scouting_screen.dart: scout_name now written on both online and offline submit paths.")