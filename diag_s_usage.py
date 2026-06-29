import pathlib, re

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')

# Find all Widget methods that reference s. but don't have s as a parameter
print("=== Methods that use 's.' but have no (AppStrings s) param ===")
in_method = False
method_start = 0
method_name = ""
method_lines = []
brace_depth = 0

for i, line in enumerate(lines, 1):
    # Detect method signatures
    m = re.match(r'\s+Widget\s+(\w+)\s*\(([^)]*)\)', line)
    if m:
        method_name = m.group(1)
        params = m.group(2)
        method_lines = [(i, line)]
        in_method = True
        has_s_param = 'AppStrings s' in params
        brace_depth = line.count('{') - line.count('}')
        uses_s = False
    elif in_method:
        method_lines.append((i, line))
        brace_depth += line.count('{') - line.count('}')
        if 's.' in line or '_themeLabel' in line:
            uses_s = True
        if brace_depth <= 0 and len(method_lines) > 1:
            if uses_s and not has_s_param:
                print(f"\n  {method_name}() at line {method_lines[0][0]} uses s but has no AppStrings param")
            in_method = False