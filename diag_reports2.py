import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')
print("=== Lines 1-60 (imports + structure) ===")
for i, l in enumerate(lines[0:60], 1):
    print(f"{i}: {l}")
print("\n=== Lines 200-260 (report detail/actions area) ===")
for i, l in enumerate(lines[199:260], 200):
    print(f"{i}: {l}")