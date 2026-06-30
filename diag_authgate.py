import pathlib

p = pathlib.Path('lib/main.dart')
lines = p.read_text(encoding='utf-8').split('\n')
print("=== Lines 278-295 (_AuthGate build) ===")
for i, l in enumerate(lines[277:295], 278):
    print(f"{i}: {repr(l)}")