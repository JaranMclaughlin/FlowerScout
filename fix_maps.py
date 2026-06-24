content = '''import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../shared/theme/app_colors.dart';
import '../../../shared/trail/data/trail_repository.dart';
import '../../../shared/trail/providers/trail_providers.dart';
import '../../../shared/providers/farm_providers.dart';

const _green  = AppColors.leaf;
const _greenL = AppColors.mint;
const _red    = AppColors.critical;
const _blue   = AppColors.info;
const _bg     = AppColors.background;
const _muted  = AppColors.muted;
const _border = AppColors.border;
const _ink    = AppColors.ink;

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
    m < 1000 ? m.toStringAsFixed(0) + ' m' : (m / 1000).toStringAsFixed(2) + ' km';

String _fmtDur(Duration d) =>
    d.inHours.toString().padLeft(2, '0') + ':' +
    (d.inMinutes % 60).toString().padLeft(2, '0') + ':' +
    (d.inSeconds % 60).toString().padLeft(2, '0');

class MapsScreen extends ConsumerWidget {
  const MapsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isManager = ref.watch(isManagerProvider);
    if (!isManager) {
      return Scaffold(
        backgroundColor: _bg,
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(32),
            child: Column(mainAxisSize: MainAxisSize.min, children: [
              Container(
                width: 72, height: 72,
                decoration: const BoxDecoration(color: _greenL, shape: BoxShape.circle),
                child: const Icon(Icons.map_rounded, color: _green, size: 34),
              ),
              const SizedBox(height: 20),
              const Text('Scout Trail Map',
                  style: TextStyle(fontFamily: 'Georgia', fontSize: 20,
                      fontWeight: FontWeight.w700, color: _ink)),
              const SizedBox(height: 8),
              const Text(
                'Trail tracking and playback are available to farm managers and admins.',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 13, color: _muted, height: 1.5),
              ),
            ]),
          ),
        ),
      );
    }
    return const _ManagerMapsView();
  }
}

class _ManagerMapsView extends ConsumerStatefulWidget {
  const _ManagerMapsView();
  @override
  ConsumerState<_ManagerMapsView> createState() => _ManagerMapsViewState();
}

class _ManagerMapsViewState extends ConsumerState<_ManagerMapsView> {
  bool _showLive = true;
  Timer? _liveRefresh;

  @override
  void initState() {
    super.initState();
    _liveRefresh = Timer.periodic(const Duration(seconds: 6), (_) {
      if (mounted) ref.invalidate(activeTrailsProvider);
    });
  }

  @override
  void dispose() {
    _liveRefresh?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: _bg,
      body: SafeArea(
        child: Column(children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
            child: Row(children: [
              Expanded(child: _toggleChip('Live Now', _showLive,
                  () => setState(() => _showLive = true))),
              const SizedBox(width: 10),
              Expanded(child: _toggleChip('History', !_showLive,
                  () => setState(() => _showLive = false))),
            ]),
          ),
          Expanded(child: _showLive ? const _LiveTrailsList() : const _TrailHistoryList()),
        ]),
      ),
    );
  }

  Widget _toggleChip(String label, bool active, VoidCallback onTap) =>
      GestureDetector(
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 12),
          alignment: Alignment.center,
          decoration: BoxDecoration(
            color: active ? _green : Colors.white,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: active ? _green : _border),
          ),
          child: Text(label,
              style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600,
                  color: active ? Colors.white : _muted)),
        ),
      );
}

class _LiveTrailsList extends ConsumerWidget {
  const _LiveTrailsList();
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final trailsAsync = ref.watch(activeTrailsProvider);
    return trailsAsync.when(
      loading: () => const Center(child: CircularProgressIndicator(color: _green, strokeWidth: 2)),
      error: (e, _) => const Center(child: Text('Could not load live scouts', style: TextStyle(color: _muted))),
      data: (trails) {
        if (trails.isEmpty) {
          return const Center(
            child: Padding(
              padding: EdgeInsets.all(24),
              child: Column(mainAxisSize: MainAxisSize.min, children: [
                Icon(Icons.route_rounded, color: _muted, size: 36),
                SizedBox(height: 12),
                Text('No scouts are currently out scouting',
                    style: TextStyle(color: _muted, fontSize: 13)),
              ]),
            ),
          );
        }
        return ListView.separated(
          padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
          itemCount: trails.length,
          separatorBuilder: (_, __) => const SizedBox(height: 10),
          itemBuilder: (_, i) => _TrailTile(trail: trails[i], isLive: true),
        );
      },
    );
  }
}

class _TrailHistoryList extends ConsumerWidget {
  const _TrailHistoryList();
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final trailsAsync = ref.watch(trailHistoryProvider);
    return trailsAsync.when(
      loading: () => const Center(child: CircularProgressIndicator(color: _green, strokeWidth: 2)),
      error: (e, _) => const Center(child: Text('Could not load trail history', style: TextStyle(color: _muted))),
      data: (trails) {
        if (trails.isEmpty) {
          return const Center(child: Text('No completed trails yet', style: TextStyle(color: _muted, fontSize: 13)));
        }
        return ListView.separated(
          padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
          itemCount: trails.length,
          separatorBuilder: (_, __) => const SizedBox(height: 10),
          itemBuilder: (_, i) => Dismissible(
            key: Key(trails[i].id),
            direction: DismissDirection.endToStart,
            background: Container(
              alignment: Alignment.centerRight,
              padding: const EdgeInsets.only(right: 20),
              decoration: BoxDecoration(color: const Color(0xFFA32D2D), borderRadius: BorderRadius.circular(14)),
              child: const Icon(Icons.delete_outline_rounded, color: Colors.white, size: 24),
            ),
            confirmDismiss: (_) async {
              return await showDialog<bool>(
                context: context,
                builder: (_) => AlertDialog(
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                  title: const Text('Delete trail?'),
                  content: const Text('This will permanently delete the trail and all its GPS points.'),
                  actions: [
                    TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Cancel')),
                    TextButton(onPressed: () => Navigator.pop(context, true),
                        child: const Text('Delete', style: TextStyle(color: Color(0xFFA32D2D)))),
                  ],
                ),
              ) ?? false;
            },
            onDismissed: (_) async {
              final repo = ref.read(trailRepositoryProvider);
              await repo.deleteTrail(trails[i].id);
              ref.invalidate(trailHistoryProvider);
            },
            child: _TrailTile(trail: trails[i], isLive: false),
          ),
        );
      },
    );
  }
}

class _TrailTile extends ConsumerWidget {
  final ScoutTrail trail;
  final bool isLive;
  const _TrailTile({required this.trail, required this.isLive});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final duration = (trail.endedAt ?? DateTime.now()).difference(trail.startedAt);
    final farms = ref.watch(farmsProvider).value ?? [];
    String? farmName;
    String? ghCode;
    for (final f in farms) {
      if (f.id == trail.farmId) {
        farmName = f.name;
        for (final gh in f.greenhouses) {
          if (gh.id == trail.greenhouseId) { ghCode = gh.code; break; }
        }
        break;
      }
    }
    final farmText = farmName != null ? (ghCode != null ? farmName + ' - ' + ghCode : farmName) : null;
    final statusText = isLive ? 'Live - ' : 'Completed - ';

    return GestureDetector(
      onTap: () => Navigator.push(context, MaterialPageRoute(
        builder: (_) => _TrailPlaybackScreen(trailId: trail.id, isLive: isLive),
      )),
      child: Container(
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: Colors.white, borderRadius: BorderRadius.circular(14),
          border: Border.all(color: _border),
        ),
        child: Row(children: [
          Container(width: 10, height: 10,
              decoration: BoxDecoration(shape: BoxShape.circle, color: isLive ? _red : _muted)),
          const SizedBox(width: 12),
          Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(trail.scoutName ?? 'Unknown scout',
                style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 14, color: _ink)),
            const SizedBox(height: 2),
            if (farmText != null)
              Padding(padding: const EdgeInsets.only(bottom: 2),
                child: Row(children: [
                  const Icon(Icons.agriculture_rounded, size: 12, color: _green),
                  const SizedBox(width: 4),
                  Text(farmText, style: const TextStyle(fontSize: 12, color: _green, fontWeight: FontWeight.w600)),
                ])),
            Text(statusText + _fmtDur(duration), style: const TextStyle(fontSize: 12, color: _muted)),
          ])),
          const Icon(Icons.chevron_right_rounded, color: _muted),
        ]),
      ),
    );
  }
}

class _TrailPlaybackScreen extends ConsumerStatefulWidget {
  final String trailId;
  final bool isLive;
  const _TrailPlaybackScreen({required this.trailId, required this.isLive});
  @override
  ConsumerState<_TrailPlaybackScreen> createState() => _TrailPlaybackScreenState();
}

class _TrailPlaybackScreenState extends ConsumerState<_TrailPlaybackScreen> {
  final _mapCtrl = MapController();
  Timer? _liveRefresh;
  Timer? _playTimer;
  bool _playing = false;
  double _cursor = 0;

  @override
  void initState() {
    super.initState();
    if (widget.isLive) {
      _liveRefresh = Timer.periodic(const Duration(seconds: 5), (_) {
        if (mounted) ref.invalidate(trailByIdProvider(widget.trailId));
      });
    }
  }

  @override
  void dispose() {
    _liveRefresh?.cancel();
    _playTimer?.cancel();
    super.dispose();
  }

  void _togglePlay(int pointCount) {
    if (_playing) { _playTimer?.cancel(); setState(() => _playing = false); return; }
    setState(() => _playing = true);
    _playTimer = Timer.periodic(const Duration(milliseconds: 200), (_) {
      setState(() {
        _cursor += 1;
        if (_cursor >= pointCount - 1) {
          _cursor = (pointCount - 1).toDouble();
          _playing = false;
          _playTimer?.cancel();
        }
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    final trailAsync = ref.watch(trailByIdProvider(widget.trailId));
    return Scaffold(
      backgroundColor: _bg,
      appBar: AppBar(
        backgroundColor: Colors.white, foregroundColor: _ink, elevation: 0,
        title: Text(widget.isLive ? 'Live trail' : 'Trail playback'),
      ),
      body: trailAsync.when(
        loading: () => const Center(child: CircularProgressIndicator(color: _green, strokeWidth: 2)),
        error: (e, _) => const Center(child: Text('Could not load trail', style: TextStyle(color: _muted))),
        data: (trail) {
          final pts = trail.points.map((p) => LatLng(p.lat, p.lng)).toList();
          if (pts.isEmpty) {
            return const Center(child: Text('No GPS points recorded for this trail', style: TextStyle(color: _muted)));
          }
          final idx = _cursor.clamp(0, pts.length - 1).toInt();
          final cursorPt = pts[idx];
          final distSoFar = _calcDistance(pts.sublist(0, idx + 1));

          return Column(children: [
            Expanded(child: FlutterMap(
              mapController: _mapCtrl,
              options: MapOptions(initialCenter: cursorPt, initialZoom: 17, maxZoom: 20, minZoom: 10),
              children: [
                TileLayer(urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                    userAgentPackageName: 'com.example.mobile', maxZoom: 20),
                PolylineLayer(polylines: [
                  Polyline(points: pts, strokeWidth: 4, color: _green,
                      borderStrokeWidth: 1.5, borderColor: Colors.white),
                ]),
                MarkerLayer(markers: [
                  Marker(point: pts.first, width: 24, height: 24,
                      child: const Icon(Icons.flag_rounded, color: _blue, size: 20)),
                  Marker(point: cursorPt, width: 22, height: 22,
                      child: Container(decoration: BoxDecoration(
                        color: widget.isLive ? _red : _green, shape: BoxShape.circle,
                        border: Border.all(color: Colors.white, width: 3)))),
                ]),
              ],
            )),
            Container(
              padding: const EdgeInsets.fromLTRB(16, 12, 16, 24),
              decoration: const BoxDecoration(color: Colors.white,
                  border: Border(top: BorderSide(color: _border))),
              child: Column(children: [
                Row(children: [
                  Text(_fmtDist(distSoFar), style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 13)),
                  const Spacer(),
                  Text((idx + 1).toString() + ' / ' + pts.length.toString() + ' pts',
                      style: const TextStyle(color: _muted, fontSize: 12)),
                ]),
                Slider(value: idx.toDouble(), min: 0, max: (pts.length - 1).toDouble(),
                    activeColor: _green, onChanged: (v) => setState(() => _cursor = v)),
                Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                  IconButton(
                    icon: Icon(_playing ? Icons.pause_circle_filled_rounded : Icons.play_circle_fill_rounded,
                        color: _green, size: 44),
                    onPressed: () => _togglePlay(pts.length)),
                ]),
              ]),
            ),
          ]);
        },
      ),
    );
  }
}
'''
open('lib/features/maps/presentation/maps_screen.dart', 'w', encoding='utf-8').write(content)
print('Done')