import pathlib

# Check app_shell sign out button - line 186
p = pathlib.Path('lib/shared/widgets/app_shell.dart')
lines = p.read_text(encoding='utf-8').split('\n')
print("=== Lines 178-200 (sign out) ===")
for i, l in enumerate(lines[177:200], 178):
    print(f"{i}: {repr(l)}")

# Check main.dart auth gate for onboarding wiring
p2 = pathlib.Path('lib/main.dart')
lines2 = p2.read_text(encoding='utf-8').split('\n')
print("\n=== main.dart _AuthGate build ===")
for i, l in enumerate(lines2[240:260], 241):
    print(f"{i}: {repr(l)}")