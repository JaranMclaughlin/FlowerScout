import pathlib, re

# ── analytics_screen.dart — last __ → _ ──────────────────────────────
p = pathlib.Path('lib/features/analytics/presentation/analytics_screen.dart')
text = p.read_text(encoding='utf-8')
lines = text.splitlines()
print(f"313: {repr(lines[312])}")
print(f"314: {repr(lines[313])}")
print(f"315: {repr(lines[314])}")