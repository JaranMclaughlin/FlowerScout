import pathlib

# ── Fix analytics_data.dart — remove duplicate inspectorName ──────────
p = pathlib.Path('lib/shared/providers/analytics_data.dart')
text = p.read_text(encoding='utf-8')
text = text.replace(
    "  final String inspectorName;\n  final String inspectorName;",
    "  final String inspectorName;"
)
p.write_text(text, encoding='utf-8')
print("analytics_data.dart: duplicate removed.")

# ── Fix farm_repository.dart — add missing _CacheKeys members ─────────
p2 = pathlib.Path('lib/shared/providers/farm_repository.dart')
text2 = p2.read_text(encoding='utf-8')

text2 = text2.replace(
    "  static const maxAgeMs        = 30 * 60 * 1000; // 30 minutes\n  static const profileMaxAgeMs = 30 * 60 * 1000; // 30 minutes",
    "  static const maxAgeMs        = 30 * 60 * 1000;\n  static const profileMaxAgeMs = 30 * 60 * 1000;"
)

# Add profileTime if missing
if "static String profileTime" not in text2:
    text2 = text2.replace(
        "  static String profile(String uid)      => 'cache_profile_v1_$uid';",
        "  static String profile(String uid)      => 'cache_profile_v1_$uid';\n  static String profileTime(String uid)  => 'cache_profile_time_v1_$uid';"
    )

p2.write_text(text2, encoding='utf-8')
print("farm_repository.dart: profileTime + profileMaxAgeMs added.")