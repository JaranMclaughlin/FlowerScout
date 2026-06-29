import pathlib

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
text = p.read_text(encoding='utf-8')

# 1. Store a stable key instead of a localized display label
old_field = "  String _theme      = 'System default';"
new_field = "  String _theme      = 'system'; // stable key: 'system' | 'light' | 'dark'"
if old_field not in text:
    raise SystemExit("_theme field anchor not found - aborting, no changes made.")
text = text.replace(old_field, new_field, 1)

# 2. Map key <-> localized label only at render time, so it can never mismatch
old_dropdown = """      _card(label: 'APPEARANCE', child: Column(children: [
        _labeledDropdown(label: 'THEME', value: _theme,
            items: [s.systemDefault, 'Light', 'Dark'],
            onChanged: (v) => setState(() => _theme = v!)),"""
new_dropdown = """      _card(label: 'APPEARANCE', child: Column(children: [
        _labeledDropdown(label: 'THEME', value: _themeLabel(_theme, s),
            items: _themeKeys.map((k) => _themeLabel(k, s)).toList(),
            onChanged: (v) => setState(() =>
                _theme = _themeKeys[_themeKeys.map((k) => _themeLabel(k, s)).toList().indexOf(v!)])),"""
if old_dropdown not in text:
    raise SystemExit("Theme dropdown anchor not found - aborting, no changes made.")
text = text.replace(old_dropdown, new_dropdown, 1)

# 3. Add the key list + label-mapping helper right before _labeledDropdown
old_helper_anchor = "  Widget _labeledDropdown({required String label, required String value,"
new_helper_anchor = """  static const _themeKeys = ['system', 'light', 'dark'];
  String _themeLabel(String key, AppStrings s) => switch (key) {
        'light' => 'Light',
        'dark' => 'Dark',
        _ => s.systemDefault,
      };

  Widget _labeledDropdown({required String label, required String value,"""
if old_helper_anchor not in text:
    raise SystemExit("_labeledDropdown anchor not found - aborting, no changes made.")
text = text.replace(old_helper_anchor, new_helper_anchor, 1)

p.write_text(text, encoding='utf-8')
print("settings_screen.dart fixed: theme stored as stable key, label resolved per-locale at render time.")