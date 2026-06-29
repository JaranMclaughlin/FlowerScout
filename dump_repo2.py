import pathlib
p = pathlib.Path('lib/shared/providers/farm_repository.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i in [260,261,262,263,264,265,266, 297,298,299,300,301]:
    print(f"{i+1}\t{repr(lines[i])}")