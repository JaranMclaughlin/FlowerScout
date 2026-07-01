import pathlib
for fname in ['lib/features/settings/presentation/settings_screen.dart', 'lib/main.dart']:
    p = pathlib.Path(fname)
    if not p.exists(): continue
    lines = p.read_text(encoding='utf-8').splitlines()
    for i, line in enumerate(lines, start=1):
        if any(x in line for x in ['signOut', 'Sign out']):
            print(f"=== {fname} ===")
            for j in range(max(0,i-3), min(len(lines),i+6)):
                print(f"{j+1}\t{repr(lines[j])}")
            print("---")