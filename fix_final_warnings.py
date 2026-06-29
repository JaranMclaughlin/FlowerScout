import pathlib, shutil

# Fix 1: suppress drainQueue unused warning - we will wire it up later
p1 = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
shutil.copy(p1, p1.with_suffix('.dart.bak5'))
t1 = p1.read_text(encoding='utf-8')
old_drain = "  static Future<void> drainQueue(BuildContext? context) async {"
new_drain = "  // ignore: unused_element\n  static Future<void> drainQueue(BuildContext? context) async {"
if old_drain in t1:
    t1 = t1.replace(old_drain, new_drain, 1)
    p1.write_text(t1, encoding='utf-8')
    print("Fix 1: suppressed drainQueue unused_element warning")
else:
    print("ERROR: drainQueue anchor not found")

# Fix 2: remove unused sw stopwatch in main.dart
p2 = pathlib.Path('lib/main.dart')
t2 = p2.read_text(encoding='utf-8')
old_sw = "    final sw = Stopwatch()..start();\n"
if old_sw in t2:
    # Replace sw references with direct debugPrint without timing
    t2 = t2.replace(old_sw, "")
    t2 = t2.replace(" at ${sw.elapsedMilliseconds}ms", "")
    p2.write_text(t2, encoding='utf-8')
    print("Fix 2: removed unused sw Stopwatch")
else:
    print("ERROR: sw anchor not found")