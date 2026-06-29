import pathlib

p1 = pathlib.Path('lib/shared/providers/farm_repository.dart')
lines = p1.read_text(encoding='utf-8').split('\n')
if '// ignore: unnecessary_cast' not in lines[256]:
    lines.insert(257, '      // ignore: unnecessary_cast')
p1.write_text('\n'.join(lines), encoding='utf-8')
print("OK: farm_repo line 258 suppressed")

p2 = pathlib.Path('lib/shared/trail/data/trail_repository.dart')
lines = p2.read_text(encoding='utf-8').split('\n')
if '// ignore: unnecessary_cast' not in lines[80]:
    lines.insert(81, '    // ignore: unnecessary_cast')
p2.write_text('\n'.join(lines), encoding='utf-8')
print("OK: trail_repo line 82 suppressed")