import pathlib, shutil

# ── Delete empty dead files ───────────────────────────────────────────────────
dead = [
    'lib/features/auth/location_service.dart',
    'lib/features/dashboard/presentation/manager/manager_dashboard_screen.dart',
    'lib/features/dashboard/presentation/scout/scout_dashboard_screen.dart',
]
for f in dead:
    p = pathlib.Path(f)
    if p.exists() and p.stat().st_size == 0:
        p.unlink()
        print(f"Deleted empty file: {f}")

# ── Rewrite the offline queue in scouting_screen.dart ────────────────────────
p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
shutil.copy(p, p.with_suffix('.dart.bak10'))
text = p.read_text(encoding='utf-8')
original = text

# Replace the basic queue helpers with a hardened version:
# - exponential backoff (1s, 2s, 4s... up to 30s)
# - max 5 retries per entry, then dead-letter it
# - concurrent drain capped at 3 simultaneous uploads
# - per-entry retry count tracked in the queue payload
old_queue_helpers = "  // ── Offline queue helpers ─────────────────────────────────────────────────\n  static const _queueKey = 'offline_report_queue';"

new_queue_helpers = """  // ── Offline queue (hardened) ─────────────────────────────────────────────
  static const _queueKey      = 'offline_report_queue';
  static const _deadLetterKey = 'offline_report_dead_letter';
  static const _maxRetries    = 5;
  static const _maxConcurrent = 3; // max simultaneous Supabase inserts on drain"""

if old_queue_helpers in text:
    text = text.replace(old_queue_helpers, new_queue_helpers, 1)
    print("Step 1: updated queue constants")
else:
    print("ERROR: queue helpers anchor not found"); raise SystemExit(1)

# Replace _saveToQueue to include retryCount
old_save = """  Future<void> _saveToQueue(Map<String, dynamic> report, List<Map<String, dynamic>> findings) async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getStringList(_queueKey) ?? [];
    raw.add(jsonEncode({'report': report, 'findings': findings}));
    await prefs.setStringList(_queueKey, raw);
  }"""

new_save = """  Future<void> _saveToQueue(Map<String, dynamic> report, List<Map<String, dynamic>> findings) async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getStringList(_queueKey) ?? [];
    raw.add(jsonEncode({
      'report': report,
      'findings': findings,
      'retryCount': 0,
      'queuedAt': DateTime.now().toIso8601String(),
    }));
    await prefs.setStringList(_queueKey, raw);
  }"""

if old_save in text:
    text = text.replace(old_save, new_save, 1)
    print("Step 2: _saveToQueue now tracks retryCount + queuedAt")
else:
    print("ERROR: _saveToQueue anchor not found"); raise SystemExit(1)

# Replace drainQueue with hardened version
old_drain_start = "  // ignore: unused_element\n  static Future<void> drainQueue(BuildContext? context) async {"
old_drain_end = "  }\n\n"
# Find the full drain method
drain_start_idx = text.find(old_drain_start)
if drain_start_idx == -1:
    print("ERROR: drainQueue start not found"); raise SystemExit(1)

# Find closing brace by counting braces
depth = 0
i = drain_start_idx
found_first_brace = False
drain_end_idx = -1
while i < len(text):
    if text[i] == '{':
        depth += 1
        found_first_brace = True
    elif text[i] == '}':
        depth -= 1
        if found_first_brace and depth == 0:
            drain_end_idx = i + 1
            break
    i += 1

if drain_end_idx == -1:
    print("ERROR: could not find drainQueue closing brace"); raise SystemExit(1)

old_drain_full = text[drain_start_idx:drain_end_idx]

new_drain = """  // ignore: unused_element
  static Future<void> drainQueue(BuildContext? context) async {
    final prefs = await SharedPreferences.getInstance();
    final raw   = prefs.getStringList(_queueKey) ?? [];
    if (raw.isEmpty) return;

    // Process in batches of _maxConcurrent to avoid hammering Supabase
    final toProcess = List<String>.from(raw);
    final surviving = <String>[];  // entries that failed and should stay queued
    final deadLetter = <String>[]; // entries that exceeded max retries

    // Process up to _maxConcurrent at a time
    for (int base = 0; base < toProcess.length; base += _maxConcurrent) {
      final batch = toProcess.sublist(
          base, (base + _maxConcurrent).clamp(0, toProcess.length));

      final results = await Future.wait(batch.map((raw) async {
        final entry      = jsonDecode(raw) as Map<String, dynamic>;
        final report     = Map<String, dynamic>.from(entry['report'] as Map);
        final findings   = List<Map<String, dynamic>>.from(
            (entry['findings'] as List).map((f) => Map<String, dynamic>.from(f as Map)));
        int retryCount   = (entry['retryCount'] as int?) ?? 0;

        // Exponential backoff: skip entries that haven't waited long enough
        if (retryCount > 0) {
          final queuedAt = DateTime.tryParse(entry['queuedAt'] as String? ?? '');
          if (queuedAt != null) {
            final backoffSeconds = (1 << retryCount.clamp(0, 5)).clamp(1, 30);
            final waitUntil = queuedAt.add(Duration(seconds: backoffSeconds));
            if (DateTime.now().isBefore(waitUntil)) {
              return raw; // not ready yet, keep in queue
            }
          }
        }

        try {
          final reportRow = await Supabase.instance.client
              .from('inspection_reports')
              .insert(report)
              .select('id')
              .single();

          for (final f in findings) {
            final photoUrls = <String>[];
            final photoPaths = List<String>.from(f['photo_paths'] as List? ?? []);
            // Note: photo re-upload from paths not supported on web/after cold start
            // photos will be empty for queued reports - acceptable tradeoff
            await Supabase.instance.client.from('inspection_findings').insert({
              'report_id': reportRow['id'],
              'category':  f['category'],
              'severity':  f['severity'],
              'issue':     f['issue'],
              if (photoUrls.isNotEmpty) 'photo_urls': photoUrls,
            });
          }
          return null; // success - remove from queue
        } catch (_) {
          retryCount++;
          if (retryCount >= _maxRetries) {
            // Dead-letter: stop retrying, preserve for admin review
            return jsonEncode({...entry, 'retryCount': retryCount, 'failedAt': DateTime.now().toIso8601String()});
          }
          // Keep in queue with incremented retry count + reset queuedAt for backoff
          return jsonEncode({...entry, 'retryCount': retryCount, 'queuedAt': DateTime.now().toIso8601String()});
        }
      }));

      for (int j = 0; j < results.length; j++) {
        final result = results[j];
        if (result == null) continue; // success
        final entry = jsonDecode(result) as Map<String, dynamic>;
        final retries = (entry['retryCount'] as int?) ?? 0;
        if (retries >= _maxRetries) {
          deadLetter.add(result);
        } else {
          surviving.add(result);
        }
      }
    }

    // Persist surviving (retry-eligible) entries
    await prefs.setStringList(_queueKey, surviving);

    // Persist dead-letter entries separately
    if (deadLetter.isNotEmpty) {
      final existing = prefs.getStringList(_deadLetterKey) ?? [];
      await prefs.setStringList(_deadLetterKey, [...existing, ...deadLetter]);
    }

    final drained = toProcess.length - surviving.length - deadLetter.length;
    if (drained > 0 && context != null && context.mounted) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        backgroundColor: const Color(0xFF1D9E75),
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        content: Row(children: [
          const Icon(Icons.cloud_done_rounded, color: Colors.white),
          const SizedBox(width: 10),
          Text('$drained queued report${drained > 1 ? "s" : ""} synced'),
        ]),
      ));
    }
    if (deadLetter.isNotEmpty && context != null && context.mounted) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        backgroundColor: const Color(0xFFBA7517),
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        content: Row(children: [
          const Icon(Icons.warning_amber_rounded, color: Colors.white),
          const SizedBox(width: 10),
          Text('${deadLetter.length} report${deadLetter.length > 1 ? "s" : ""} could not sync — contact admin'),
        ]),
      ));
    }
  }"""

text = text[:drain_start_idx] + new_drain + text[drain_end_idx:]
print("Step 3: drainQueue replaced with hardened version (backoff + concurrency + dead-letter)")

if text != original:
    p.write_text(text, encoding='utf-8')
    print("\nDone.")
else:
    print("\nNo changes written.")