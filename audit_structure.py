import pathlib, os

mobile = pathlib.Path('lib')

# 1. Show full file tree
print("=== FILE TREE ===")
for p in sorted(mobile.rglob('*.dart')):
    size = os.path.getsize(p)
    print(f"  {p}  ({size} bytes)")

# 2. Show pubspec versions
print("\n=== PUBSPEC DEPENDENCIES ===")
pub = pathlib.Path('pubspec.yaml').read_text(encoding='utf-8')
for line in pub.split('\n'):
    if line.strip() and not line.startswith('#'):
        print(line)