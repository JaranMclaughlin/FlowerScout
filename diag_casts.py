import pathlib

p1 = pathlib.Path('lib/shared/providers/farm_repository.dart')
l1 = p1.read_text(encoding='utf-8').split('\n')
print(f"farm_repo 258: {repr(l1[257])}")

p2 = pathlib.Path('lib/shared/trail/data/trail_repository.dart')
l2 = p2.read_text(encoding='utf-8').split('\n')
print(f"trail_repo 82: {repr(l2[81])}")