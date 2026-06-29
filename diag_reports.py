import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')
print("=== Lines 15-35 ===")
for i, l in enumerate(lines[14:35], 15):
    print(f"{i}: {l}")