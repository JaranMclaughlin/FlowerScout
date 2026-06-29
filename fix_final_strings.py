import pathlib

# Fix location_permission_screen
p = pathlib.Path('lib/features/auth/presentation/location_permission_screen.dart')
txt = p.read_text(encoding='utf-8', errors='replace')

txt = txt.replace(
    "import 'package:flutter/material.dart';\nimport 'package:geolocator/geolocator.dart';\nimport '../../../shared/widgets/app_shell.dart';\nimport '../../../core/location/location_tracking_service.dart';",
    "import 'package:flutter/material.dart';\nimport 'package:flutter_riverpod/flutter_riverpod.dart';\nimport 'package:geolocator/geolocator.dart';\nimport '../../../shared/widgets/app_shell.dart';\nimport '../../../core/location/location_tracking_service.dart';\nimport '../../../shared/l10n/app_strings.dart';\nimport '../../../shared/providers/locale_provider.dart';"
)
txt = txt.replace(
    'class LocationPermissionScreen extends StatefulWidget {',
    'class LocationPermissionScreen extends ConsumerStatefulWidget {'
)
txt = txt.replace(
    'State<LocationPermissionScreen> =>',
    'ConsumerState<LocationPermissionScreen> =>'
)
txt = txt.replace(
    'class _LocationPermissionScreenState extends State<LocationPermissionScreen>',
    'class _LocationPermissionScreenState extends ConsumerState<LocationPermissionScreen>'
)
txt = txt.replace("'Location blocked'", 's.locationBlocked')
txt = txt.replace("'Continue anyway'", 's.continueAnyway')
txt = txt.replace("'Open settings'", 's.openAppSettings')
txt = txt.replace("'Allow location access'", 's.allowLocationAccess')
txt = txt.replace("'Records your walking trail across the farm'", 's.recordsTrail')
txt = txt.replace("'Tracks which farm zones are covered or missed'", 's.tracksZones')
txt = txt.replace("'Powers distance and coverage analytics'", 's.powersAnalytics')
txt = txt.replace("'Allow while using app'", 's.allowWhileUsing')
txt = txt.replace("'Not now'", 's.notNow')
p.write_text(txt, encoding='utf-8')
print('location done')

# Fix topbar remaining
p2 = pathlib.Path('lib/features/scouting/presentation/topbar_widgets.dart')
txt2 = p2.read_text(encoding='utf-8', errors='replace')
txt2 = txt2.replace("'Feels like'", 's.feelsLike')
txt2 = txt2.replace("'High Severity Alert'", 's.highSeverityAlert')
txt2 = txt2.replace("'Potential pest outbreak detected'", 's.pestOutbreak')
txt2 = txt2.replace("'Inspection Due'", 's.inspectionDue')
txt2 = txt2.replace("'Report Ready'", 's.reportReady')
txt2 = txt2.replace("'Weekly scouting summary is ready to view'", 's.weeklySummaryReady')
txt2 = txt2.replace("'Irrigation Alert'", 's.irrigationAlert')
txt2 = txt2.replace("'No new notifications'", 's.noNewNotifications')
p2.write_text(txt2, encoding='utf-8')
print('topbar done')