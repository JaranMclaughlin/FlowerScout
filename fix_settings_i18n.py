import pathlib

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
t = p.read_text(encoding='utf-8')

replacements = [
    # Theme/date/map dropdown items
    ("items: const ['System default', 'Light', 'Dark'],",
     "items: [s.themeSystem, s.themeLight, s.themeDark],"),
    ("items: const ['DD/MM/YYYY', 'MM/DD/YYYY', 'YYYY-MM-DD (ISO)'],",
     "items: [s.dateFmtDMY, s.dateFmtMDY, s.dateFmtISO],"),
    ("items: const ['Satellite', 'Terrain', 'Street'],",
     "items: [s.mapSatellite, s.mapTerrain, s.mapStreet],"),
    # Role dropdown items
    ("items: const ['Scout', 'Viewer', 'Manager'],",
     "items: [s.roleScout, s.roleViewer, s.roleManager],"),
    # Notifications tab hardcoded strings
    ("'Control when and how FlowerScout notifies you.',",
     "s.controlNotif,"),
    ("'Critical pest / disease alert',",
     "s.criticalAlert,"),
    ("'Every Monday 7 AM \u2013 farm health digest',",
     "s.weeklyDescFull,"),
    # Preferences tab
    ("'Personalise how FlowerScout looks and behaves.',",
     "s.personaliseDesc,"),
    ("'Show heatmap on load',",
     "s.showHeatmap,"),
    ("'Auto-display scouting heatmap when opening Maps',",
     "s.showHeatmapDesc,"),
    # About/sign out
    ("subtitle: 'Version 1.0.0 \u00b7 Flutter',",
     "subtitle: s.versionLabel,"),
    ("subtitle: 'Log out of FlowerScout',",
     "subtitle: s.logOut,"),
    # Farm config section header
    ("_sectionHeader('Farm & greenhouse config',",
     "_sectionHeader(s.farmGhConfigTitle,"),
    # Role label in tab bar
    ("'scout'        => 'Scout',",
     "'scout'        => s.roleScout,"),
    # Tab labels
    ("_Tab.farms         => (label: 'Farm config',   icon: Icons.agriculture_rounded),",
     "_Tab.farms         => (label: s.tabFarms,   icon: Icons.agriculture_rounded),"),
]

failed = []
for old, new in replacements:
    if old in t:
        t = t.replace(old, new, 1)
    else:
        failed.append(old[:70])

p.write_text(t, encoding='utf-8')
print('settings_screen.dart updated.')
if failed: print('MISSED:', failed)