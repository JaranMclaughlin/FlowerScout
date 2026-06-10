import 'dart:async';
import 'package:geolocator/geolocator.dart';

class LocationTrackingService {
  static final LocationTrackingService instance =
      LocationTrackingService._();

  LocationTrackingService._();

  StreamSubscription<Position>? _subscription;

  final List<Position> routePoints = [];

  bool get isTracking => _subscription != null;

  void startTracking() {
    if (_subscription != null) return;

    const settings = LocationSettings(
      accuracy: LocationAccuracy.best,
      distanceFilter: 5,
    );

    _subscription =
        Geolocator.getPositionStream(
          locationSettings: settings,
        ).listen((position) {
      routePoints.add(position);

      print(
        'GPS: ${position.latitude}, ${position.longitude}',
      );
    });
  }

  Future<void> stopTracking() async {
    await _subscription?.cancel();
    _subscription = null;
  }
}
