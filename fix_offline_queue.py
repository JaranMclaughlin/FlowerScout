import pathlib, shutil

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
shutil.copy(p, p.with_suffix('.dart.bak'))
text = p.read_text(encoding='utf-8')
original = text

# ── Step 1: Add imports for shared_preferences and dart:convert ──────────────
old_imports_anchor = "import 'package:flutter/material.dart';"
new_imports = """import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';"""
if old_imports_anchor in text and "dart:convert" not in text:
    text = text.replace(old_imports_anchor, new_imports, 1)
    print("Step 1: added imports")
elif "dart:convert" in text:
    print("Step 1: imports already present")
else:
    print("ERROR: import anchor not found"); raise SystemExit(1)

# ── Step 2: Add queue helper methods before _submitReport ────────────────────
queue_helpers = """
  // ── Offline queue helpers ─────────────────────────────────────────────────
  static const _queueKey = 'offline_report_queue';

  Future<void> _saveToQueue(Map<String, dynamic> report, List<Map<String, dynamic>> findings) async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getStringList(_queueKey) ?? [];
    raw.add(jsonEncode({'report': report, 'findings': findings}));
    await prefs.setStringList(_queueKey, raw);
  }

  static Future<List<Map<String, dynamic>>> loadQueue() async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getStringList(_queueKey) ?? [];
    return raw.map((e) => Map<String, dynamic>.from(jsonDecode(e))).toList();
  }

  static Future<void> removeFromQueue(int index) async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getStringList(_queueKey) ?? [];
    if (index < raw.length) {
      raw.removeAt(index);
      await prefs.setStringList(_queueKey, raw);
    }
  }

  static Future<int> queueLength() async {
    final prefs = await SharedPreferences.getInstance();
    return (prefs.getStringList(_queueKey) ?? []).length;
  }

  /// Drains the offline queue - call this on app resume / reconnect
  static Future<void> drainQueue(BuildContext? context) async {
    final queue = await loadQueue();
    if (queue.isEmpty) return;
    int drained = 0;
    for (int i = queue.length - 1; i >= 0; i--) {
      try {
        final entry   = queue[i];
        final report  = Map<String, dynamic>.from(entry['report']);
        final findings = List<Map<String, dynamic>>.from(entry['findings']);
        final reportRow = await Supabase.instance.client
            .from('inspection_reports')
            .insert(report)
            .select('id')
            .single();
        for (final f in findings) {
          await Supabase.instance.client.from('inspection_findings').insert({
            ...f,
            'report_id': reportRow['id'],
          });
        }
        await removeFromQueue(i);
        drained++;
      } catch (_) {
        // Still offline - leave in queue
      }
    }
    if (drained > 0 && context != null && context.mounted) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        backgroundColor: const Color(0xFF1D9E75),
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        content: Row(children: [
          const Icon(Icons.cloud_done_rounded, color: Colors.white),
          const SizedBox(width: 10),
          Text('$drained queued report${drained > 1 ? "s" : ""} synced successfully'),
        ]),
      ));
    }
  }

"""

old_submit_anchor = "  Future<void> _submitReport() async {"
if queue_helpers.strip().split('\n')[1] not in text:
    text = text.replace(old_submit_anchor, queue_helpers + "  Future<void> _submitReport() async {", 1)
    print("Step 2: added queue helper methods")
else:
    print("Step 2: queue helpers already present")

# ── Step 3: Replace the catch block to save to queue on failure ───────────────
old_catch = """    } catch (e) {
      if (mounted) {
        setState(() { _submitting = false; _submitted = false; });
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text('${ref.read(stringsProvider).failedToSubmit}$e'),
          backgroundColor: _C.critical,
        ));
      }
    }"""

new_catch = """    } catch (e) {
      // Network failure - save to offline queue
      try {
        final user = Supabase.instance.client.auth.currentUser;
        await _saveToQueue({
          'scout_id': user?.id,
          'greenhouse_id': selectedGreenhouse!.id,
          'variety_name': selectedVariety,
          'started_at': _sessionStart?.toIso8601String(),
          'submitted_at': DateTime.now().toIso8601String(),
          'duration_seconds': _elapsedSeconds,
          'latitude': _gpsPosition?.latitude,
          'longitude': _gpsPosition?.longitude,
          'status': 'queued',
          if (trailId != null) 'trail_id': trailId,
        }, findings.where((f) => f.issue.trim().isNotEmpty).map((f) => {
          'category': f.category,
          'severity': f.severity,
          'issue': f.issue.trim(),
        }).toList());

        if (mounted) {
          setState(() {
            _scoutingStarted  = false;
            _sessionStart     = null;
            _elapsedSeconds   = 0;
            _gpsPosition      = null;
            _locationDenied   = false;
            selectedFarm      = null;
            selectedGreenhouse = null;
            selectedVariety   = null;
            findings.clear();
            findings.add(FindingData());
            _submitting = false;
            _submitted  = false;
          });
          _headerAnim.reset();
          _headerAnim.forward();
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            backgroundColor: const Color(0xFFBA7517),
            behavior: SnackBarBehavior.floating,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            content: Row(children: [
              const Icon(Icons.cloud_off_rounded, color: Colors.white),
              const SizedBox(width: 10),
              const Expanded(child: Text('No connection — report saved locally and will sync when online',
                  style: TextStyle(color: Colors.white))),
            ]),
          ));
        }
      } catch (queueError) {
        if (mounted) {
          setState(() { _submitting = false; _submitted = false; });
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            content: Text('${ref.read(stringsProvider).failedToSubmit}$e'),
            backgroundColor: _C.critical,
          ));
        }
      }
    }"""

if old_catch in text:
    text = text.replace(old_catch, new_catch, 1)
    print("Step 3: catch block updated to queue on failure")
else:
    print("ERROR: catch block anchor not found"); raise SystemExit(1)

if text != original:
    p.write_text(text, encoding='utf-8')
    print("\nDone. Next: add drainQueue call to main.dart on app resume.")
else:
    print("No changes written.")