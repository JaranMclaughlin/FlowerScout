import pathlib, re

p = pathlib.Path('lib/core/offline/offline_sync_service.dart')
text = p.read_text(encoding='utf-8')

# 1. Remove unused locale_provider import
text = text.replace(
    "import '../../../shared/providers/locale_provider.dart';\n",
    ""
)

# 2. Fix showSyncSnackbar — s is declared but AppStrings.of(lang) used inline instead
# Replace the method to use s correctly
text = re.sub(
    r"  static void showSyncSnackbar\(BuildContext context, int synced, int failed, String lang\) \{.*?\n  \}",
    """  static void showSyncSnackbar(BuildContext context, int synced, int failed, String lang) {
    final s = AppStrings.of(lang);
    if (synced > 0 && context.mounted) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        backgroundColor: const Color(0xFF1D9E75),
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        content: Row(children: [
          const Icon(Icons.cloud_done_rounded, color: Colors.white),
          const SizedBox(width: 10),
          Text('$synced ${synced == 1 ? s.offlineSyncedSingle : s.offlineSyncedPlural}',
              style: const TextStyle(color: Colors.white)),
        ]),
      ));
    }
    if (failed > 0 && context.mounted) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        backgroundColor: const Color(0xFFBA7517),
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        content: Row(children: [
          const Icon(Icons.warning_amber_rounded, color: Colors.white),
          const SizedBox(width: 10),
          Text('$failed ${s.offlineDeadLetter}',
              style: const TextStyle(color: Colors.white)),
        ]),
      ));
    }
  }""",
    text,
    flags=re.DOTALL
)

p.write_text(text, encoding='utf-8')
print("Done.")