import pathlib, sys

p = pathlib.Path('lib/main.dart')
text = p.read_text(encoding='utf-8')

# Add missing imports after supabase import
old_import = "import 'package:supabase_flutter/supabase_flutter.dart';"
new_import = """import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'core/offline/offline_sync_service.dart';"""
if old_import not in text:
    sys.exit("Import anchor not found.")
text = text.replace(old_import, new_import, 1)

# Add connectivity subscription field
old_field = "  bool _loggedIn = false;"
new_field = """  bool _loggedIn = false;
  late final StreamSubscription<List<ConnectivityResult>> _connectivitySub;"""
if old_field not in text:
    sys.exit("Field anchor not found.")
text = text.replace(old_field, new_field, 1)

# Wire in initState
old_observer = "    WidgetsBinding.instance.addObserver(this);"
new_observer = """    WidgetsBinding.instance.addObserver(this);
    _connectivitySub = Connectivity().onConnectivityChanged.listen((results) {
      final hasConnection = results.any((r) => r != ConnectivityResult.none);
      if (hasConnection && _loggedIn) OfflineSyncService.drain(context);
    });"""
if old_observer not in text:
    sys.exit("Observer anchor not found.")
text = text.replace(old_observer, new_observer, 1)

# Cancel in dispose
old_dispose = "    WidgetsBinding.instance.removeObserver(this);\n    super.dispose();"
new_dispose = "    WidgetsBinding.instance.removeObserver(this);\n    _connectivitySub.cancel();\n    super.dispose();"
if old_dispose not in text:
    sys.exit("Dispose anchor not found.")
text = text.replace(old_dispose, new_dispose, 1)

p.write_text(text, encoding='utf-8')
print("main.dart: connectivity drain wired.")