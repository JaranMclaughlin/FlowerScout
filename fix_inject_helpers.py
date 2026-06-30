import pathlib

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')

# Find the end of _themeLabel method (closing };)
insert_after = -1
for i in range(821, min(835, len(lines))):
    if lines[i].strip() == '};':
        insert_after = i
        break

if insert_after == -1:
    print("ERROR: could not find _themeLabel closing }; ")
else:
    print(f"Inserting after line {insert_after+1}: {repr(lines[insert_after])}")
    new_helpers = """
  static const _mapKeys  = ['satellite', 'terrain', 'street'];
  static const _dateKeys = ['dmy', 'mdy', 'iso'];
  static const _roleKeys = ['scout', 'viewer', 'manager'];

  String _mapLabel(String key, AppStrings s) => switch (key) {
        'terrain' => s.mapTerrain,
        'street'  => s.mapStreet,
        _         => s.mapSatellite,
      };

  String _dateLabel(String key, AppStrings s) => switch (key) {
        'mdy' => s.dateFmtMDY,
        'iso' => s.dateFmtISO,
        _     => s.dateFmtDMY,
      };

  String _roleKeyToLabel(String key, AppStrings s) => switch (key) {
        'viewer'  => s.roleViewer,
        'manager' => s.roleManager,
        _         => s.roleScout,
      };

  String _roleLabelToKey(String label, AppStrings s) {
    if (label == s.roleViewer)  return 'viewer';
    if (label == s.roleManager) return 'manager';
    return 'scout';
  }"""
    lines.insert(insert_after + 1, new_helpers)
    p.write_text('\n'.join(lines), encoding='utf-8')
    print("Done: all helpers injected")