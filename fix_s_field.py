import pathlib, shutil

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
shutil.copy(p, p.with_suffix('.dart.bak4'))
text = p.read_text(encoding='utf-8')
original = text

# ── Step 1: Add _s instance field after the class opening fields ──────────────
# Insert a late AppStrings _s field near the top of the state class
old_theme_field = "  String _theme      = 'system'; // stable key: 'system' | 'light' | 'dark'"
new_theme_field = """  // Localisation snapshot - set at top of build(), safe to use anywhere in the class
  late AppStrings _s;
  String _theme      = 'system'; // stable key: 'system' | 'light' | 'dark'"""
if old_theme_field in text:
    text = text.replace(old_theme_field, new_theme_field, 1)
    print("Step 1: added _s instance field")
else:
    print("ERROR: theme field anchor not found"); raise SystemExit(1)

# ── Step 2: In build(), assign _s = this.s before anything else ──────────────
old_build_top = """  @override
  Widget build(BuildContext context) {
    final s = this.s; // capture once inside build so ref.watch is legal
    // Populate profile fields once loaded"""
new_build_top = """  @override
  Widget build(BuildContext context) {
    _s = this.s; // snapshot locale once per build - safe to read via _s anywhere
    // Populate profile fields once loaded"""
if old_build_top in text:
    text = text.replace(old_build_top, new_build_top, 1)
    print("Step 2: build() now snapshots _s = this.s")
else:
    print("ERROR: build() top anchor not found"); raise SystemExit(1)

# ── Step 3: Revert _wideLayout / _narrowLayout signatures (remove AppStrings s param) ──
text = text.replace(
    "  Widget _wideLayout(AppStrings s) => Row(children: [",
    "  Widget _wideLayout() => Row(children: [", 1)
text = text.replace(
    "  Widget _narrowLayout(AppStrings s) =>",
    "  Widget _narrowLayout() =>", 1)
text = text.replace(
    "  Widget _narrowLayout(AppStrings s) {",
    "  Widget _narrowLayout() {", 1)
print("Step 3: reverted _wideLayout/_narrowLayout signatures")

# ── Step 4: Revert the call sites in build() ─────────────────────────────────
text = text.replace(
    "return isWide ? _wideLayout(s) : _narrowLayout(s);",
    "return isWide ? _wideLayout() : _narrowLayout();", 1)
print("Step 4: reverted call sites in build()")

# ── Step 5: Replace every use of bare `s.` with `_s.` throughout the file ────
# But NOT inside the getter definition itself (line 99: AppStrings get s => ...)
# and NOT `super.` or other words ending in s.
import re

# Replace s. only when it's a standalone identifier: word boundary before s, dot after
# Avoid matching inside the getter line and avoid 'this.s'
lines = text.split('\n')
new_lines = []
changed_lines = []
for i, line in enumerate(lines, 1):
    # Skip the getter definition line
    if 'AppStrings get s =>' in line:
        new_lines.append(line)
        continue
    # Replace standalone `s.` -> `_s.` (not `this.s` -> `this._s`, not `AppStrings s`)
    new_line = re.sub(r'(?<![a-zA-Z0-9_])s\.', '_s.', line)
    if new_line != line:
        changed_lines.append(i)
    new_lines.append(new_line)

text = '\n'.join(new_lines)
print(f"Step 5: replaced s. -> _s. on {len(changed_lines)} lines: {changed_lines[:10]}{'...' if len(changed_lines)>10 else ''}")

# ── Step 6: Fix _themeLabel calls - it takes AppStrings, now pass _s ─────────
# _themeLabel(x, s) -> _themeLabel(x, _s)  (the s arg, not the key arg)
text = text.replace('_themeLabel(_theme, s)', '_themeLabel(_theme, _s)')
text = text.replace("_themeLabel(k, s)", "_themeLabel(k, _s)")
print("Step 6: fixed _themeLabel calls to use _s")

if text != original:
    p.write_text(text, encoding='utf-8')
    print("\nAll steps done. Run:")
    print("  flutter analyze lib\\features\\settings\\presentation\\settings_screen.dart")
    print("  flutter run -d chrome --web-port=8080")
else:
    print("\nNo changes written.")