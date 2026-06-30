import pathlib, re

# ── maps_screen.dart: hardcoded Cancel ───────────────────────────────────────
p = pathlib.Path('lib/features/maps/presentation/maps_screen.dart')
t = p.read_text(encoding='utf-8')

# Find how s is accessed in maps_screen
if 'stringsProvider' in t:
    s_ref = 'ref.read(stringsProvider)'
elif 'AppStrings.of' in t:
    m = re.search(r'AppStrings\.of\([^)]+\)', t)
    s_ref = m.group(0) if m else None
else:
    s_ref = None
print(f"maps_screen s_ref: {s_ref}")

# Show imports and s usage
lines = t.split('\n')
for i, l in enumerate(lines, 1):
    if 'AppStrings' in l or 'strings' in l.lower() or 'locale' in l.lower():
        print(f"  {i}: {l}")