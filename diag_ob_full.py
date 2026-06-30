import pathlib, re

p = pathlib.Path('lib/features/onboarding/presentation/onboarding_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')
print(f"=== Lines 200-440 ===")
for i, l in enumerate(lines[199:], 200):
    print(f"{i}: {l}")

# Check app_strings for onboarding keys
s = pathlib.Path('lib/shared/l10n/app_strings.dart').read_text(encoding='utf-8')
onboard_keys = re.findall(r'String get (\w+)\s*=>', s)
onboard = [k for k in onboard_keys if any(x in k.lower() for x in ['onboard','welcome','scout','start','get','finish','next','back','skip','step'])]
print(f"\n=== Relevant AppStrings keys ===")
for k in onboard:
    m = re.search(rf"String get {k}\s*=>\s*_t\('([^']+)',\s*'([^']+)'\)", s)
    if m:
        print(f"  {k}: EN={m.group(1)!r} SW={m.group(2)!r}")