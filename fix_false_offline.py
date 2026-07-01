import pathlib

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
text = p.read_text(encoding='utf-8')

old = """    } catch (e) {
      // Network failure - save to offline queue
      try {"""

new = """    } catch (e) {
      // Only fall back to the offline queue if there is genuinely no network.
      // Any other failure (RLS, validation, storage, etc.) should surface
      // as a real error so it can be fixed, not be hidden behind a false
      // "offline" message.
      final connectivity = await Connectivity().checkConnectivity();
      final hasNetwork = connectivity.any((r) =>
          r == ConnectivityResult.mobile ||
          r == ConnectivityResult.wifi   ||
          r == ConnectivityResult.ethernet);

      if (!hasNetwork) {
      try {"""

if old not in text:
    raise SystemExit("Anchor 1 not found — aborting, no changes made.")

text = text.replace(old, new, 1)

# Close the new if-block right before the existing queueError catch,
# and add an else branch that surfaces the real error instead of
# silently queueing it.
old2 = """      } catch (queueError) {"""

new2 = """      } else {
        // Genuine error while online — show it instead of masking as offline.
        if (mounted) {
          setState(() { _submitting = false; _submitted = false; });
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            backgroundColor: AppColors.critical,
            behavior: SnackBarBehavior.floating,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            content: Text('Submit failed: \\$e',
                style: const TextStyle(color: Colors.white)),
          ));
        }
      }
      } catch (queueError) {"""

if old2 not in text:
    raise SystemExit("Anchor 2 not found — aborting, no changes made.")

text = text.replace(old2, new2, 1)

# Ensure connectivity_plus is imported (used elsewhere already per offline_sync_service)
if "import 'package:connectivity_plus/connectivity_plus.dart';" not in text:
    text = text.replace(
        "import '../../../core/offline/offline_sync_service.dart';",
        "import '../../../core/offline/offline_sync_service.dart';\nimport 'package:connectivity_plus/connectivity_plus.dart';"
    )

p.write_text(text, encoding='utf-8')
print("scouting_screen.dart: offline detection now checks real connectivity before queuing.")