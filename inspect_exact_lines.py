import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines(keepends=True)

print("--- Lines 1403-1411 (Excel block) ---")
for i in range(1402, 1411):
    print(f"{i+1}: {lines[i]!r}")

print()
print("--- Lines 1419-1429 (PDF block) ---")
for i in range(1418, 1429):
    print(f"{i+1}: {lines[i]!r}")