import pathlib

p = pathlib.Path('lib/features/scouting/presentation/topbar_widgets.dart')
txt = p.read_text(encoding='utf-8', errors='replace')

# Fix _WeatherDetailSheet
txt = txt.replace(
    'class _WeatherDetailSheet extends StatelessWidget {',
    'class _WeatherDetailSheet extends ConsumerWidget {'
)
txt = txt.replace(
    '  Widget build(BuildContext context) {\n    final mins =\n        DateTime.now().difference(weather.fetchedAt).inMinutes;\n    final freshLabel = mins == 0 ? s.justNow',
    '  Widget build(BuildContext context, WidgetRef ref) {\n    final s = AppStrings.of(ref.watch(localeProvider));\n    final mins =\n        DateTime.now().difference(weather.fetchedAt).inMinutes;\n    final freshLabel = mins == 0 ? s.justNow'
)

# Fix _NotificationPanel
txt = txt.replace(
    'class _NotificationPanel extends StatelessWidget {',
    'class _NotificationPanel extends ConsumerWidget {'
)
txt = txt.replace(
    '  String _timeAgo(DateTime t) {\n    final diff = DateTime.now().difference(t);\n    if (diff.inMinutes < 1) return s.justNow;',
    '  String _timeAgo(DateTime t, AppStrings s) {\n    final diff = DateTime.now().difference(t);\n    if (diff.inMinutes < 1) return s.justNow;'
)
txt = txt.replace(
    '  Widget build(BuildContext context) {\n    final unread = notifications.where((n) => !n.isRead).length;',
    '  Widget build(BuildContext context, WidgetRef ref) {\n    final s = AppStrings.of(ref.watch(localeProvider));\n    final unread = notifications.where((n) => !n.isRead).length;'
)

# Fix 'Notifications' hardcoded header
txt = txt.replace(
    "              const Text(\n                        'Notifications',",
    "              Text(\n                        s.navScouting == 'Ukaguzi' ? 'Arifa' : 'Notifications',"
)

p.write_text(txt, encoding='utf-8')
print('done')