import 'dart:async';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:geolocator/geolocator.dart';
import 'models/scout_trail.dart';
import 'data/trail_repository.dart';
import 'providers/trail_providers.dart';
import '../providers/farm_providers.dart';

class TrailSessionState {
  final bool isActive;
  final String? trailId;
  final List<TrailPoint> points;
  const TrailSessionState({
    this.isActive = false,
    this.trailId,
    this.points = const [],
  });

  TrailSessionState copyWith({
    bool? isActive,
    String? trailId,
    List<TrailPoint>? points,
  }) =>
      TrailSessionState(
        isActive: isActive ?? this.isActive,
        trailId: trailId ?? this.trailId,
        points: points ?? this.points,
      );
}

class TrailTrackingController extends Notifier<TrailSessionState> {
  StreamSubscription<Position>? _posSub;
  Timer? _flushTimer;
  final List<TrailPoint> _buffer = [];
  int _seq = 0;

  @override
  TrailSessionState build() {
    ref.onDispose(() {
      _posSub?.cancel();
      _flushTimer?.cancel();
    });
    return const TrailSessionState();
  }

  Future<void> start({String? farmId, String? greenhouseId}) async {
    final db = ref.read(supabaseClientProvider);
    final scoutId = db.auth.currentUser?.id;
    if (scoutId == null) return;

    final repo = ref.read(trailRepositoryProvider);
    final trailId = await repo.startTrail(
      scoutId: scoutId,
      farmId: farmId,
      greenhouseId: greenhouseId,
    );

    _buffer.clear();
    _seq = 0;
    state = TrailSessionState(isActive: true, trailId: trailId, points: const []);

    _posSub = Geolocator.getPositionStream(
      locationSettings: const LocationSettings(
        accuracy: LocationAccuracy.high,
        distanceFilter: 8,
      ),
    ).listen((pos) {
      final pt = TrailPoint(
        lat: pos.latitude,
        lng: pos.longitude,
        recordedAt: DateTime.now(),
        accuracy: pos.accuracy,
        sequence: _seq++,
      );
      _buffer.add(pt);
      state = state.copyWith(points: [...state.points, pt]);
    });

    _flushTimer = Timer.periodic(const Duration(seconds: 15), (_) => _flush());
  }

  Future<void> _flush() async {
    if (_buffer.isEmpty || state.trailId == null) return;
    final toSend = List<TrailPoint>.from(_buffer);
    _buffer.clear();
    final repo = ref.read(trailRepositoryProvider);
    try {
      await repo.appendPoints(state.trailId!, toSend);
    } catch (_) {
      _buffer.insertAll(0, toSend);
    }
  }

  Future<String?> stop({
    String? reportId,
    String? farmId,
    String? greenhouseId,
  }) async {
    _posSub?.cancel();
    _flushTimer?.cancel();
    await _flush();
    final trailId = state.trailId;
    if (trailId != null) {
      final repo = ref.read(trailRepositoryProvider);
      await repo.endTrail(
        trailId,
        reportId: reportId,
        farmId: farmId,
        greenhouseId: greenhouseId,
      );
    }
    state = const TrailSessionState();
    return trailId;
  }
}

final trailTrackingControllerProvider =
    NotifierProvider<TrailTrackingController, TrailSessionState>(
        TrailTrackingController.new);