import pathlib, shutil

p = pathlib.Path('lib/shared/providers/farm_repository.dart')
shutil.copy(p, p.with_suffix('.dart.bak2'))
text = p.read_text(encoding='utf-8')

# Line 207: invalidate farms cache after greenhouse update
old1 = "      // Invalidate cache\n      await _prefs.remove(_CacheKeys.farms);"
new1 = "      // Invalidate cache for current user\n      final uid = _db.auth.currentUser?.id ?? 'anon';\n      await _prefs.remove(_CacheKeys.farms(uid));\n      await _prefs.remove(_CacheKeys.cacheTime(uid));"
if old1 in text:
    text = text.replace(old1, new1, 1)
    print("Fix 1: updateGreenhouseStatus cache invalidation fixed")
else:
    print("ERROR: line 207 anchor not found"); raise SystemExit(1)

# Line 254: invalidate profile cache after update
old2 = "      await _prefs.remove(_CacheKeys.profile);"
new2 = "      await _prefs.remove(_CacheKeys.profile(uid));"
if old2 in text:
    text = text.replace(old2, new2, 1)
    print("Fix 2: updateProfile cache invalidation fixed")
else:
    print("ERROR: line 254 anchor not found"); raise SystemExit(1)

p.write_text(text, encoding='utf-8')
print("Saved.")