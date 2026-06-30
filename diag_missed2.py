import pathlib

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')

for ln in [520, 538, 554]:
    print(f"=== Lines {ln}-{ln+5} ===")
    for i, l in enumerate(lines[ln-1:ln+5], ln):
        print(f"{i}: {repr(l)}")