import pathlib, re

# ── analytics_screen.dart — ___ → _ ──────────────────────────────────
p = pathlib.Path('lib/features/analytics/presentation/analytics_screen.dart')
text = p.read_text(encoding='utf-8')
text = text.replace(
    'getDotPainter: (s, _, _, ___) =>',
    'getDotPainter: (s, _, _, _) =>'
)
p.write_text(text, encoding='utf-8')
print("analytics_screen.dart fixed.")

# ── maps_screen.dart — string concat → interpolation ─────────────────
p = pathlib.Path('lib/features/maps/presentation/maps_screen.dart')
text = p.read_text(encoding='utf-8')
text = text.replace(
    "    final farmText = farmName != null ? (ghCode != null ? farmName + ' - ' + ghCode : farmName) : null;",
    "    final farmText = farmName != null ? (ghCode != null ? '\$farmName - \$ghCode' : farmName) : null;"
)
p.write_text(text, encoding='utf-8')
print("maps_screen.dart fixed.")