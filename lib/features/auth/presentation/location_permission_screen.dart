import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:geolocator/geolocator.dart';
import '../../../shared/widgets/app_shell.dart';
import '../../../shared/l10n/app_strings.dart';
import '../../../shared/providers/locale_provider.dart';

class LocationPermissionScreen extends ConsumerStatefulWidget {
  final String scoutName;

  const LocationPermissionScreen({
    super.key,
    required this.scoutName,
  });

  @override
  ConsumerState<LocationPermissionScreen> createState() =>
      _LocationPermissionScreenState();
}

class _LocationPermissionScreenState
    extends ConsumerState<LocationPermissionScreen> {
  bool _checking = false;

  AppStrings get s => AppStrings.of(ref.watch(localeProvider));

  // Navigate directly from here � no callback needed
  void _goToApp() {
    if (!mounted) return;
    Navigator.of(context).pushAndRemoveUntil(
      MaterialPageRoute(builder: (_) => const AppShell()),
      (route) => false, // clears entire stack
    );
  }

  Future<void> _handleAllow() async {
    setState(() => _checking = true);

    try {
      LocationPermission permission =
          await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
      }
      if (permission == LocationPermission.deniedForever) {
        setState(() => _checking = false);
        if (mounted) _showSettingsDialog();
        return;
      }
    } catch (_) {
      // Any error � still go to app
    }

    setState(() => _checking = false);


    _goToApp();
  }

  void _showSettingsDialog() {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (_) => AlertDialog(
        shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16)),
        title: Text(s.locationBlocked,
            style: const TextStyle(
                fontSize: 16, fontWeight: FontWeight.w600)),
        content: const Text(
          'Location was permanently denied. Open settings to '
          'enable it, or continue without GPS � scouting routes '
          'won\'t be recorded.',
          style: TextStyle(fontSize: 14, height: 1.5),
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              _goToApp();
            },
            child: Text(s.continueAnyway,
                style: const TextStyle(color: Color(0xFF888780))),
          ),
          TextButton(
            onPressed: () async {
              Navigator.pop(context);
              await Geolocator.openAppSettings();
              _goToApp();
            },
            child: Text(s.openAppSettings,
                style: const TextStyle(color: Color(0xFF1D9E75))),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final isTablet = MediaQuery.of(context).size.shortestSide >= 600;
    final maxWidth = isTablet ? 480.0 : double.infinity;

    final rawName = widget.scoutName;
    final displayName =
        rawName.replaceAll(RegExp(r'[0-9]'), '').trim();
    final name = displayName.isEmpty
        ? 'Scout'
        : displayName[0].toUpperCase() +
            displayName.substring(1);

    return Scaffold(
      backgroundColor: const Color(0xFFF5F4EF),
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: EdgeInsets.symmetric(
              horizontal: isTablet ? 0 : 24,
              vertical: 32,
            ),
            child: ConstrainedBox(
              constraints: BoxConstraints(maxWidth: maxWidth),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Center(
                    child: Container(
                      width: isTablet ? 88 : 72,
                      height: isTablet ? 88 : 72,
                      decoration: BoxDecoration(
                        color: const Color(0xFFE1F5EE),
                        shape: BoxShape.circle,
                        border: Border.all(
                            color: const Color(0xFF9FE1CB)),
                      ),
                      child: Icon(Icons.location_on_rounded,
                          color: const Color(0xFF1D9E75),
                          size: isTablet ? 40 : 34),
                    ),
                  ),

                  SizedBox(height: isTablet ? 28 : 20),

                  Text(s.allowLocationAccess,
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: isTablet ? 22 : 19,
                        fontWeight: FontWeight.w600,
                        color: const Color(0xFF2C2C2A),
                      )),

                  const SizedBox(height: 8),

                  Text(
                    'Hi $name! FlowerScout needs your GPS to track '
                    'your scouting route and ensure full farm coverage.',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: isTablet ? 15 : 13,
                      color: const Color(0xFF888780),
                      height: 1.5,
                    ),
                  ),

                  SizedBox(height: isTablet ? 32 : 24),

                  Container(
                    padding: EdgeInsets.all(isTablet ? 20 : 16),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(
                          color: const Color(0xFFD3D1C7),
                          width: 0.5),
                    ),
                    child: Column(children: [
                      _Reason(Icons.route_rounded,
                          s.recordsTrail,
                          isTablet),
                      const SizedBox(height: 12),
                      _Reason(Icons.grid_view_rounded,
                          s.tracksZones,
                          isTablet),
                      const SizedBox(height: 12),
                      _Reason(Icons.speed_rounded,
                          'Measures pace to flag rushing vs thorough scouting',
                          isTablet),
                      const SizedBox(height: 12),
                      _Reason(Icons.bar_chart_rounded,
                          s.powersAnalytics,
                          isTablet),
                    ]),
                  ),

                  SizedBox(height: isTablet ? 32 : 24),

                  SizedBox(
                    height: isTablet ? 52 : 48,
                    child: ElevatedButton(
                      onPressed: _checking ? null : _handleAllow,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF1D9E75),
                        foregroundColor: Colors.white,
                        elevation: 0,
                        shape: RoundedRectangleBorder(
                            borderRadius:
                                BorderRadius.circular(50)),
                      ),
                      child: _checking
                          ? const SizedBox(
                              width: 20,
                              height: 20,
                              child: CircularProgressIndicator(
                                  color: Colors.white,
                                  strokeWidth: 2))
                          : Text(s.allowWhileUsing,
                              style: TextStyle(
                                  fontSize: isTablet ? 16 : 14,
                                  fontWeight:
                                      FontWeight.w600)),
                    ),
                  ),

                  const SizedBox(height: 12),

                  SizedBox(
                    height: isTablet ? 48 : 44,
                    child: OutlinedButton(
                      onPressed: _checking ? null : _goToApp,
                      style: OutlinedButton.styleFrom(
                        foregroundColor:
                            const Color(0xFF888780),
                        side: const BorderSide(
                            color: Color(0xFFD3D1C7),
                            width: 0.5),
                        shape: RoundedRectangleBorder(
                            borderRadius:
                                BorderRadius.circular(50)),
                      ),
                      child: Text(s.notNow,
                          style: TextStyle(
                              fontSize: isTablet ? 15 : 13)),
                    ),
                  ),

                  SizedBox(height: isTablet ? 20 : 14),

                  Text(
                    'Your location is only used during active scouting sessions.',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: isTablet ? 12 : 11,
                      color: const Color(0xFFB4B2A9),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _Reason extends StatelessWidget {
  final IconData icon;
  final String text;
  final bool isTablet;
  const _Reason(this.icon, this.text, this.isTablet);

  @override
  Widget build(BuildContext context) => Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: isTablet ? 36 : 32,
            height: isTablet ? 36 : 32,
            decoration: BoxDecoration(
              color: const Color(0xFFE1F5EE),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(icon,
                color: const Color(0xFF1D9E75),
                size: isTablet ? 20 : 17),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.only(top: 6),
              child: Text(text,
                  style: TextStyle(
                      fontSize: isTablet ? 14 : 12,
                      color: const Color(0xFF5F5E5A),
                      height: 1.4)),
            ),
          ),
        ],
      );
}


