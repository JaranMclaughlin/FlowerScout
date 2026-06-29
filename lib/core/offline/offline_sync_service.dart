import 'dart:convert';
import 'package:flutter/material.dart';
import '../../../shared/l10n/app_strings.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:connectivity_plus/connectivity_plus.dart';

class OfflineSyncService {
  static const _key = 'pending_reports';

  // -- Aliases (used by scouting_screen) --------------------------------------
  static Future<int> queueLength() => pendingCount();
  static Future<void> saveToQueue(Map<String, dynamic> report, Iterable<Map<String, dynamic>> findings) => enqueue({...report, 'findings': findings.toList()});

  // -- Enqueue ----------------------------------------------------------------
  static Future<void> enqueue(Map<String, dynamic> report) async {
    final prefs = await SharedPreferences.getInstance();
    final list  = _load(prefs);
    list.add(report);
    await prefs.setString(_key, jsonEncode(list));
  }

  // -- Pending count ----------------------------------------------------------
  static Future<int> pendingCount() async {
    final prefs = await SharedPreferences.getInstance();
    return _load(prefs).length;
  }

  // -- Flush on reconnect -----------------------------------------------------
  static Future<int> flush() async {
    final prefs   = await SharedPreferences.getInstance();
    final pending = _load(prefs);
    if (pending.isEmpty) return 0;
    final client  = Supabase.instance.client;
    final failed  = <Map<String, dynamic>>[];
    int uploaded  = 0;
    for (final report in pending) {
      try {
        final findings = List<Map<String, dynamic>>.from(report['findings'] ?? []);
        final reportPayload = Map<String, dynamic>.from(report)..remove('findings');
        final row = await client
            .from('inspection_reports')
            .insert(reportPayload)
            .select('id')
            .single();
        for (final f in findings) {
          await client.from('inspection_findings').insert({
            ...f,
            'report_id': row['id'],
          });
        }
        uploaded++;
      } catch (_) {
        failed.add(report);
      }
    }
    await prefs.setString(_key, jsonEncode(failed));
    return uploaded;
  }

  // -- Auto-flush when connectivity returns -----------------------------------
  static void startListening({void Function(int count)? onFlushed}) {
    Connectivity().onConnectivityChanged.listen((results) async {
      final online = results.any((r) =>
          r == ConnectivityResult.mobile ||
          r == ConnectivityResult.wifi   ||
          r == ConnectivityResult.ethernet);
      if (!online) return;
      final count = await flush();
      if (count > 0) onFlushed?.call(count);
    });
  }

  /// Show a localised snackbar after flush.
  static void showSyncSnackbar(BuildContext context, int synced, int failed, String lang) {
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
  }

  // -- Check connectivity -----------------------------------------------------
  static Future<bool> isOnline() async {
    final r = await Connectivity().checkConnectivity();
    return r.any((c) =>
        c == ConnectivityResult.mobile ||
        c == ConnectivityResult.wifi   ||
        c == ConnectivityResult.ethernet);
  }

  // -- Internal ---------------------------------------------------------------
  static List<Map<String, dynamic>> _load(SharedPreferences prefs) {
    final raw = prefs.getString(_key);
    if (raw == null) return [];
    return List<Map<String, dynamic>>.from(jsonDecode(raw));
  }
}

