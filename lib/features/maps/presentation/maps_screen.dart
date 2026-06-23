import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:geolocator/geolocator.dart';
import '../../../shared/theme/app_colors.dart';

const _green  = AppColors.leaf;
const _greenL = AppColors.mint;
const _red    = AppColors.critical;
const _blue   = AppColors.info;
const _amber  = AppColors.warning;
const _bg     = AppColors.background;
const _muted  = AppColors.muted;
const _border = AppColors.border;
const _ink    = AppColors.ink;

Color _paceColor(double? mps) {
  if (mps == null) return _muted;
  final k = mps * 3.6;
  if (k < 0.3) return _muted;
  if (k < 2.0) return _green;
  if (k < 4.0) return _amber;
  return _red;
}

String _paceLabel(double? mps) {
  if (mps == null) return '—';
  final k = mps * 3.6;
  if (k < 0.3) return 'Stationary';
  if (k < 2.0) return 'Thorough';
  if (k < 4.0) return 'Normal';
  return 'Rushing';
}

double _calcDistance(List<LatLng> pts) {
  if (pts.length < 2) return 0;
  const d = Distance();
  double total = 0;
  for (int i = 0; i < pts.length - 1; i++) {
    total += d(pts[i], pts[i + 1]);
  }
  return total;
}

String _fmtDist(double m) =>
    m < 1000 ? '${m.toStringAsFixed(0)} m' : '${(m / 1000).toStringAsFixed(2)} km';

String _fmtDur(Duration d) =>
    '${d.inHours.toString().padLeft(2, '0')}:'
    '${(d.inMinutes % 60).toString().padLeft(2, '0')}:'
    '${(d.inSeconds % 60).toString().padLeft(2, '0')}';

class MapsScreen extends StatefulWidget {
  const MapsScreen({super.key});
  @override
  State<MapsScreen> createState() => _MapsScreenState();
}

class _MapsScreenState extends State<MapsScreen> {
  final _mapCtrl = MapController();
  bool _sessionActive = false;
  bool _followScout   = true;
  final List<LatLng> _trail = [];
  double? _lastSpeedMps;
  double? _lastAccuracy;
  DateTime? _sessionStart;
  Duration  _elapsed = Duration.zero;
  LatLng?   _currentPos;
  StreamSubscription<Position>? _posSub;
  Timer? _timer;
  static const _nairobi = LatLng(-1.2921, 36.8219);

  @override
  void dispose() {
    _posSub?.cancel();
    _timer?.cancel();
    super.dispose();
  }

  Future<void> _startSession() async {
    final perm = await Geolocator.checkPermission();
    if (perm == LocationPermission.denied || perm == LocationPermission.deniedForever) {
      _showPermDialog(); return;
    }
    HapticFeedback.mediumImpact();
    setState(() {
      _sessionActive = true;
      _followScout   = true;
      _trail.clear();
      _sessionStart  = DateTime.now();
      _elapsed       = Duration.zero;
      _lastSpeedMps  = null;
      _lastAccuracy  = null;
    });
    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      if (mounted) setState(() => _elapsed = DateTime.now().difference(_sessionStart!));
    });
    _posSub = Geolocator.getPositionStream(
      locationSettings: const LocationSettings(
        accuracy: LocationAccuracy.bestForNavigation,
        distanceFilter: 3,
      ),
    ).listen((pos) {
      final pt = LatLng(pos.latitude, pos.longitude);
      setState(() {
        _currentPos   = pt;
        _lastSpeedMps = pos.speed < 0 ? 0 : pos.speed;
        _lastAccuracy = pos.accuracy;
        _trail.add(pt);
      });
      if (_followScout) _mapCtrl.move(pt, _mapCtrl.camera.zoom);
    });
  }

  void _endSession() {
    HapticFeedback.mediumImpact();
    _posSub?.cancel();
    _timer?.cancel();
    setState(() => _sessionActive = false);
    if (_trail.isNotEmpty) _showSessionSummary();
  }

  void _showSessionSummary() {
    final dist = _calcDistance(_trail);
    showModalBottomSheet(
      context: context,
      backgroundColor: _bg,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (_) => Padding(
        padding: const EdgeInsets.fromLTRB(20, 16, 20, 32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Center(child: Container(width: 40, height: 4,
              decoration: BoxDecoration(color: _border, borderRadius: BorderRadius.circular(2)))),
            const SizedBox(height: 16),
            Row(children: [
              Container(padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(color: _greenL, borderRadius: BorderRadius.circular(10)),
                child: const Icon(Icons.route_rounded, color: _green, size: 20)),
              const SizedBox(width: 10),
              const Text('Session complete',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600, color: _ink)),
            ]),
            const SizedBox(height: 16),
            Row(children: [
              _SummaryTile(icon: Icons.straighten_rounded,  label: 'Distance', value: _fmtDist(dist),        color: _blue),
              const SizedBox(width: 10),
              _SummaryTile(icon: Icons.timer_rounded,       label: 'Duration', value: _fmtDur(_elapsed),     color: _green),
              const SizedBox(width: 10),
              _SummaryTile(icon: Icons.my_location_rounded, label: 'GPS pts',  value: '${_trail.length}',    color: _amber),
            ]),
            const SizedBox(height: 16),
            SizedBox(width: double.infinity, height: 44,
              child: ElevatedButton(
                onPressed: () => Navigator.pop(context),
                style: ElevatedButton.styleFrom(
                  backgroundColor: _green, foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(50)),
                  elevation: 0),
                child: const Text('Done', style: TextStyle(fontWeight: FontWeight.w600)))),
          ],
        ),
      ),
    );
  }

  void _showPermDialog() {
    showDialog(context: context, builder: (_) => AlertDialog(
      title: const Text('Location required'),
      content: const Text('Enable location permissions to start scouting.'),
      actions: [
        TextButton(onPressed: () => Navigator.pop(context), child: const Text('Cancel')),
        TextButton(onPressed: () async { Navigator.pop(context); await Geolocator.openAppSettings(); },
          child: const Text('Settings')),
      ],
    ));
  }

  @override
  Widget build(BuildContext context) {
    final isTablet = MediaQuery.of(context).size.shortestSide >= 600;
    final center   = _currentPos ?? _nairobi;
    return Scaffold(
      backgroundColor: _bg,
      body: Stack(children: [
        FlutterMap(
          mapController: _mapCtrl,
          options: MapOptions(
            initialCenter: center,
            initialZoom: 17,
            maxZoom: 20,
            minZoom: 10,
            onPositionChanged: (_, hasGesture) {
              if (hasGesture && _followScout) setState(() => _followScout = false);
            },
          ),
          children: [
            TileLayer(
              urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
              userAgentPackageName: 'com.example.mobile',
              maxZoom: 20,
              tileProvider: NetworkTileProvider(),
            ),
            if (_trail.length > 1)
              PolylineLayer(polylines: [
                Polyline(
                  points: _trail,
                  strokeWidth: isTablet ? 5 : 4,
                  color: _green,
                  borderStrokeWidth: 1.5,
                  borderColor: Colors.white,
                ),
              ]),
            MarkerLayer(markers: [
              if (_trail.isNotEmpty)
                Marker(
                  point: _trail.first,
                  width: 28, height: 36,
                  alignment: Alignment.topCenter,
                  child: const _StartPin(),
                ),
              if (_currentPos != null)
                Marker(
                  point: _currentPos!,
                  width: 26, height: 26,
                  child: _LiveCursor(color: _paceColor(_lastSpeedMps)),
                ),
            ]),
          ],
        ),
        if (_sessionActive)
          Positioned(
            top: MediaQuery.of(context).padding.top + 10,
            left: 12, right: 12,
            child: _StatsHUD(
              elapsed: _elapsed, trail: _trail,
              speedMps: _lastSpeedMps, accuracy: _lastAccuracy, isTablet: isTablet,
            ),
          ),
        if (_sessionActive && !_followScout)
          Positioned(
            top: MediaQuery.of(context).padding.top + 80,
            right: 12,
            child: GestureDetector(
              onTap: () {
                if (_currentPos != null) _mapCtrl.move(_currentPos!, _mapCtrl.camera.zoom);
                setState(() => _followScout = true);
              },
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 7),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: _border, width: 0.5),
                ),
                child: Row(mainAxisSize: MainAxisSize.min, children: const [
                  Icon(Icons.my_location_rounded, size: 14, color: _green),
                  SizedBox(width: 5),
                  Text('Re-center',
                    style: TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: _green)),
                ]),
              ),
            ),
          ),
        Positioned(
          bottom: 28 + MediaQuery.of(context).padding.bottom,
          left: 0, right: 0,
          child: Center(
            child: GestureDetector(
              onTap: _sessionActive ? _endSession : _startSession,
              child: Container(
                padding: EdgeInsets.symmetric(
                  horizontal: isTablet ? 40 : 28,
                  vertical:   isTablet ? 18  : 14,
                ),
                decoration: BoxDecoration(
                  color: _sessionActive ? _red : _green,
                  borderRadius: BorderRadius.circular(50),
                  boxShadow: const [
                    BoxShadow(color: Color(0x28000000), blurRadius: 12, offset: Offset(0, 4)),
                  ],
                ),
                child: Row(mainAxisSize: MainAxisSize.min, children: [
                  Icon(
                    _sessionActive ? Icons.stop_rounded : Icons.play_arrow_rounded,
                    color: Colors.white, size: isTablet ? 24 : 20,
                  ),
                  SizedBox(width: isTablet ? 10 : 8),
                  Text(
                    _sessionActive ? 'End scouting' : 'Start scouting',
                    style: TextStyle(
                      color: Colors.white, fontWeight: FontWeight.w700,
                      fontSize: isTablet ? 16 : 14,
                    ),
                  ),
                ]),
              ),
            ),
          ),
        ),
      ]),
    );
  }
}

class _StatsHUD extends StatelessWidget {
  final Duration elapsed;
  final List<LatLng> trail;
  final double? speedMps;
  final double? accuracy;
  final bool isTablet;
  const _StatsHUD({required this.elapsed, required this.trail,
    required this.speedMps, required this.accuracy, required this.isTablet});

  @override
  Widget build(BuildContext context) {
    final dist = _calcDistance(trail);
    final pc   = _paceColor(speedMps);
    final pl   = _paceLabel(speedMps);
    final acc  = accuracy != null ? '${accuracy!.toStringAsFixed(1)} m' : '—';
    return Container(
      padding: EdgeInsets.symmetric(
        horizontal: isTablet ? 18 : 12, vertical: isTablet ? 12 : 9),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: _border, width: 0.5),
        boxShadow: const [BoxShadow(color: Color(0x14000000), blurRadius: 8, offset: Offset(0,2))],
      ),
      child: Row(children: [
        Container(width: 7, height: 7,
          decoration: const BoxDecoration(shape: BoxShape.circle, color: _red)),
        const SizedBox(width: 5),
        const Text('LIVE', style: TextStyle(
          fontSize: 9, fontWeight: FontWeight.w800, color: _red, letterSpacing: 1.4)),
        const SizedBox(width: 12),
        Expanded(child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            _HUDStat(label: 'Time',     value: _fmtDur(elapsed), color: _ink),
            Container(width: 0.5, height: 24, color: _border),
            _HUDStat(label: 'Distance', value: _fmtDist(dist),   color: _ink),
            Container(width: 0.5, height: 24, color: _border),
            _HUDStat(label: 'Pace',     value: pl,               color: pc),
            Container(width: 0.5, height: 24, color: _border),
            _HUDStat(label: 'Accuracy', value: acc,              color: _ink),
            Container(width: 0.5, height: 24, color: _border),
            _HUDStat(label: 'GPS pts',  value: '${trail.length}',color: _ink),
          ],
        )),
      ]),
    );
  }
}

class _HUDStat extends StatelessWidget {
  final String label, value;
  final Color color;
  const _HUDStat({required this.label, required this.value, required this.color});
  @override
  Widget build(BuildContext context) => Column(
    mainAxisSize: MainAxisSize.min,
    children: [
      Text(value, style: TextStyle(fontSize: 12, fontWeight: FontWeight.w700, color: color)),
      const SizedBox(height: 1),
      Text(label, style: const TextStyle(fontSize: 9, color: _muted, letterSpacing: 0.3)),
    ],
  );
}

class _StartPin extends StatelessWidget {
  const _StartPin();
  @override
  Widget build(BuildContext context) => Column(
    mainAxisSize: MainAxisSize.min,
    children: [
      Container(
        width: 24, height: 24,
        decoration: BoxDecoration(
          color: _blue, shape: BoxShape.circle,
          border: Border.all(color: Colors.white, width: 2),
          boxShadow: const [BoxShadow(color: Color(0x30000000), blurRadius: 4, offset: Offset(0,2))],
        ),
        child: const Icon(Icons.flag_rounded, color: Colors.white, size: 13),
      ),
      Container(width: 2, height: 8, color: _blue),
    ],
  );
}

class _LiveCursor extends StatefulWidget {
  final Color color;
  const _LiveCursor({required this.color});
  @override
  State<_LiveCursor> createState() => _LiveCursorState();
}

class _LiveCursorState extends State<_LiveCursor> with SingleTickerProviderStateMixin {
  late AnimationController _ctrl;
  late Animation<double> _scale;
  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(vsync: this, duration: const Duration(milliseconds: 900))
      ..repeat(reverse: true);
    _scale = Tween(begin: 0.85, end: 1.15)
        .animate(CurvedAnimation(parent: _ctrl, curve: Curves.easeInOut));
  }
  @override
  void dispose() { _ctrl.dispose(); super.dispose(); }
  @override
  Widget build(BuildContext context) => ScaleTransition(
    scale: _scale,
    child: Container(
      width: 20, height: 20,
      decoration: BoxDecoration(
        color: widget.color, shape: BoxShape.circle,
        border: Border.all(color: Colors.white, width: 3),
        boxShadow: [BoxShadow(color: widget.color.withValues(alpha: 0.4), blurRadius: 8)],
      ),
    ),
  );
}

class _SummaryTile extends StatelessWidget {
  final IconData icon;
  final String label, value;
  final Color color;
  const _SummaryTile({required this.icon, required this.label,
    required this.value, required this.color});
  @override
  Widget build(BuildContext context) => Expanded(
    child: Container(
      padding: const EdgeInsets.symmetric(vertical: 12),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withValues(alpha: 0.2), width: 0.5),
      ),
      child: Column(children: [
        Icon(icon, color: color, size: 18),
        const SizedBox(height: 4),
        Text(value, style: TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: color)),
        const SizedBox(height: 2),
        Text(label, style: const TextStyle(fontSize: 10, color: _muted)),
      ]),
    ),
  );
}
