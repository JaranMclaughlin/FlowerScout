import pathlib, sys

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
text = p.read_text(encoding='utf-8')
original = text

# Add import
old_import = "import '../../../shared/trail/trail_tracking_controller.dart';"
new_import = """import '../../../shared/trail/trail_tracking_controller.dart';
import '../../../core/offline/offline_sync_service.dart';"""
if old_import not in text:
    sys.exit("Import anchor not found.")
text = text.replace(old_import, new_import, 1)

# Replace _saveToQueue call with OfflineSyncService.saveToQueue
old_save = "        await _saveToQueue({"
new_save = "        await OfflineSyncService.saveToQueue({"
text = text.replace(old_save, new_save, 1)

# Replace _refreshQueueCount body to use OfflineSyncService
old_refresh = """  Future<void> _refreshQueueCount() async {
    final count = await _ScoutingScreenState.queueLength();
    if (mounted) setState(() => _queueCount = count);
  }"""
new_refresh = """  Future<void> _refreshQueueCount() async {
    final count = await OfflineSyncService.queueLength();
    if (mounted) setState(() => _queueCount = count);
  }"""
if old_refresh not in text:
    sys.exit("refreshQueueCount anchor not found.")
text = text.replace(old_refresh, new_refresh, 1)

p.write_text(text, encoding='utf-8')
print("scouting_screen.dart patched.")