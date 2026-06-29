import pathlib

p = pathlib.Path('lib/shared/providers/farm_repository.dart')
text = p.read_text(encoding='utf-8')

# Fix 1: getMyProfile — catch _ but reference e.message (escaped)
text = text.replace(
    "    } on PostgrestException catch (_) {\n      final cached = _loadCachedProfile(uid);\n      if (cached != null) return cached;\n      throw FarmRepositoryException('Failed to load profile: \\${e.message}');",
    "    } on PostgrestException catch (e) {\n      final cached = _loadCachedProfile(uid);\n      if (cached != null) return cached;\n      throw FarmRepositoryException('Failed to load profile: \${e.message}');"
)

# Fix 2: getTeamMembers — catch _ but reference e.message (escaped)
text = text.replace(
    "    } on PostgrestException catch (_) {\n      throw FarmRepositoryException('Failed to load team: \\${e.message}');",
    "    } on PostgrestException catch (e) {\n      throw FarmRepositoryException('Failed to load team: \${e.message}');"
)

p.write_text(text, encoding='utf-8')
print("farm_repository.dart: catch blocks fixed.")