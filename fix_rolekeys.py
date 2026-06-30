import pathlib

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')
for i, l in enumerate(lines, 1):
    if "_roleKeys" in l and "static const" in l:
        lines.insert(i-1, "  // ignore: unused_field")
        print(f"Suppressed _roleKeys at line {i}")
        break
p.write_text('\n'.join(lines), encoding='utf-8')