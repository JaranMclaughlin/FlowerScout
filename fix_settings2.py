import pathlib
p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
t = p.read_text(encoding='utf-8')

# Find and fix const issue at line 190
# It's likely a const widget containing s. reference
# Replace all const _SectionHeader or similar with non-const
t = t.replace("const _SectionHeader(", "_SectionHeader(")
t = t.replace("const _SettingRow(", "_SettingRow(")

# Fix tab meta - find exact text
import re
# Replace remaining hardcoded tab labels
for old,new in [
    ("(label: 'Profile',", "(label: s.tabProfile,"),
    ("(label: 'Team',", "(label: s.tabTeam,"),
    ("(label: 'Notifications',", "(label: s.tabNotifications,"),
    ("(label: 'Preferences',", "(label: s.tabPreferences,"),
    ("(label: 'Farm config',", "(label: s.tabFarms,"),
]:
    t = t.replace(old, new, 1)

p.write_text(t, encoding='utf-8')
print('settings_screen.dart fixed.')