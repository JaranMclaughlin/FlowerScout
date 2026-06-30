import pathlib

# Check locale_provider default
p = pathlib.Path('lib/shared/providers/locale_provider.dart')
print("=== locale_provider.dart ===")
print(p.read_text(encoding='utf-8'))

# Check main.dart initState for onboarding
p2 = pathlib.Path('lib/main.dart')
lines = p2.read_text(encoding='utf-8').split('\n')
print("\n=== main.dart initState ===")
for i, l in enumerate(lines[188:225], 189):
    print(f"{i}: {l}")