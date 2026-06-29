import pathlib, sys

p = pathlib.Path('lib/main.dart')
text = p.read_text(encoding='utf-8')
original = text

# Add import for OfflineSyncService after the last import line
old_import = "import 'shared/providers/locale_provider.dart';"
new_import = """import 'shared/providers/locale_provider.dart';
import 'core/offline/offline_sync_service.dart';"""
if old_import not in text:
    sys.exit("Import anchor not found.")
text = text.replace(old_import, new_import, 1)

# Wire drain after sign-in event (there is a comment placeholder)
old_signin = "        // Drain any queued reports from when the scout was offline\n\n"
new_signin = """        // Drain any queued reports from when the scout was offline
        OfflineSyncService.drain(context);

"""
if old_signin not in text:
    sys.exit("Sign-in drain anchor not found.")
text = text.replace(old_signin, new_signin, 1)

# Wire drain on app resume
old_resume = """  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed && _loggedIn) {

    }
  }"""
new_resume = """  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed && _loggedIn) {
      OfflineSyncService.drain(context);
    }
  }"""
if old_resume not in text:
    sys.exit("App resume anchor not found.")
text = text.replace(old_resume, new_resume, 1)

p.write_text(text, encoding='utf-8')
print("main.dart patched: drain on sign-in + app resume.")