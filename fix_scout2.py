import pathlib, re

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
text = p.read_text(encoding='utf-8')

# 1. Remove unused imports
text = text.replace("import 'dart:convert';\n", "")
text = text.replace("import 'package:shared_preferences/shared_preferences.dart';\n", "")

# 2. Remove dead constants block
text = re.sub(
    r"  static const _queueKey\s*=\s*'offline_report_queue';\n"
    r"  static const _deadLetterKey\s*=\s*'offline_report_dead_letter';\n"
    r"  static const _maxRetries\s*=\s*5;\n"
    r"  static const _maxConcurrent\s*=\s*3;[^\n]*\n",
    "",
    text,
    count=1
)

# 3. Revert invalid null-aware on map keys
text = text.replace("            ?'trail_id': trailId,", "            if (trailId != null) 'trail_id': trailId,")
text = text.replace("          ?'trail_id': trailId,", "          if (trailId != null) 'trail_id': trailId,")

# 4. curly_braces
text = re.sub(
    r'(?m)\b((?:else\s+)?if)\s*(\([^)]*\))\s*\r?\n(\s+[^\n{][^\n]*;)',
    lambda m: f"{m.group(1)}{m.group(2)} {{\n{m.group(3)}\n}}",
    text
)

p.write_text(text, encoding='utf-8')
print("Done.")