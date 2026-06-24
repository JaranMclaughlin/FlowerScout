import pathlib

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
txt = p.read_text(encoding='utf-8')

txt = txt.replace(
    "_sectionHeader('Notifications & alerts',",
    "_sectionHeader(s.notificationsAlerts,"
)
txt = txt.replace(
    "_card(label: 'INSPECTION ALERTS', child: Column(children: [",
    "_card(label: s.inspectionAlerts, child: Column(children: ["
)
txt = txt.replace(
    "_toggleRow('Overdue inspection reminder',\n_notify when a greenhouse passes its inspection date',",
    "_toggleRow(s.overdueReminder,\ns.overdueDesc,"
)
txt = txt.replace(
    "_toggleRow('Overdue inspection reminder',\n'Notify when a greenhouse passes its inspection date',",
    "_toggleRow(s.overdueReminder,\ns.overdueDesc,"
)
txt = txt.replace(
    "'Immediate push when health score drops below threshold',",
    "s.criticalAlertDesc,"
)
txt = txt.replace(
    "_toggleRow('Weekly summary report',",
    "_toggleRow(s.weeklySummary,"
)
txt = txt.replace(
    "_card(label: 'DELIVERY CHANNELS', child: Column(children: [",
    "_card(label: s.deliveryChannels, child: Column(children: ["
)
txt = txt.replace(
    "_toggleRow('Push notifications', 'Mobile and desktop',",
    "_toggleRow(s.pushNotifications, s.pushDesc,"
)
txt = txt.replace(
    "_toggleRow('SMS', 'Add phone number in Profile',",
    "_toggleRow('SMS', s.addPhoneForSms,"
)
txt = txt.replace(
    "_saveButton('Save notification settings')",
    "_saveButton(s.saveNotifSettings)"
)

p.write_text(txt, encoding='utf-8')
print('done')