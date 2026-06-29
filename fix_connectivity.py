import pathlib, sys

# ── Fix 5: connectivity_plus drain on reconnect ───────────────────────
p = pathlib.Path('lib/main.dart')
text = p.read_text(encoding='utf-8')

# Add connectivity_plus import
old_import = "import 'core/offline/offline_sync_service.dart';"
new_import = """import 'core/offline/offline_sync_service.dart';
import 'package:connectivity_plus/connectivity_plus.dart';"""
if old_import not in text:
    sys.exit("Import anchor not found.")
text = text.replace(old_import, new_import, 1)

# Add connectivity subscription field after _loggedIn declaration
old_field = "  bool _loggedIn = false;"
new_field = """  bool _loggedIn = false;
  late final StreamSubscription<List<ConnectivityResult>> _connectivitySub;"""
if old_field not in text:
    sys.exit("Field anchor not found.")
text = text.replace(old_field, new_field, 1)

# Wire subscription in initState after addObserver
old_observer = "    WidgetsBinding.instance.addObserver(this);"
new_observer = """    WidgetsBinding.instance.addObserver(this);
    _connectivitySub = Connectivity().onConnectivityChanged.listen((results) {
      final hasConnection = results.any((r) => r != ConnectivityResult.none);
      if (hasConnection && _loggedIn) {
        OfflineSyncService.drain(context);
      }
    });"""
if old_observer not in text:
    sys.exit("Observer anchor not found.")
text = text.replace(old_observer, new_observer, 1)

# Cancel subscription in dispose
old_dispose = """    WidgetsBinding.instance.removeObserver(this);
    super.dispose();"""
new_dispose = """    WidgetsBinding.instance.removeObserver(this);
    _connectivitySub.cancel();
    super.dispose();"""
if old_dispose not in text:
    sys.exit("Dispose anchor not found.")
text = text.replace(old_dispose, new_dispose, 1)

# Add dart:async import if missing
if "import 'dart:async';" not in text:
    text = "import 'dart:async';\n" + text

p.write_text(text, encoding='utf-8')
print("main.dart: connectivity drain wired.")

# ── Fix 6: farm cache TTL 5min → 30min ───────────────────────────────
p2 = pathlib.Path('lib/shared/providers/farm_repository.dart')
text2 = p2.read_text(encoding='utf-8')
text2 = text2.replace(
    "static const maxAgeMs = 5 * 60 * 1000; // 5 minutes",
    "static const maxAgeMs = 30 * 60 * 1000; // 30 minutes"
)
p2.write_text(text2, encoding='utf-8')
print("farm_repository.dart: cache TTL extended to 30 minutes.")