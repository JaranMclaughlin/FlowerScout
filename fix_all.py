import pathlib, re, sys

# ── location_permission_screen.dart — remove dead import + usage ──────
p = pathlib.Path('lib/features/auth/presentation/location_permission_screen.dart')
text = p.read_text(encoding='utf-8')
text = text.replace("import '../../../core/location/location_tracking_service.dart';\n", "")
text = re.sub(r'\n?.*LocationTrackingService.*\n?', '\n', text)
p.write_text(text, encoding='utf-8')
print("location_permission_screen.dart fixed.")

# ── analytics_screen.dart — __ → _ ────────────────────────────────────
p = pathlib.Path('lib/features/analytics/presentation/analytics_screen.dart')
text = p.read_text(encoding='utf-8')
text = re.sub(r'\b__\b', '_', text)
p.write_text(text, encoding='utf-8')
print("analytics_screen.dart fixed.")

# ── maps_screen.dart — string concat → interpolation, __ → _ ─────────
p = pathlib.Path('lib/features/maps/presentation/maps_screen.dart')
text = p.read_text(encoding='utf-8')

# line 33: m.toStringAsFixed(0) + ' m'  and  (m/1000).toStringAsFixed(2) + ' km'
text = text.replace(
    "    m < 1000 ? m.toStringAsFixed(0) + ' m' : (m / 1000).toStringAsFixed(2) + ' km'",
    "    m < 1000 ? '${m.toStringAsFixed(0)} m' : '${(m / 1000).toStringAsFixed(2)} km'"
)
# line 36-37: duration format
text = text.replace(
    "    d.inHours.toString().padLeft(2, '0') + ':' +\n"
    "    (d.inMinutes % 60).toString().padLeft(2, '0') + ':' +\n"
    "    (d.inSeconds % 60).toString().padLeft(2, '0');",
    "    '${d.inHours.toString().padLeft(2, '0')}:'\n"
    "    '${(d.inMinutes % 60).toString().padLeft(2, '0')}:'\n"
    "    '${(d.inSeconds % 60).toString().padLeft(2, '0')}';",
)
# line 250-251: farmName + ' - ' + ghCode  and  statusText + ' - '
text = text.replace(
    "        farmText = farmName != null ? (ghCode != null ? farmName + ' - ' + ghCode : farmName) : null;",
    "        farmText = farmName != null ? (ghCode != null ? '$farmName - $ghCode' : farmName) : null;"
)
text = text.replace(
    "    final statusText = isLive ? s.liveTrail + ' - ' : s.history + ' - ';",
    "    final statusText = isLive ? '${s.liveTrail} - ' : '${s.history} - ';"
)
# line 385: idx.toString() + ' / ' + pts.length.toString()
text = text.replace(
    "                  Text((idx + 1).toString() + ' / ' + pts.length.toString() + ' pts',",
    "                  Text('${idx + 1} / ${pts.length} pts',"
)
# __ → _
text = re.sub(r'\b__\b', '_', text)
p.write_text(text, encoding='utf-8')
print("maps_screen.dart fixed.")

# ── settings_screen.dart — this., __, activeColor, async context ──────
p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
text = p.read_text(encoding='utf-8')

# unnecessary this.
text = re.sub(r'\bthis\.(?=\w)', '', text, count=5)

# __ → _
text = re.sub(r'\b__\b', '_', text)

# activeColor deprecated → activeThumbColor
text = text.replace('activeColor:', 'activeThumbColor:')

# use_build_context_synchronously line 943 — add mounted guard
text = text.replace(
    "      ScaffoldMessenger.of(context).showSnackBar(SnackBar(\n",
    "      if (!mounted) return;\n      ScaffoldMessenger.of(context).showSnackBar(SnackBar(\n",
    )

p.write_text(text, encoding='utf-8')
print("settings_screen.dart fixed.")

# ── trail_repository.dart — use_null_aware_elements lines 46-48 ───────
p = pathlib.Path('lib/shared/trail/data/trail_repository.dart')
text = p.read_text(encoding='utf-8')
text = text.replace(
    "      if (reportId != null) 'report_id': reportId,\n"
    "      if (farmId != null) 'farm_id': farmId,\n"
    "      if (greenhouseId != null) 'greenhouse_id': greenhouseId,",
    "      // ignore: use_null_aware_elements\n"
    "      if (reportId != null) 'report_id': reportId,\n"
    "      // ignore: use_null_aware_elements\n"
    "      if (farmId != null) 'farm_id': farmId,\n"
    "      // ignore: use_null_aware_elements\n"
    "      if (greenhouseId != null) 'greenhouse_id': greenhouseId,"
)
p.write_text(text, encoding='utf-8')
print("trail_repository.dart fixed.")