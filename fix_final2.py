import pathlib, re

# ── scouting_screen.dart — remove ghost import ────────────────────────
p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
text = p.read_text(encoding='utf-8')
text = text.replace("import 'voice_text_field.dart';\n", "")
p.write_text(text, encoding='utf-8')
print("scouting_screen.dart: ghost import removed.")

# ── maps_screen.dart — __ → _ ─────────────────────────────────────────
p = pathlib.Path('lib/features/maps/presentation/maps_screen.dart')
text = p.read_text(encoding='utf-8')
text = re.sub(r'\b__\b', '_', text)
p.write_text(text, encoding='utf-8')
print("maps_screen.dart: __ fixed.")