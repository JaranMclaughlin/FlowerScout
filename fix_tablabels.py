import pathlib
p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
t = p.read_text(encoding='utf-8')

# Fix remaining tab meta labels
replacements = [
    ("_Tab.profile       => (label: 'Profile',       icon: Icons.person_outline_rounded),",
     "_Tab.profile       => (label: s.tabProfile,    icon: Icons.person_outline_rounded),"),
    ("_Tab.team          => (label: 'Team',           icon: Icons.group_outlined),",
     "_Tab.team          => (label: s.tabTeam,        icon: Icons.group_outlined),"),
    ("_Tab.notifications => (label: 'Notifications',  icon: Icons.notifications_none_rounded),",
     "_Tab.notifications => (label: s.tabNotifications, icon: Icons.notifications_none_rounded),"),
    ("_Tab.preferences   => (label: 'Preferences',    icon: Icons.tune_rounded),",
     "_Tab.preferences   => (label: s.tabPreferences, icon: Icons.tune_rounded),"),
    # role display in member row
    ("'manager'      => 'Manager',",  "'manager'      => s.roleManager,"),
    ("'viewer'       => 'Viewer',",   "'viewer'       => s.roleViewer,"),
    ("'system_admin' => 'System Admin',", "'system_admin' => s.systemAdmin,"),
    # second Scout/Viewer/Manager dropdown (invite)
]

failed = []
for old, new in replacements:
    if old in t:
        t = t.replace(old, new, 1)
    else:
        failed.append(old[:70])

p.write_text(t, encoding='utf-8')
print('Tab labels fixed.')
if failed: print('MISSED:', failed)