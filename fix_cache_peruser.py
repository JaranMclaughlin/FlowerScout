import pathlib, shutil

# ── Fix 1: Per-user cache keys in farm_repository.dart ───────────────────────
p = pathlib.Path('lib/shared/providers/farm_repository.dart')
shutil.copy(p, p.with_suffix('.dart.bak'))
text = p.read_text(encoding='utf-8')
original = text

old_cache_keys = """class _CacheKeys {
  static const farms     = 'cache_farms_v1';
  static const profile   = 'cache_profile_v1';
  static const cacheTime = 'cache_time_v1';
  static const maxAgeMs  = 5 * 60 * 1000; // 5 minutes
}"""

new_cache_keys = """class _CacheKeys {
  // Per-user keys: append userId so shared-device users never see each other's data
  static String farms(String uid)     => 'cache_farms_v1_$uid';
  static String profile(String uid)   => 'cache_profile_v1_$uid';
  static String cacheTime(String uid) => 'cache_time_v1_$uid';
  static const maxAgeMs = 5 * 60 * 1000; // 5 minutes
}"""

if old_cache_keys in text:
    text = text.replace(old_cache_keys, new_cache_keys, 1)
    print("Fix 1a: cache keys are now per-user")
else:
    print("ERROR: cache keys anchor not found"); raise SystemExit(1)

# Fix cache validity check - needs uid
old_is_valid = """  bool _isCacheValid() {
    final ts = _prefs.getInt(_CacheKeys.cacheTime);
    if (ts == null) return false;
    return DateTime.now().millisecondsSinceEpoch - ts < _CacheKeys.maxAgeMs;
  }"""

new_is_valid = """  bool _isCacheValid(String uid) {
    final ts = _prefs.getInt(_CacheKeys.cacheTime(uid));
    if (ts == null) return false;
    return DateTime.now().millisecondsSinceEpoch - ts < _CacheKeys.maxAgeMs;
  }"""

if old_is_valid in text:
    text = text.replace(old_is_valid, new_is_valid, 1)
    print("Fix 1b: _isCacheValid takes uid")
else:
    print("ERROR: _isCacheValid anchor not found"); raise SystemExit(1)

# Fix _loadCachedFarms
old_load_farms = """  List<FarmModel>? _loadCachedFarms() {
    if (!_isCacheValid()) return null;
    final raw = _prefs.getString(_CacheKeys.farms);
    if (raw == null) return null;
    try {
      final list = jsonDecode(raw) as List;
      return list.map((f) => FarmModel.fromJson(f as Map<String, dynamic>)).toList();
    } catch (_) {
      return null;
    }
  }"""

new_load_farms = """  List<FarmModel>? _loadCachedFarms(String uid) {
    if (!_isCacheValid(uid)) return null;
    final raw = _prefs.getString(_CacheKeys.farms(uid));
    if (raw == null) return null;
    try {
      final list = jsonDecode(raw) as List;
      return list.map((f) => FarmModel.fromJson(f as Map<String, dynamic>)).toList();
    } catch (_) {
      return null;
    }
  }"""

if old_load_farms in text:
    text = text.replace(old_load_farms, new_load_farms, 1)
    print("Fix 1c: _loadCachedFarms takes uid")
else:
    print("ERROR: _loadCachedFarms anchor not found"); raise SystemExit(1)

# Fix _cacheFarms
old_cache_farms = """  Future<void> _cacheFarms(List<FarmModel> farms) async {
    await _prefs.setString(
        _CacheKeys.farms, jsonEncode(farms.map((f) => f.toJson()).toList()));
    await _prefs.setInt(
        _CacheKeys.cacheTime, DateTime.now().millisecondsSinceEpoch);
  }"""

new_cache_farms = """  Future<void> _cacheFarms(List<FarmModel> farms, String uid) async {
    await _prefs.setString(
        _CacheKeys.farms(uid), jsonEncode(farms.map((f) => f.toJson()).toList()));
    await _prefs.setInt(
        _CacheKeys.cacheTime(uid), DateTime.now().millisecondsSinceEpoch);
  }"""

if old_cache_farms in text:
    text = text.replace(old_cache_farms, new_cache_farms, 1)
    print("Fix 1d: _cacheFarms takes uid")
else:
    print("ERROR: _cacheFarms anchor not found"); raise SystemExit(1)

# Fix _loadCachedProfile
old_load_profile = """  UserProfileModel? _loadCachedProfile() {
    final raw = _prefs.getString(_CacheKeys.profile);
    if (raw == null) return null;
    try {
      return UserProfileModel.fromJson(jsonDecode(raw) as Map<String, dynamic>);
    } catch (_) {
      return null;
    }
  }"""

new_load_profile = """  UserProfileModel? _loadCachedProfile(String uid) {
    final raw = _prefs.getString(_CacheKeys.profile(uid));
    if (raw == null) return null;
    try {
      return UserProfileModel.fromJson(jsonDecode(raw) as Map<String, dynamic>);
    } catch (_) {
      return null;
    }
  }"""

if old_load_profile in text:
    text = text.replace(old_load_profile, new_load_profile, 1)
    print("Fix 1e: _loadCachedProfile takes uid")
else:
    print("ERROR: _loadCachedProfile anchor not found"); raise SystemExit(1)

# Fix _cacheProfile
old_cache_profile = """  Future<void> _cacheProfile(UserProfileModel profile) async {
    await _prefs.setString(_CacheKeys.profile, jsonEncode({"""

new_cache_profile = """  Future<void> _cacheProfile(UserProfileModel profile) async {
    await _prefs.setString(_CacheKeys.profile(profile.id), jsonEncode({"""

if old_cache_profile in text:
    text = text.replace(old_cache_profile, new_cache_profile, 1)
    print("Fix 1f: _cacheProfile uses profile.id as key")
else:
    print("ERROR: _cacheProfile anchor not found"); raise SystemExit(1)

# Fix getFarms to pass uid to cache methods
old_get_farms = """  Future<List<FarmModel>> getFarms({bool forceRefresh = false}) async {
    if (!forceRefresh) {
      final cached = _loadCachedFarms();
      if (cached != null) return cached;
    }

    try {
      final data = await _db"""

new_get_farms = """  Future<List<FarmModel>> getFarms({bool forceRefresh = false}) async {
    final uid = _db.auth.currentUser?.id ?? 'anon';
    if (!forceRefresh) {
      final cached = _loadCachedFarms(uid);
      if (cached != null) return cached;
    }

    try {
      final data = await _db"""

if old_get_farms in text:
    text = text.replace(old_get_farms, new_get_farms, 1)
    print("Fix 1g: getFarms passes uid to cache")
else:
    print("ERROR: getFarms anchor not found"); raise SystemExit(1)

# Fix _cacheFarms call in getFarms
old_cache_call = "      await _cacheFarms(farms);"
new_cache_call = "      await _cacheFarms(farms, uid);"
if old_cache_call in text:
    text = text.replace(old_cache_call, new_cache_call, 1)
    print("Fix 1h: _cacheFarms call updated")
else:
    print("ERROR: _cacheFarms call not found"); raise SystemExit(1)

# Fix _loadCachedFarms call in catch block
old_cached_catch = """      final cached = _loadCachedFarms();
      if (cached != null) return cached;"""
new_cached_catch = """      final cached = _loadCachedFarms(uid);
      if (cached != null) return cached;"""
if old_cached_catch in text:
    text = text.replace(old_cached_catch, new_cached_catch, 1)
    print("Fix 1i: catch block uses uid cache")
else:
    print("ERROR: catch _loadCachedFarms not found"); raise SystemExit(1)

# Fix getMyProfile to pass uid
old_get_profile = """  Future<UserProfileModel?> getMyProfile({bool forceRefresh = false}) async {
    final uid = _db.auth.currentUser?.id;
    if (uid == null) return null;

    if (!forceRefresh) {
      final cached = _loadCachedProfile();
      if (cached != null) return cached;
    }

    try {
      final data = await _db
          .from('user_profiles')
          .select()
          .eq('id', uid)
          .single();

      final profile = UserProfileModel.fromJson(data as Map<String, dynamic>);
      await _cacheProfile(profile);
      return profile;
    } on PostgrestException catch (e) {
      final cached = _loadCachedProfile();
      if (cached != null) return cached;
      throw FarmRepositoryException('Failed to load profile: ${e.message}');
    }
  }"""

new_get_profile = """  Future<UserProfileModel?> getMyProfile({bool forceRefresh = false}) async {
    final uid = _db.auth.currentUser?.id;
    if (uid == null) return null;

    if (!forceRefresh) {
      final cached = _loadCachedProfile(uid);
      if (cached != null) return cached;
    }

    try {
      final data = await _db
          .from('user_profiles')
          .select()
          .eq('id', uid)
          .single();

      final profile = UserProfileModel.fromJson(data as Map<String, dynamic>);
      await _cacheProfile(profile);
      return profile;
    } on PostgrestException catch (e) {
      final cached = _loadCachedProfile(uid);
      if (cached != null) return cached;
      throw FarmRepositoryException('Failed to load profile: \${e.message}');
    }
  }"""

if old_get_profile in text:
    text = text.replace(old_get_profile, new_get_profile, 1)
    print("Fix 1j: getMyProfile passes uid to cache methods")
else:
    print("ERROR: getMyProfile anchor not found"); raise SystemExit(1)

# Fix clearCache to clear for current user only
old_clear = """  Future<void> clearCache() async {
    await _prefs.remove(_CacheKeys.farms);
    await _prefs.remove(_CacheKeys.profile);
    await _prefs.remove(_CacheKeys.cacheTime);
  }"""

new_clear = """  Future<void> clearCache() async {
    final uid = _db.auth.currentUser?.id ?? 'anon';
    await _prefs.remove(_CacheKeys.farms(uid));
    await _prefs.remove(_CacheKeys.profile(uid));
    await _prefs.remove(_CacheKeys.cacheTime(uid));
  }"""

if old_clear in text:
    text = text.replace(old_clear, new_clear, 1)
    print("Fix 1k: clearCache is now per-user")
else:
    print("ERROR: clearCache anchor not found"); raise SystemExit(1)

if text != original:
    p.write_text(text, encoding='utf-8')
    print("\nfarm_repository.dart saved.")

# ── Fix 2: Remove dead Hive queue (PendingReport never wired up) ──────────────
hive_path = pathlib.Path('lib/core/offline/pending_finding.dart')
if hive_path.exists():
    # Keep the file but gut it - in case anything imports it
    hive_path.write_text(
        "// Dead code: offline queue migrated to SharedPreferences in scouting_screen.dart\n"
        "// This file retained to avoid breaking any imports.\n",
        encoding='utf-8'
    )
    print("Fix 2: gutted dead Hive PendingReport (never wired, replaced by SharedPreferences queue)")

print("\nAll fixes done.")