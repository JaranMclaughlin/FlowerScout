import pathlib

p = pathlib.Path('lib/shared/providers/farm_repository.dart')
text = p.read_text(encoding='utf-8')

text = text.replace(
    "class _CacheKeys {\n  // Per-user keys: append userId so shared-device users never see each other's data\n  static String farms(String uid)     => 'cache_farms_v1_$uid';\n  static String profile(String uid)   => 'cache_profile_v1_$uid';\n  static String cacheTime(String uid) => 'cache_time_v1_$uid';\n  static const maxAgeMs = 5 * 60 * 1000; // 5 minutes\n}",
    "class _CacheKeys {\n  // Per-user keys: append userId so shared-device users never see each other's data\n  static String farms(String uid)       => 'cache_farms_v1_\$uid';\n  static String profile(String uid)     => 'cache_profile_v1_\$uid';\n  static String cacheTime(String uid)   => 'cache_time_v1_\$uid';\n  static String profileTime(String uid) => 'cache_profile_time_v1_\$uid';\n  static const maxAgeMs        = 30 * 60 * 1000; // 30 minutes\n  static const profileMaxAgeMs = 30 * 60 * 1000; // 30 minutes\n}"
)

p.write_text(text, encoding='utf-8')
print("Done.")