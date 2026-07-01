import pathlib, re, sys

# ── 1. Remove unused login_screen import from app_shell.dart ──────────
p = pathlib.Path('lib/shared/widgets/app_shell.dart')
text = p.read_text(encoding='utf-8')
text = text.replace(
    "import '../../features/auth/presentation/login_screen.dart';\n",
    ""
)
p.write_text(text, encoding='utf-8')
print("app_shell.dart: unused import removed.")

# ── 2. Remove the now-unused _confirmSignOut method ───────────────────
p2 = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
lines = p2.read_text(encoding='utf-8').splitlines(keepends=True)

# Find start line (method signature) and matching closing brace by depth
start_idx = None
for i, line in enumerate(lines):
    if '_confirmSignOut' in line and 'void' in line:
        start_idx = i
        break

if start_idx is None:
    sys.exit("Could not find _confirmSignOut method start.")

depth = 0
end_idx = None
started = False
for i in range(start_idx, len(lines)):
    depth += lines[i].count('{') - lines[i].count('}')
    if '{' in lines[i]:
        started = True
    if started and depth == 0:
        end_idx = i
        break

if end_idx is None:
    sys.exit("Could not find matching closing brace.")

print(f"Removing lines {start_idx+1} to {end_idx+1}")
del lines[start_idx:end_idx+1]
p2.write_text(''.join(lines), encoding='utf-8')
print("settings_screen.dart: _confirmSignOut method removed.")