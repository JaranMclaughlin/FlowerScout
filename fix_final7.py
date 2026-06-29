import pathlib, re

# ── reports_screen.dart: suppress 3 unused color fields ──────────────────────
p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')
targets = {20, 22, 29}  # 1-indexed line numbers from analyzer
new_lines = []
for i, line in enumerate(lines, 1):
    if i in targets and '// ignore:' not in lines[i-2] if i > 1 else True:
        new_lines.append('  // ignore: unused_field')
    new_lines.append(line)
p.write_text('\n'.join(new_lines), encoding='utf-8')
print("OK: reports_screen color fields suppressed by line number")

# ── farm_repository.dart: fix lines 258+261+298 ──────────────────────────────
p = pathlib.Path('lib/shared/providers/farm_repository.dart')
t = p.read_text(encoding='utf-8')
lines = t.split('\n')

# Line 258: unnecessary cast - find and fix `as List<dynamic>` or `as List`
print(f"  farm_repo line 258: {repr(lines[257])}")
print(f"  farm_repo line 261: {repr(lines[260])}")
print(f"  farm_repo line 298: {repr(lines[297])}")

# Fix unnecessary cast at line 258 (0-indexed: 257)
if 'as List' in lines[257]:
    lines[257] = lines[257].replace(' as List<dynamic>', '').replace(' as List)', ')')
    print("OK: farm_repo line 258 cast removed")

# Fix unused catch clause at line 261 (0-indexed: 260) - change catch(e) to catch(_)
if 'catch (e)' in lines[260]:
    lines[260] = lines[260].replace('catch (e)', 'catch (_)')
    print("OK: farm_repo line 261 catch(e) -> catch(_)")

# Fix unused catch clause at line 298 (0-indexed: 297)
if 'catch (e)' in lines[297]:
    lines[297] = lines[297].replace('catch (e)', 'catch (_)')
    print("OK: farm_repo line 298 catch(e) -> catch(_)")

p.write_text('\n'.join(lines), encoding='utf-8')

# ── trail_repository.dart: fix line 82 unnecessary cast ──────────────────────
p = pathlib.Path('lib/shared/trail/data/trail_repository.dart')
lines = p.read_text(encoding='utf-8').split('\n')
print(f"\n  trail_repo line 82: {repr(lines[81])}")
# Remove the cast
if 'as List<dynamic>' in lines[81]:
    lines[81] = lines[81].replace(' as List<dynamic>', '')
    print("OK: trail_repo line 82 cast removed")
elif 'as List)' in lines[81]:
    lines[81] = lines[81].replace(' as List)', ')')
    print("OK: trail_repo line 82 cast removed (alt)")
p.write_text('\n'.join(lines), encoding='utf-8')