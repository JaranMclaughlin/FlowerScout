import pathlib, re

# ── 1. Use chartLabelsWeekShort in analytics_screen.dart ─────────────
p = pathlib.Path('lib/features/analytics/presentation/analytics_screen.dart')
text = p.read_text(encoding='utf-8')
text = text.replace(
    "final labels = d.chartLabels;",
    "final labels = d.chartLabels.length == 7 ? AppStrings.of(ref.watch(localeProvider)).chartLabelsWeekShort : d.chartLabels;"
)
p.write_text(text, encoding='utf-8')
print("analytics_screen.dart: short week labels wired.")

# ── 2. Use chartLabelsWeekShort in reports_screen.dart ───────────────
p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')
# reports uses _ReportStats which has chartLabels — fix at the stats build level
# in analytics_data.dart _buildTrend, replace chartLabelsWeek with short version
p.write_text(text, encoding='utf-8')
print("reports_screen.dart: done.")

# ── 3. Fix analytics_data.dart to use short labels ────────────────────
p = pathlib.Path('lib/shared/providers/analytics_data.dart')
text = p.read_text(encoding='utf-8')
text = text.replace(
    "    labels = AppStrings.of(lang).chartLabelsWeek; n = 7;",
    "    labels = AppStrings.of(lang).chartLabelsWeekShort; n = 7;"
)
p.write_text(text, encoding='utf-8')
print("analytics_data.dart: short week labels in trend builder.")

# ── 4. Fix offline snackbar strings in offline_sync_service.dart ──────
p = pathlib.Path('lib/core/offline/offline_sync_service.dart')
text = p.read_text(encoding='utf-8')

# Add flutter import for BuildContext snackbar support
if "import 'package:flutter/material.dart';" not in text:
    text = text.replace(
        "import 'dart:convert';",
        "import 'dart:convert';\nimport 'package:flutter/material.dart';\nimport '../../../shared/l10n/app_strings.dart';\nimport '../../../shared/providers/locale_provider.dart';"
    )

# Replace hardcoded snackbar in flush with localised version
# The flush() method currently returns int — wire snackbar at call sites instead
# For now just make startListening accept a locale-aware callback
text = text.replace(
    "  static void startListening({void Function(int count)? onFlushed}) {\n    Connectivity().onConnectivityChanged.listen((results) async {\n      final online = results.any((r) =>\n          r == ConnectivityResult.mobile ||\n          r == ConnectivityResult.wifi   ||\n          r == ConnectivityResult.ethernet);\n      if (!online) return;\n      final count = await flush();\n      if (count > 0) onFlushed?.call(count);\n    });\n  }",
    "  static void startListening({void Function(int count)? onFlushed}) {\n    Connectivity().onConnectivityChanged.listen((results) async {\n      final online = results.any((r) =>\n          r == ConnectivityResult.mobile ||\n          r == ConnectivityResult.wifi   ||\n          r == ConnectivityResult.ethernet);\n      if (!online) return;\n      final count = await flush();\n      if (count > 0) onFlushed?.call(count);\n    });\n  }\n\n  /// Show a localised snackbar after flush.\n  static void showSyncSnackbar(BuildContext context, int synced, int failed, String lang) {\n    final s = AppStrings.of(lang);\n    if (synced > 0 && context.mounted) {\n      ScaffoldMessenger.of(context).showSnackBar(SnackBar(\n        backgroundColor: const Color(0xFF1D9E75),\n        behavior: SnackBarBehavior.floating,\n        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),\n        content: Row(children: [\n          const Icon(Icons.cloud_done_rounded, color: Colors.white),\n          const SizedBox(width: 10),\n          Text('\$synced \${synced == 1 ? s.offlineSyncedSingle : s.offlineSyncedPlural}',\n              style: const TextStyle(color: Colors.white)),\n        ]),\n      ));\n    }\n    if (failed > 0 && context.mounted) {\n      ScaffoldMessenger.of(context).showSnackBar(SnackBar(\n        backgroundColor: const Color(0xFFBA7517),\n        behavior: SnackBarBehavior.floating,\n        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),\n        content: Row(children: [\n          const Icon(Icons.warning_amber_rounded, color: Colors.white),\n          const SizedBox(width: 10),\n          Text('\$failed \${s.offlineDeadLetter}',\n              style: const TextStyle(color: Colors.white)),\n        ]),\n      ));\n    }\n  }"
)

p.write_text(text, encoding='utf-8')
print("offline_sync_service.dart: localised snackbar helper added.")

# ── 5. Fix scouting_screen hardcoded offline strings ─────────────────
p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
text = p.read_text(encoding='utf-8')
text = text.replace(
    "              const Expanded(child: Text('No connection \u2014 report saved locally and will sync when online',\n                  style: TextStyle(color: Colors.white))),",
    "              Expanded(child: Text('${ref.read(stringsProvider).offlineNoConn} \u2014 ${ref.read(stringsProvider).offlineQueuedSingle}',\n                  style: const TextStyle(color: Colors.white))),"
)
text = text.replace(
    "              '$_queueCount report\${_queueCount > 1 ? \"s\" : \"\"} queued \u2014 will sync when online'",
    "'$_queueCount \${_queueCount > 1 ? ref.read(stringsProvider).offlineQueuedPlural : ref.read(stringsProvider).offlineQueuedSingle}'"
)
p.write_text(text, encoding='utf-8')
print("scouting_screen.dart: offline strings localised.")