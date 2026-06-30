import pathlib, shutil

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
shutil.copy(p, p.with_suffix('.dart.bak_i18n'))
text = p.read_text(encoding='utf-8')
original = text

replacements = [
    # ── Section labels ────────────────────────────────────────────────────────
    ("label: 'INSPECTION DEFAULTS'",   "label: _s.inspectionDefaults.toUpperCase()"),
    ("label: 'INVITE A NEW MEMBER'",   "label: _s.inviteNewMember.toUpperCase()"),
    ("label: 'APPEARANCE'",            "label: _s.appearance.toUpperCase()"),
    ("label: 'THEME'",                 "label: _s.theme.toUpperCase()"),
    ("label: 'DATE FORMAT'",           "label: _s.dateFormat.toUpperCase()"),
    ("label: 'MAP DEFAULTS'",          "label: _s.mapDefaults.toUpperCase()"),
    ("label: 'DEFAULT VIEW'",          "label: _s.defaultView.toUpperCase()"),
    ("label: 'ABOUT'",                 "label: _s.about.toUpperCase()"),
    # EMAIL label appears twice - replace both
    ("label: 'EMAIL',\n              controller: _inviteCtrl,",
     "label: _s.emailLabel.toUpperCase(),\n              controller: _inviteCtrl,"),
    ("_styledTextField(label: 'EMAIL', controller: _inviteCtrl,",
     "_styledTextField(label: _s.emailLabel.toUpperCase(), controller: _inviteCtrl,"),
    # ROLE label appears twice
    ("label: 'ROLE', value: _inviteRole,\n                items: ['scout', 'viewer', 'manager'],",
     "label: _s.roleLabel.toUpperCase(), value: _inviteRole,\n                items: [_s.roleScout, _s.roleViewer, _s.roleManager],"),
    ("_labeledDropdown(label: 'ROLE', value: _inviteRole,\n            items: ['scout', 'viewer', 'manager'],",
     "_labeledDropdown(label: _s.roleLabel.toUpperCase(), value: _inviteRole,\n            items: [_s.roleScout, _s.roleViewer, _s.roleManager],"),

    # ── Map defaults dropdown items ────────────────────────────────────────────
    ("items: ['Satellite', 'Terrain', 'Street'],",
     "items: [_s.mapSatellite, _s.mapTerrain, _s.mapStreet],"),

    # ── Date format dropdown items ─────────────────────────────────────────────
    ("items: ['DD/MM/YYYY', 'MM/DD/YYYY', 'YYYY-MM-DD (ISO)'],",
     "items: [_s.dateFmtDMY, _s.dateFmtMDY, _s.dateFmtISO],"),
]

for old, new in replacements:
    if old in text:
        text = text.replace(old, new, 1)
        print(f"OK: {old[:50].strip()!r}")
    else:
        print(f"MISS: {old[:50].strip()!r}")

# ── Fix _dateFormat default to stable key ─────────────────────────────────────
# _dateFormat stores display value - need to store stable key like _theme
# For now just keep as-is since date format doesn't change with locale
# but _mapDefault stores 'Satellite' which won't match translated items
# Fix: store stable keys for _mapDefault and _inviteRole

# _mapDefault: store stable key, resolve at render time
old_map_default = "  String _mapDefault = 'Satellite';"
new_map_default = "  String _mapDefault = 'satellite'; // stable key: satellite|terrain|street"
if old_map_default in text:
    text = text.replace(old_map_default, new_map_default, 1)
    print("OK: _mapDefault now uses stable key")

# Add _mapLabel helper near _themeLabel
old_theme_label_helper = """  String _themeLabel(String key, AppStrings s) => switch (key) {
        'light' => 'Light',
        'dark' => 'Dark',
        _ => s.systemDefault,
      };"""
new_theme_label_helper = """  String _themeLabel(String key, AppStrings s) => switch (key) {
        'light' => s.themeLight,
        'dark'  => s.themeDark,
        _       => s.systemDefault,
      };

  static const _mapKeys = ['satellite', 'terrain', 'street'];
  String _mapLabel(String key, AppStrings s) => switch (key) {
        'terrain' => s.mapTerrain,
        'street'  => s.mapStreet,
        _         => s.mapSatellite,
      };"""
if old_theme_label_helper in text:
    text = text.replace(old_theme_label_helper, new_theme_label_helper, 1)
    print("OK: added _mapLabel helper + fixed themeLight/themeDark labels")
else:
    print("MISS: _themeLabel helper anchor")

# Fix the map dropdown to use stable keys like theme dropdown
old_map_dropdown = """        _labeledDropdown(label: _s.defaultView.toUpperCase(), value: _mapDefault,
            items: [_s.mapSatellite, _s.mapTerrain, _s.mapStreet],
            onChanged: (v) => setState(() => _mapDefault = v!)),"""
new_map_dropdown = """        _labeledDropdown(label: _s.defaultView.toUpperCase(),
            value: _mapLabel(_mapDefault, _s),
            items: _mapKeys.map((k) => _mapLabel(k, _s)).toList(),
            onChanged: (v) => setState(() =>
                _mapDefault = _mapKeys[_mapKeys.map((k) => _mapLabel(k, _s)).toList().indexOf(v!)])),"""
if old_map_dropdown in text:
    text = text.replace(old_map_dropdown, new_map_dropdown, 1)
    print("OK: map dropdown uses stable key pattern")
else:
    print("MISS: map dropdown anchor")

# Fix _inviteRole: store stable key, display translated label
old_invite_role = "  String _inviteRole = 'scout';"
new_invite_role = "  String _inviteRole = 'scout'; // stable key: scout|viewer|manager"
if old_invite_role in text:
    text = text.replace(old_invite_role, new_invite_role, 1)
    print("OK: _inviteRole comment added")

# Fix _dateFormat to use stable key
old_date_format = "  String _dateFormat = 'DD/MM/YYYY';"
new_date_format = "  String _dateFormat = 'dmy'; // stable key: dmy|mdy|iso"
if old_date_format in text:
    text = text.replace(old_date_format, new_date_format, 1)
    print("OK: _dateFormat now uses stable key")

# Add date format helpers near _mapLabel
old_map_keys = "  static const _mapKeys = ['satellite', 'terrain', 'street'];"
new_map_keys = """  static const _mapKeys  = ['satellite', 'terrain', 'street'];
  static const _dateKeys = ['dmy', 'mdy', 'iso'];
  String _dateLabel(String key, AppStrings s) => switch (key) {
        'mdy' => s.dateFmtMDY,
        'iso' => s.dateFmtISO,
        _     => s.dateFmtDMY,
      };"""
if old_map_keys in text:
    text = text.replace(old_map_keys, new_map_keys, 1)
    print("OK: added _dateLabel helper")
else:
    print("MISS: _mapKeys anchor")

# Fix date format dropdown to use stable key pattern
old_date_dropdown = """        _labeledDropdown(label: _s.dateFormat.toUpperCase(), value: _dateFormat,
            items: [_s.dateFmtDMY, _s.dateFmtMDY, _s.dateFmtISO],
            onChanged: (v) => setState(() => _dateFormat = v!)),"""
new_date_dropdown = """        _labeledDropdown(label: _s.dateFormat.toUpperCase(),
            value: _dateLabel(_dateFormat, _s),
            items: _dateKeys.map((k) => _dateLabel(k, _s)).toList(),
            onChanged: (v) => setState(() =>
                _dateFormat = _dateKeys[_dateKeys.map((k) => _dateLabel(k, _s)).toList().indexOf(v!)])),"""
if old_date_dropdown in text:
    text = text.replace(old_date_dropdown, new_date_dropdown, 1)
    print("OK: date format dropdown uses stable key pattern")
else:
    print("MISS: date format dropdown anchor")

# Fix invite role dropdown to use stable key pattern
old_role_dropdown = """label: _s.roleLabel.toUpperCase(), value: _inviteRole,\n            items: [_s.roleScout, _s.roleViewer, _s.roleManager],"""
new_role_dropdown = """label: _s.roleLabel.toUpperCase(),
            value: _roleKeyToLabel(_inviteRole, _s),
            items: [_s.roleScout, _s.roleViewer, _s.roleManager],"""
if old_role_dropdown in text:
    text = text.replace(old_role_dropdown, new_role_dropdown, 1)
    print("OK: role dropdown uses label helper")

# Add _roleKeyToLabel helper
old_date_keys = "  static const _dateKeys = ['dmy', 'mdy', 'iso'];"
new_date_keys = """  static const _dateKeys = ['dmy', 'mdy', 'iso'];
  static const _roleKeys = ['scout', 'viewer', 'manager'];
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
if old_date_keys in text:
    text = text.replace(old_date_keys, new_date_keys, 1)
    print("OK: added _roleKeyToLabel + _roleLabelToKey helpers")

# Fix role onChanged to reverse-map
old_role_onchanged = """onChanged: (v) => setState(() => _inviteRole = v!)),"""
new_role_onchanged = """onChanged: (v) => setState(() => _inviteRole = _roleLabelToKey(v!, _s))),"""
if old_role_onchanged in text:
    text = text.replace(old_role_onchanged, new_role_onchanged, 1)
    print("OK: role onChanged reverse-maps label to key")

# Fix wide layout role dropdown too (line 545 version)
old_role_wide = """label: _s.roleLabel.toUpperCase(), value: _inviteRole,\n                items: [_s.roleScout, _s.roleViewer, _s.roleManager],"""
new_role_wide = """label: _s.roleLabel.toUpperCase(),
                value: _roleKeyToLabel(_inviteRole, _s),
                items: [_s.roleScout, _s.roleViewer, _s.roleManager],"""
if old_role_wide in text:
    text = text.replace(old_role_wide, new_role_wide, 1)
    print("OK: wide role dropdown uses label helper")

if text != original:
    p.write_text(text, encoding='utf-8')
    print("\nSaved.")
else:
    print("\nNo changes written.")