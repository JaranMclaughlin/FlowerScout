import pathlib
p = pathlib.Path('lib/features/onboarding/presentation/onboarding_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')
lines[305] = "  const _Item(this.icon, this.title, this.desc);"
p.write_text('\n'.join(lines), encoding='utf-8')
print("Fixed")