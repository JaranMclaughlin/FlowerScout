import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'farm_repository.dart';

// ── Core providers ────────────────────────────────────────────────────────────

final supabaseClientProvider = Provider<SupabaseClient>(
  (_) => Supabase.instance.client,
);

final sharedPrefsProvider = FutureProvider<SharedPreferences>(
  (_) => SharedPreferences.getInstance(),
);

final farmRepositoryProvider = Provider<FarmRepository>((ref) {
  final db    = ref.watch(supabaseClientProvider);
  final prefs = ref.watch(sharedPrefsProvider).value;
  if (prefs == null) throw StateError('SharedPreferences not ready');
  return FarmRepository(db, prefs);
});

// ── Auth state ────────────────────────────────────────────────────────────────

final authStateProvider = StreamProvider<AuthState>((ref) {
  return ref.watch(supabaseClientProvider).auth.onAuthStateChange;
});

final currentUserProvider = Provider<User?>((ref) {
  return ref.watch(supabaseClientProvider).auth.currentUser;
});

// ── Farms (cached, role-filtered via RLS) ────────────────────────────────────

class FarmsNotifier extends AsyncNotifier<List<FarmModel>> {
  @override
  Future<List<FarmModel>> build() async {
    final repo = ref.watch(farmRepositoryProvider);
    return repo.getFarms();
  }

  Future<void> refresh() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() {
      final repo = ref.read(farmRepositoryProvider);
      return repo.getFarms(forceRefresh: true);
    });
  }

  Future<void> toggleGreenhouse(String greenhouseId, bool isActive) async {
    final repo = ref.read(farmRepositoryProvider);
    await repo.updateGreenhouseStatus(greenhouseId, isActive);
    // Optimistic update in-memory
    state = state.whenData((farms) => farms.map((farm) {
      final updated = farm.greenhouses.map((gh) {
        if (gh.id == greenhouseId) {
          return GreenhouseModel(
            id: gh.id, farmId: gh.farmId, code: gh.code,
            medium: gh.medium, isActive: isActive, plantings: gh.plantings,
          );
        }
        return gh;
      }).toList();
      return FarmModel(
        id: farm.id, name: farm.name, location: farm.location,
        isActive: farm.isActive, greenhouses: updated,
      );
    }).toList());
  }
}

final farmsProvider = AsyncNotifierProvider<FarmsNotifier, List<FarmModel>>(
  FarmsNotifier.new,
);

// ── User profile ──────────────────────────────────────────────────────────────

class ProfileNotifier extends AsyncNotifier<UserProfileModel?> {
  @override
  Future<UserProfileModel?> build() async {
    final user = ref.watch(currentUserProvider);
    if (user == null) return null;
    final repo = ref.watch(farmRepositoryProvider);
    return repo.getMyProfile();
  }

  Future<void> refresh() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() {
      final repo = ref.read(farmRepositoryProvider);
      return repo.getMyProfile(forceRefresh: true);
    });
  }

  Future<void> save({required String fullName, String? phone}) async {
    final repo = ref.read(farmRepositoryProvider);
    await repo.updateProfile(fullName: fullName, phone: phone);
    await refresh();
  }
}

final profileProvider = AsyncNotifierProvider<ProfileNotifier, UserProfileModel?>(
  ProfileNotifier.new,
);

// -- Selected tab ------------------------------------------------------

// -- Team members ──────────────────────────────────────────────────────────────

final teamProvider = FutureProvider<List<UserProfileModel>>((ref) async {
  final user = ref.watch(currentUserProvider);
  if (user == null) return [];
  final repo = ref.watch(farmRepositoryProvider);
  return repo.getTeamMembers();
});
