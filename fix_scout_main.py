import pathlib, re, sys

# ── scouting_screen.dart ─────────────────────────────────────────────
p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
text = p.read_text(encoding='utf-8')

# 1. Remove unnecessary dart:typed_data import
text = text.replace("import 'dart:typed_data';\n", "")

# 2. Remove dead _saveToQueue method (192) — find and delete it
text = re.sub(
    r'\n  Future<void> _saveToQueue\(Map<String, dynamic> report, List<Map<String, dynamic>> findings\) async \{.*?\n  \}\n',
    '\n',
    text,
    count=1,
    flags=re.DOTALL
)

# 3. Remove dead static loadQueue method
text = re.sub(
    r'\n  // ignore: unused_element\n  static Future<List<Map<String, dynamic>>> loadQueue\(\).*?\n  \}\n',
    '\n',
    text,
    count=1,
    flags=re.DOTALL
)

# 4. Remove dead static removeFromQueue method
text = re.sub(
    r'\n  // ignore: unused_element\n  static Future<void> removeFromQueue\(int index\).*?\n  \}\n',
    '\n',
    text,
    count=1,
    flags=re.DOTALL
)

# 5. Remove dead static queueLength method
text = re.sub(
    r'\n  static Future<int> queueLength\(\).*?\n  \}\n',
    '\n',
    text,
    count=1,
    flags=re.DOTALL
)

# 6. Remove dead static drainQueue method
text = re.sub(
    r'\n  // ignore: unused_element\n  static Future<void> drainQueue\(BuildContext\? context\).*?\n  \}\n',
    '\n',
    text,
    count=1,
    flags=re.DOTALL
)

# 7. __ → _ (unnecessary_underscores line 983)
text = re.sub(r'\b__\b', '_', text)

# 8. use_null_aware_elements line 384:
# if (trailId != null) 'trail_id': trailId  →  ?'trail_id': trailId
text = text.replace(
    "            if (trailId != null) 'trail_id': trailId,",
    "            ?'trail_id': trailId,"
)

# 9. use_null_aware_elements line 461 (offline queue path)
text = text.replace(
    "          if (trailId != null) 'trail_id': trailId,",
    "          ?'trail_id': trailId,"
)

# 10. curly_braces line 989
text = re.sub(
    r'(?m)\b((?:else\s+)?if)\s*(\([^)]*\))\s*\r?\n(\s+[^\n{][^\n]*;)',
    lambda m: f"{m.group(1)}{m.group(2)} {{\n{m.group(3)}\n}}",
    text
)

p.write_text(text, encoding='utf-8')
print("scouting_screen.dart cleaned.")

# ── main.dart ────────────────────────────────────────────────────────
p2 = pathlib.Path('lib/main.dart')
text2 = p2.read_text(encoding='utf-8')

text2 = text2.replace(
    "        anonKey: dotenv.env['SUPABASE_ANON_KEY']!,",
    "        publishableKey: dotenv.env['SUPABASE_ANON_KEY']!,"
)

p2.write_text(text2, encoding='utf-8')
print("main.dart: anonKey -> publishableKey.")