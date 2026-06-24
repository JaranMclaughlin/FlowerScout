import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/trail_repository.dart';
import '../models/scout_trail.dart';
import '../../providers/farm_providers.dart';

final trailRepositoryProvider = Provider<TrailRepository>((ref) {
  final db = ref.watch(supabaseClientProvider);
  return TrailRepository(db);
});

final activeTrailsProvider = FutureProvider<List<ScoutTrail>>((ref) {
  final repo = ref.watch(trailRepositoryProvider);
  return repo.getActiveTrails();
});

final trailHistoryProvider = FutureProvider<List<ScoutTrail>>((ref) {
  final repo = ref.watch(trailRepositoryProvider);
  return repo.getTrailHistory();
});

final trailByIdProvider =
    FutureProvider.family<ScoutTrail, String>((ref, trailId) {
  final repo = ref.watch(trailRepositoryProvider);
  return repo.getTrailById(trailId);
});
