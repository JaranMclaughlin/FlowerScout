import pathlib
p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
t = p.read_text(encoding='utf-8')

# Fix _inviteRole default and theme/map/dateformat defaults to use keys not display values
# The dropdowns now show translated labels but value must match
# Solution: use index-based or keep internal values separate from display

# Fix invite role - use internal key, display translated
old1 = "  String _inviteRole = 'Scout';"
new1 = "  String _inviteRole = 'scout';"
if old1 in t: t = t.replace(old1, new1, 1)

# Fix role dropdown to use internal keys as values, translated as display
old2 = "items: [s.roleScout, s.roleViewer, s.roleManager],"
new2 = "items: ['scout', 'viewer', 'manager'],"
t = t.replace(old2, new2)

# Fix theme/date/map dropdowns - keep internal values, not translated
old3 = "items: [s.themeSystem, s.themeLight, s.themeDark],"
new3 = "items: ['System default', 'Light', 'Dark'],"
t = t.replace(old3, new3)

old4 = "items: [s.dateFmtDMY, s.dateFmtMDY, s.dateFmtISO],"
new4 = "items: ['DD/MM/YYYY', 'MM/DD/YYYY', 'YYYY-MM-DD (ISO)'],"
t = t.replace(old4, new4)

old5 = "items: [s.mapSatellite, s.mapTerrain, s.mapStreet],"
new5 = "items: ['Satellite', 'Terrain', 'Street'],"
t = t.replace(old5, new5)

# For dropdowns, we need value+display to differ - use DropdownMenuItem with child
# But simplest fix: translate the display label separately in the dropdown builder
# Replace the simple items list approach with translated display

p.write_text(t, encoding='utf-8')
print('Dropdown values fixed.')