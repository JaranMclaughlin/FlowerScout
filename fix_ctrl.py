import pathlib

# Fix 1: Add missing model import to trail_tracking_controller.dart
ctrl = pathlib.Path('lib/shared/trail/trail_tracking_controller.dart')
txt = ctrl.read_text(encoding='utf-8')
if "import 'models/scout_trail.dart';" not in txt:
    txt = txt.replace(
        "import 'data/trail_repository.dart';",
        "import 'models/scout_trail.dart';\nimport 'data/trail_repository.dart';"
    )
    ctrl.write_text(txt, encoding='utf-8')
    print('Fixed: added scout_trail import to controller')
else:
    print('Already present')