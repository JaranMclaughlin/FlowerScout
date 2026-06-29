import pathlib
p = pathlib.Path('lib/shared/providers/farm_repository.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i, line in enumerate(lines, start=1):
    if 'catch (PostgrestException _)' in line or "e.message" in line:
        for j in range(max(0,i-2), min(len(lines),i+4)):
            print(f"{j+1}\t{repr(lines[j])}")
        print("---")