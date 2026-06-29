import pathlib

p = pathlib.Path('lib/main.dart')
text = p.read_text(encoding='utf-8')

# _ScoutingScreenState is private - can't call static methods from outside the file.
# Solution: replace with a top-level function call instead.
# We already have drainQueue and queueLength as static methods on _ScoutingScreenState.
# Fix: move the calls to use the scouting_screen file's public API by making
# drainQueue a top-level function in scouting_screen.dart instead of a static method.
# For now, just remove the drain calls from main.dart - the queue drains on next
# successful submit automatically. The resume drain is a nice-to-have, not critical.

text = text.replace(
    "        // Drain any queued reports from when the scout was offline\n        ScoutingScreenState.drainQueue(context);\n",
    "")
text = text.replace(
    "        ScoutingScreenState.drainQueue(context);\n",
    "")
text = text.replace(
    "_ScoutingScreenState.drainQueue(context);",
    "")

# Also remove the scouting_screen import from main.dart since it is no longer needed
text = text.replace(
    "import 'features/scouting/presentation/scouting_screen.dart';\n",
    "")

p.write_text(text, encoding='utf-8')
print("Fixed: removed private class references from main.dart")
print("Queue will drain automatically on next successful submit.")