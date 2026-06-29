import pathlib, sys

p = pathlib.Path('lib/main.dart')
text = p.read_text(encoding='utf-8')

# 1. Remove the manual connectivity listener we added — OfflineSyncService.startListening handles it
old_listener = """    _connectivitySub = Connectivity().onConnectivityChanged.listen((results) {
      final hasConnection = results.any((r) => r != ConnectivityResult.none);
      if (hasConnection && _loggedIn) OfflineSyncService.drain(context);
    });"""
new_listener = """    // OfflineSyncService.startListening handles connectivity-based drain internally"""
if old_listener not in text:
    sys.exit("Listener anchor not found.")
text = text.replace(old_listener, new_listener, 1)

# 2. Remove the StreamSubscription field — no longer needed
text = text.replace(
    "  late final StreamSubscription<List<ConnectivityResult>> _connectivitySub;\n",
    ""
)

# 3. Remove the cancel call in dispose
text = text.replace(
    "    _connectivitySub.cancel();\n",
    ""
)

# 4. Remove connectivity_plus import from main.dart — it lives in offline_sync_service now
text = text.replace(
    "import 'package:connectivity_plus/connectivity_plus.dart';\n",
    ""
)

# 5. Start the listener after sign-in
old_signin = "        // Drain any queued reports from when the scout was offline\n        OfflineSyncService.drain(context);"
new_signin = """        // Flush any queued reports and start connectivity listener
        OfflineSyncService.flush();
        OfflineSyncService.startListening();"""
if old_signin not in text:
    sys.exit("Sign-in drain anchor not found.")
text = text.replace(old_signin, new_signin, 1)

# 6. Start listener on cold-start resume too
old_resume = "    if (state == AppLifecycleState.resumed && _loggedIn) {\n      OfflineSyncService.drain(context);\n    }"
new_resume = "    if (state == AppLifecycleState.resumed && _loggedIn) {\n      OfflineSyncService.flush();\n    }"
if old_resume not in text:
    sys.exit("Resume anchor not found.")
text = text.replace(old_resume, new_resume, 1)

p.write_text(text, encoding='utf-8')
print("main.dart: uses flush() + startListening() correctly.")