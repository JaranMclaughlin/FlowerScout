import pathlib
p = pathlib.Path('lib/shared/providers/farm_repository.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i, line in enumerate(lines, start=1):
    if 'CacheKeys' in line and ('farms' in line or 'profile' in line or 'maxAge' in line or 'cache_' in line):
        print(f"{i}\t{repr(line)}")