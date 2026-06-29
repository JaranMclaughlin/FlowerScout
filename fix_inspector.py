import pathlib, sys

# ── 1. Profile cache TTL — add 30min expiry ───────────────────────────
p = pathlib.Path('lib/shared/providers/farm_repository.dart')
text = p.read_text(encoding='utf-8')

# Add profile cache time key
text = text.replace(
    "  static String farms(String uid)     => 'cache_farms_v1_$uid';\n  static String profile(String uid)   => 'cache_profile_v1_$uid';\n  static String cacheTime(String uid) => 'cache_time_v1_$uid';\n  static const maxAgeMs = 30 * 60 * 1000; // 30 minutes",
    "  static String farms(String uid)        => 'cache_farms_v1_$uid';\n  static String profile(String uid)      => 'cache_profile_v1_$uid';\n  static String cacheTime(String uid)    => 'cache_time_v1_$uid';\n  static String profileTime(String uid)  => 'cache_profile_time_v1_$uid';\n  static const maxAgeMs        = 30 * 60 * 1000; // 30 minutes\n  static const profileMaxAgeMs = 30 * 60 * 1000; // 30 minutes"
)

# Add TTL check to _loadCachedProfile
text = text.replace(
    "  UserProfileModel? _loadCachedProfile(String uid) {\n    final raw = _prefs.getString(_CacheKeys.profile(uid));\n    if (raw == null) return null;\n    try {\n      return UserProfileModel.fromJson(jsonDecode(raw) as Map<String, dynamic>);\n    } catch (_) {\n      return null;\n    }\n  }",
    "  UserProfileModel? _loadCachedProfile(String uid) {\n    final ts = _prefs.getInt(_CacheKeys.profileTime(uid));\n    if (ts != null) {\n      final age = DateTime.now().millisecondsSinceEpoch - ts;\n      if (age > _CacheKeys.profileMaxAgeMs) return null;\n    }\n    final raw = _prefs.getString(_CacheKeys.profile(uid));\n    if (raw == null) return null;\n    try {\n      return UserProfileModel.fromJson(jsonDecode(raw) as Map<String, dynamic>);\n    } catch (_) {\n      return null;\n    }\n  }"
)

# Stamp profileTime on cache write
text = text.replace(
    "  Future<void> _cacheProfile(UserProfileModel profile) async {\n    await _prefs.setString(_CacheKeys.profile(profile.id), jsonEncode({",
    "  Future<void> _cacheProfile(UserProfileModel profile) async {\n    await _prefs.setInt(_CacheKeys.profileTime(profile.id), DateTime.now().millisecondsSinceEpoch);\n    await _prefs.setString(_CacheKeys.profile(profile.id), jsonEncode({"
)

p.write_text(text, encoding='utf-8')
print("farm_repository.dart: profile cache TTL added.")

# ── 2. Inspector name in reports table ────────────────────────────────
p2 = pathlib.Path('lib/shared/providers/analytics_data.dart')
text2 = p2.read_text(encoding='utf-8')

# Fix: fetch scout name from user_profiles join or use full_name field
# The query already has scout_id — add scout name to InspectionRecord
text2 = text2.replace(
    "  final String inspectorId;",
    "  final String inspectorId;\n  final String inspectorName;"
)
text2 = text2.replace(
    "    required this.inspectorId,\n  });",
    "    required this.inspectorId,\n    this.inspectorName = '',\n  });"
)

# Fix fromRow to use scout_name if available
text2 = text2.replace(
    "    return InspectionRecord(\n      id: r['id']?.toString() ?? '',\n      dateTime: dt,\n      dateLabel: label,\n      gh: r['greenhouse_code'] as String? ?? r['greenhouse_id']?.toString() ?? '—',\n      variety: r['variety_name'] as String? ?? '—',\n      category: topCat,\n      severity: topSev,\n      inspectorId: scoutId.length >= 8 ? scoutId.substring(0, 8) : scoutId,\n    );",
    "    final scoutName = r['scout_name'] as String? ?? r['user_profiles']?['full_name'] as String? ?? '';\n    return InspectionRecord(\n      id: r['id']?.toString() ?? '',\n      dateTime: dt,\n      dateLabel: label,\n      gh: r['greenhouse_code'] as String? ?? r['greenhouse_id']?.toString() ?? '—',\n      variety: r['variety_name'] as String? ?? '—',\n      category: topCat,\n      severity: topSev,\n      inspectorId: scoutId.length >= 8 ? scoutId.substring(0, 8) : scoutId,\n      inspectorName: scoutName,\n    );"
)

# Add scout_name to the query select
text2 = text2.replace(
    "    id, submitted_at, started_at, variety_name, greenhouse_id, scout_id,",
    "    id, submitted_at, started_at, variety_name, greenhouse_id, scout_id, scout_name,"
)

p2.write_text(text2, encoding='utf-8')
print("analytics_data.dart: inspector name added.")