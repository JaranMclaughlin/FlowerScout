import pathlib

p = pathlib.Path('lib/shared/providers/farm_repository.dart')
text = p.read_text(encoding='utf-8')

# Fix line 265 — remove the backslash before $
text = text.replace(
    r"throw FarmRepositoryException('Failed to load profile: \${e.message}');",
    "throw FarmRepositoryException('Failed to load profile: ${e.message}');"
)

# Fix line 300 — same
text = text.replace(
    r"throw FarmRepositoryException('Failed to load team: \${e.message}');",
    "throw FarmRepositoryException('Failed to load team: ${e.message}');"
)

p.write_text(text, encoding='utf-8')
print("Backslashes removed.")