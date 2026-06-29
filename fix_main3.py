import pathlib

p = pathlib.Path('lib/main.dart')
text = p.read_text(encoding='utf-8')

# 1. Replace manual connectivity listener with startListening
text = text.replace(
    "  late final StreamSubscription<List<ConnectivityResult>> _connectivitySub;\n",
    ""
)
text = text.replace(
    "    _connectivitySub = Connectivity().onConnectivityChanged.listen((results) {\n      final hasConnection = results.any((r) => r != ConnectivityResult.none);\n      if (hasConnection && _loggedIn) OfflineSyncService.drain(context);\n    });",
    "    OfflineSyncService.startListening();"
)
text = text.replace(
    "    _connectivitySub.cancel();\n",
    ""
)

# 2. Remove now-unused connectivity_plus import from main.dart
text = text.replace(
    "import 'package:connectivity_plus/connectivity_plus.dart';\n",
    ""
)

p.write_text(text, encoding='utf-8')
print("main.dart: connectivity fixed.")