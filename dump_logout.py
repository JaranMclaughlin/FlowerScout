import pathlib
p = pathlib.Path('lib/shared/widgets/app_shell.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i, line in enumerate(lines, start=1):
    if any(x in line for x in ['signOut', 'Sign out', 'logout', 'Logout', 'Toka']):
        for j in range(max(0,i-3), min(len(lines),i+5)):
            print(f"{j+1}\t{repr(lines[j])}")
        print("---")