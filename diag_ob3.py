import pathlib
p = pathlib.Path('lib/features/onboarding/presentation/onboarding_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')
for i, l in enumerate(lines[50:200], 51):
    print(f"{i}: {l}")