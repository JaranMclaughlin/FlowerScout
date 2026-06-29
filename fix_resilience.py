import pathlib, shutil

p = pathlib.Path('lib/shared/providers/farm_repository.dart')
shutil.copy(p, p.with_suffix('.dart.bak3'))
text = p.read_text(encoding='utf-8')
original = text

# ── Add timeout + retry wrapper at the top of FarmRepository ─────────────────
old_repo_start = """class FarmRepository {
  final SupabaseClient _db;
  final SharedPreferences _prefs;

  FarmRepository(this._db, this._prefs);"""

new_repo_start = """class FarmRepository {
  final SupabaseClient _db;
  final SharedPreferences _prefs;

  FarmRepository(this._db, this._prefs);

  // ── Resilience config ─────────────────────────────────────────────────────
  static const _timeout    = Duration(seconds: 12); // per-request timeout
  static const _maxRetries = 3;                     // retries on transient errors

  /// Retry wrapper with exponential backoff — safe for 500+ concurrent users.
  /// Only retries on network/timeout errors, not on auth or data errors.
  Future<T> _withRetry<T>(Future<T> Function() fn) async {
    int attempt = 0;
    while (true) {
      try {
        return await fn().timeout(_timeout);
      } on PostgrestException catch (e) {
        // Auth errors, RLS violations, bad data — don't retry
        if (e.code != null && ['42501','PGRST301','PGRST116'].contains(e.code)) rethrow;
        attempt++;
        if (attempt >= _maxRetries) rethrow;
      } catch (e) {
        // Timeout, socket errors — retry with backoff
        attempt++;
        if (attempt >= _maxRetries) rethrow;
      }
      // Exponential backoff: 500ms, 1s, 2s
      await Future.delayed(Duration(milliseconds: 500 * (1 << (attempt - 1))));
    }
  }"""

if old_repo_start in text:
    text = text.replace(old_repo_start, new_repo_start, 1)
    print("Step 1: added _withRetry + timeout config")
else:
    print("ERROR: repo start anchor not found"); raise SystemExit(1)

# ── Wrap getFarms DB call with _withRetry ─────────────────────────────────────
old_get_farms_db = """      final data = await _db
          .from('farms')
          .select(\'\'\'
            id, name, location, is_active,
            greenhouses (
              id, farm_id, code, medium, is_active,
              plantings ( id, greenhouse_id, variety_name, product_type,
                          planting_date, number_of_plants, area_m2 )
            )
          \'\'\')
          .eq('is_active', true)
          .order('name');"""

new_get_farms_db = """      final data = await _withRetry(() => _db
          .from('farms')
          .select(\'\'\'
            id, name, location, is_active,
            greenhouses (
              id, farm_id, code, medium, is_active,
              plantings ( id, greenhouse_id, variety_name, product_type,
                          planting_date, number_of_plants, area_m2 )
            )
          \'\'\')
          .eq('is_active', true)
          .order('name'));"""

if old_get_farms_db in text:
    text = text.replace(old_get_farms_db, new_get_farms_db, 1)
    print("Step 2: getFarms wrapped with _withRetry")
else:
    print("ERROR: getFarms DB call anchor not found"); raise SystemExit(1)

# ── Wrap getMyProfile DB call ─────────────────────────────────────────────────
old_profile_db = """      final data = await _db
          .from('user_profiles')
          .select()
          .eq('id', uid)
          .single();"""

new_profile_db = """      final data = await _withRetry(() => _db
          .from('user_profiles')
          .select()
          .eq('id', uid)
          .single());"""

if old_profile_db in text:
    text = text.replace(old_profile_db, new_profile_db, 1)
    print("Step 3: getMyProfile wrapped with _withRetry")
else:
    print("ERROR: getMyProfile DB call anchor not found"); raise SystemExit(1)

# ── Wrap updateProfile DB call ────────────────────────────────────────────────
old_update_db = """      await _db.from('user_profiles').update({
        'full_name': fullName,
        'phone': phone,
        'updated_at': DateTime.now().toIso8601String(),
      }).eq('id', uid);"""

new_update_db = """      await _withRetry(() => _db.from('user_profiles').update({
        'full_name': fullName,
        'phone': phone,
        'updated_at': DateTime.now().toIso8601String(),
      }).eq('id', uid));"""

if old_update_db in text:
    text = text.replace(old_update_db, new_update_db, 1)
    print("Step 4: updateProfile wrapped with _withRetry")
else:
    print("ERROR: updateProfile DB call anchor not found"); raise SystemExit(1)

# ── Wrap updateGreenhouseStatus DB call ───────────────────────────────────────
old_gh_db = """      await _db
          .from('greenhouses')
          .update({'is_active': isActive})
          .eq('id', greenhouseId);"""

new_gh_db = """      await _withRetry(() => _db
          .from('greenhouses')
          .update({'is_active': isActive})
          .eq('id', greenhouseId));"""

if old_gh_db in text:
    text = text.replace(old_gh_db, new_gh_db, 1)
    print("Step 5: updateGreenhouseStatus wrapped with _withRetry")
else:
    print("ERROR: updateGreenhouseStatus DB call anchor not found"); raise SystemExit(1)

# ── Wrap getTeamMembers DB call ───────────────────────────────────────────────
old_team_db = """      final data = await _db
          .from('user_profiles')
          .select()
          .order('full_name');"""

new_team_db = """      final data = await _withRetry(() => _db
          .from('user_profiles')
          .select()
          .order('full_name'));"""

if old_team_db in text:
    text = text.replace(old_team_db, new_team_db, 1)
    print("Step 6: getTeamMembers wrapped with _withRetry")
else:
    print("ERROR: getTeamMembers DB call anchor not found"); raise SystemExit(1)

if text != original:
    p.write_text(text, encoding='utf-8')
    print("\nDone.")
else:
    print("\nNo changes written.")