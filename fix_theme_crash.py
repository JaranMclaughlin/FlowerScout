import pathlib, shutil

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
shutil.copy(p, p.with_suffix('.dart.bak2'))
text = p.read_text(encoding='utf-8')
original = text

# The dropdown value is 'system' (stable key) but items are localized labels.
# _themeLabel helper already exists from the previous fix.
# Problem: the dropdown widget is still passing raw _theme as value instead of _themeLabel(_theme, s).
# Find and fix the _labeledDropdown call for theme.

# Pattern 1: value: _theme, where items are localized
old1 = "value: _theme,"
new1 = "value: _themeLabel(_theme, s),"
if old1 in text:
    text = text.replace(old1, new1, 1)
    print("Fixed: value now uses _themeLabel()")
else:
    print("WARNING: 'value: _theme,' not found")

# Pattern 2: items list still has raw localized strings instead of mapped keys
# items: [s.systemDefault, 'Light', 'Dark']  ->  items: _themeKeys.map((k) => _themeLabel(k, s)).toList()
old2 = "items: [s.systemDefault, 'Light', 'Dark'],"
new2 = "items: _themeKeys.map((k) => _themeLabel(k, s)).toList(),"
if old2 in text:
    text = text.replace(old2, new2, 1)
    print("Fixed: items now use _themeLabel mapping")
else:
    print("WARNING: items list pattern not found - checking alternate")
    # Try without comma
    old2b = "items: [s.systemDefault, 'Light', 'Dark']"
    new2b = "items: _themeKeys.map((k) => _themeLabel(k, s)).toList()"
    if old2b in text:
        text = text.replace(old2b, new2b, 1)
        print("Fixed (alt): items list replaced")
    else:
        print("WARNING: items list not found either - print current theme dropdown block:")
        # Print lines containing _theme or systemDefault for diagnosis
        for i, line in enumerate(text.split('\n'), 1):
            if '_theme' in line or 'systemDefault' in line or 'themeLabel' in line:
                print(f"  {i}: {line}")

# Pattern 3: onChanged still needs to reverse-map label -> key
old3 = "onChanged: (v) => setState(() => _theme = v!),"
new3 = "onChanged: (v) => setState(() => _theme = _themeKeys[_themeKeys.map((k) => _themeLabel(k, s)).toList().indexOf(v!)]),"
if old3 in text:
    text = text.replace(old3, new3, 1)
    print("Fixed: onChanged now reverse-maps label to key")
else:
    print("INFO: onChanged pattern not found (may already be correct or different format)")

if text != original:
    p.write_text(text, encoding='utf-8')
    print("\nDone. Run: flutter analyze lib\features\settings\presentation\settings_screen.dart")
else:
    print("\nNo changes made.")