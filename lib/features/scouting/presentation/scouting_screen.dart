import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:uuid/uuid.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:geolocator/geolocator.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../../../shared/providers/farm_providers.dart';
import '../../../shared/providers/farm_repository.dart';
import '../../../shared/providers/locale_provider.dart';
import '../../../shared/l10n/app_strings.dart';
import '../../../shared/trail/trail_tracking_controller.dart';
import '../../../core/offline/offline_sync_service.dart';
import '../../../shared/theme/app_colors.dart';

class FindingData {
  String category;
  String severity;
  String issue;
  List<XFile>  photoFiles = [];   // local files (pre-upload)
  List<String> photoUrls  = [];   // Supabase Storage URLs (post-upload)
  FindingData({this.category = 'Disease', this.severity = 'Medium', this.issue = ''});
}


class ScoutingScreen extends ConsumerStatefulWidget {
  const ScoutingScreen({super.key});
  @override
  ConsumerState<ScoutingScreen> createState() => _ScoutingScreenState();
}

class _ScoutingScreenState extends ConsumerState<ScoutingScreen>
    with TickerProviderStateMixin {

  bool _scoutingStarted = false;
  DateTime? _sessionStart;
  Timer? _timer;
  int _elapsedSeconds = 0;
  Position? _gpsPosition;
  bool _locationDenied = false;

  FarmModel? selectedFarm;
  GreenhouseModel? selectedGreenhouse;
  String? selectedVariety;
  final List<FindingData> findings = [FindingData()];

  // Duplicate submit guard
  bool _submitting = false;
  bool _submitted  = false;
  int  _queueCount = 0; // offline queue badge

  late AnimationController _headerAnim;
  late Animation<double> _headerFade;

  double get progress {
    double v = 0;
    if (selectedFarm != null) v += 0.25;
    if (selectedGreenhouse != null) v += 0.25;
    if (selectedVariety != null) v += 0.25;
    if (findings.any((f) => f.issue.trim().isNotEmpty)) v += 0.25;
    return v;
  }

  String get _timerLabel {
    final m = (_elapsedSeconds ~/ 60).toString().padLeft(2, '0');
    final s = (_elapsedSeconds % 60).toString().padLeft(2, '0');
    return '$m:$s';
  }

  @override
  void initState() {
    super.initState();
    _refreshQueueCount();
    _headerAnim = AnimationController(vsync: this, duration: const Duration(milliseconds: 800));
    _headerFade = CurvedAnimation(parent: _headerAnim, curve: Curves.easeOut);
    _headerAnim.forward();
  }

  @override
  void dispose() {
    _headerAnim.dispose();
    _timer?.cancel();
    super.dispose();
  }

  Future<void> _requestLocationAndStart() async {
    final s = ref.read(stringsProvider);
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      _showLocationDialog(title: s.locationServicesOff, message: s.locationServicesMsg, showSettings: true);
      _startSession(withLocation: false);
      return;
    }
    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
    }
    if (permission == LocationPermission.deniedForever) {
      if (mounted) _showLocationDialog(title: s.locationPermReq, message: s.locationPermMsg, showSettings: true);
      _startSession(withLocation: false);
      return;
    }
    if (permission == LocationPermission.denied) {
      _startSession(withLocation: false);
      setState(() => _locationDenied = true);
      return;
    }
    try {
      final pos = await Geolocator.getCurrentPosition(
        locationSettings: const LocationSettings(accuracy: LocationAccuracy.high, timeLimit: Duration(seconds: 10)),
      );
      setState(() => _gpsPosition = pos);
    } catch (_) {}
    _startSession(withLocation: true);
  }

  void _startSession({required bool withLocation}) {
    // Start GPS trail tracking
    ref.read(trailTrackingControllerProvider.notifier).start(
      farmId: selectedFarm?.id,
      greenhouseId: selectedGreenhouse?.id,
    );
    setState(() {
      _scoutingStarted = true;
      _sessionStart = DateTime.now();
      _elapsedSeconds = 0;
      _submitted = false;
    });
    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      if (mounted) setState(() => _elapsedSeconds++);
    });
  }

  void _showLocationDialog({required String title, required String message, bool showSettings = false}) {
    final s = ref.read(stringsProvider);
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: Text(title, style: const TextStyle(fontFamily: 'Georgia', fontSize: 17)),
        content: Text(message, style: const TextStyle(fontSize: 13)),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: Text(s.continueAnyway)),
          if (showSettings)
            TextButton(
              onPressed: () { Navigator.pop(context); Geolocator.openAppSettings(); },
              child: Text(s.openAppSettings),
            ),
        ],
      ),
    );
  }


  // ── Queue badge ──────────────────────────────────────────────────────────────
  Future<void> _refreshQueueCount() async {
    final count = await OfflineSyncService.queueLength();
    if (mounted) setState(() => _queueCount = count);
  }

  // ── Offline queue (hardened) ─────────────────────────────────────────────





  /// Drains the offline queue - call this on app resume / reconnect

  Future<void> _submitReport() async {
    // Duplicate submit guard
    if (_submitting || _submitted) return;

    final s = ref.read(stringsProvider);

    if (selectedFarm == null || selectedGreenhouse == null || selectedVariety == null) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text(s.pleaseSelectAll), backgroundColor: AppColors.high));
      return;
    }
    if (!findings.any((f) => f.issue.trim().isNotEmpty)) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text(s.pleaseAddFinding), backgroundColor: AppColors.high));
      return;
    }

    setState(() { _submitting = true; _submitted = true; });
    _timer?.cancel();

    // Stop trail tracking
    final trailId = await ref.read(trailTrackingControllerProvider.notifier).stop(
      farmId: selectedFarm?.id,
      greenhouseId: selectedGreenhouse?.id,
    );

    try {
      final user = Supabase.instance.client.auth.currentUser;
      final reportId = await Supabase.instance.client
          .from('inspection_reports')
          .insert({
            'scout_id': user?.id,
            'greenhouse_id': selectedGreenhouse!.id,
            'variety_name': selectedVariety,
            'started_at': _sessionStart?.toIso8601String(),
            'submitted_at': DateTime.now().toIso8601String(),
            'duration_seconds': _elapsedSeconds,
            'latitude': _gpsPosition?.latitude,
            'longitude': _gpsPosition?.longitude,
            'status': 'submitted',
            // ignore: use_null_aware_elements
            // ignore: use_null_aware_elements
          if (trailId != null) 'trail_id': trailId,
          })
          .select('id')
          .single();

      for (final finding in findings.where((f) => f.issue.trim().isNotEmpty)) {
        // Upload any photos for this finding
        final List<String> uploadedUrls = [];
        for (final photo in finding.photoFiles) {
          try {
            final bytes    = await photo.readAsBytes();
            final ext      = photo.name.split('.').last.toLowerCase();
            final fileName = '${const Uuid().v4()}.$ext';
            final path     = 'findings/${reportId['id']}/$fileName';
            await Supabase.instance.client.storage
                .from('finding-photos')
                .uploadBinary(path, bytes,
                    fileOptions: FileOptions(contentType: 'image/$ext', upsert: false));
            final url = Supabase.instance.client.storage
                .from('finding-photos')
                .getPublicUrl(path);
            uploadedUrls.add(url);
          } catch (photoErr) {
            debugPrint('[photos] upload failed: \$photoErr');
          }
        }
        await Supabase.instance.client.from('inspection_findings').insert({
          'report_id': reportId['id'],
          'category': finding.category,
          'severity': finding.severity,
          'issue': finding.issue.trim(),
          if (uploadedUrls.isNotEmpty) 'photo_urls': uploadedUrls,
        });
      }

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          backgroundColor: AppColors.forest,
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          content: Row(children: [
            const Icon(Icons.check_circle_rounded, color: AppColors.mint),
            const SizedBox(width: 10),
            Text(s.reportSubmitted, style: const TextStyle(color: Colors.white)),
          ]),
        ));
        setState(() {
          _scoutingStarted = false;
          _sessionStart = null;
          _elapsedSeconds = 0;
          _gpsPosition = null;
          _locationDenied = false;
          selectedFarm = null;
          selectedGreenhouse = null;
          selectedVariety = null;
          findings.clear();
          findings.add(FindingData());
          _submitting = false;
          _submitted = false;
        });
        _headerAnim.reset();
        _headerAnim.forward();
      }
    } catch (e) {
      // Network failure - save to offline queue
      try {
        final user = Supabase.instance.client.auth.currentUser;
        await OfflineSyncService.saveToQueue({
          'scout_id': user?.id,
          'greenhouse_id': selectedGreenhouse!.id,
          'variety_name': selectedVariety,
          'started_at': _sessionStart?.toIso8601String(),
          'submitted_at': DateTime.now().toIso8601String(),
          'duration_seconds': _elapsedSeconds,
          'latitude': _gpsPosition?.latitude,
          'longitude': _gpsPosition?.longitude,
          'status': 'queued',
          // ignore: use_null_aware_elements
          if (trailId != null) 'trail_id': trailId,
        }, findings.where((f) => f.issue.trim().isNotEmpty).map((f) => {
          'category': f.category,
          'severity': f.severity,
          'issue': f.issue.trim(),
          // photos are local files - paths only, re-upload on drain
          'photo_paths': f.photoFiles.map((x) => x.path).toList(),
        }).toList());

        if (mounted) {
          setState(() {
            _scoutingStarted  = false;
            _sessionStart     = null;
            _elapsedSeconds   = 0;
            _gpsPosition      = null;
            _locationDenied   = false;
            selectedFarm      = null;
            selectedGreenhouse = null;
            selectedVariety   = null;
            findings.clear();
            findings.add(FindingData());
            _submitting = false;
            _submitted  = false;
          });
          _headerAnim.reset();
          _headerAnim.forward();
          _refreshQueueCount(); // update badge
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            backgroundColor: const Color(0xFFBA7517),
            behavior: SnackBarBehavior.floating,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            content: Row(children: [
              const Icon(Icons.cloud_off_rounded, color: Colors.white),
              const SizedBox(width: 10),
              Expanded(child: Text('${ref.read(stringsProvider).offlineNoConn} — ${ref.read(stringsProvider).offlineQueuedSingle}',
                  style: const TextStyle(color: Colors.white))),
            ]),
          ));
        }
      } catch (queueError) {
        if (mounted) {
          setState(() { _submitting = false; _submitted = false; });
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            content: Text('${ref.read(stringsProvider).failedToSubmit}$e'),
            backgroundColor: AppColors.critical,
          ));
        }
      }
    }
  }

  void _addFinding([String category = 'Disease']) =>
      setState(() => findings.add(FindingData(category: category)));

  void _removeFinding(int index) {
    if (findings.length == 1) return;
    setState(() => findings.removeAt(index));
  }

  @override
  Widget build(BuildContext context) {
    final farmsAsync = ref.watch(farmsProvider);
    final s = ref.watch(stringsProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: farmsAsync.when(
          loading: () => const Center(child: CircularProgressIndicator(color: AppColors.leaf, strokeWidth: 2)),
          error: (e, _) => Center(child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(mainAxisSize: MainAxisSize.min, children: [
              const Icon(Icons.error_outline_rounded, size: 40, color: AppColors.critical),
              const SizedBox(height: 16),
              Text(s.couldNotLoadFarm, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
              const SizedBox(height: 4),
              Text(e.toString(), style: const TextStyle(fontSize: 12, color: AppColors.slate), textAlign: TextAlign.center),
            ]),
          )),
          data: (farms) => LayoutBuilder(
            builder: (context, constraints) {
              final isWide = constraints.maxWidth >= 900;
              return CustomScrollView(
                slivers: [
                  SliverToBoxAdapter(
                    child: Padding(
                      padding: EdgeInsets.symmetric(horizontal: isWide ? 40 : 20, vertical: 24),
                      child: Center(
                        child: ConstrainedBox(
                          constraints: const BoxConstraints(maxWidth: 1200),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              FadeTransition(opacity: _headerFade, child: _buildHeader(isWide, s)),
                              const SizedBox(height: 28),
                              if (!_scoutingStarted)
                                _buildReadyCard(s)
                              else ...[
                                _buildSelectorRow(isWide, farms, s),
                                const SizedBox(height: 24),
                                _buildProgressCard(s),
                                const SizedBox(height: 32),
                                _buildSectionLabel(s.quickAdd),
                                const SizedBox(height: 12),
                                _buildQuickButtons(s),
                                const SizedBox(height: 32),
                                _buildSectionLabel(s.findings),
                                const SizedBox(height: 12),
                                ...List.generate(findings.length, (i) => _FindingCard(
                                  key: ValueKey(findings[i]),
                                  index: i,
                                  data: findings[i],
                                  isWide: isWide,
                                  s: s,
                                  onRemove: findings.length > 1 ? () => _removeFinding(i) : null,
                                  onChanged: () => setState(() {}),
                                )),
                                const SizedBox(height: 8),
                                _buildAddFindingButton(s),
                                const SizedBox(height: 32),
                                _buildSubmitButton(s),
                                const SizedBox(height: 40),
                              ],
                            ],
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              );
            },
          ),
        ),
      ),
    );
  }

  Widget _buildReadyCard(AppStrings s) {
    final now = DateTime.now();
    final days = s.chartLabelsWeek;
    final months = s.monthsShort;
    final dateStr = '${days[now.weekday-1]}, ${now.day} ${months[now.month-1]} ${now.year}';
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(28),
      decoration: BoxDecoration(
        color: AppColors.surface, borderRadius: BorderRadius.circular(20),
        border: Border.all(color: AppColors.divider),
        boxShadow: [BoxShadow(color: Colors.black.withValues(alpha: 0.04), blurRadius: 12, offset: const Offset(0, 4))],
      ),
      child: Column(children: [
        Container(width: 72, height: 72,
          decoration: const BoxDecoration(color: AppColors.mist, shape: BoxShape.circle),
          child: const Icon(Icons.grass_rounded, color: AppColors.forest, size: 36)),
        const SizedBox(height: 20),
        Text(s.readyToScout, style: const TextStyle(fontFamily: 'Georgia', fontSize: 22, fontWeight: FontWeight.w700, color: AppColors.ink)),
        const SizedBox(height: 8),
        Text(dateStr, style: const TextStyle(fontSize: 14, color: AppColors.slate)),
        const SizedBox(height: 8),
        Text(s.startScoutingDesc, textAlign: TextAlign.center, style: const TextStyle(fontSize: 13, color: AppColors.graphite, height: 1.5)),
        const SizedBox(height: 28),
        SizedBox(
          width: double.infinity, height: 52,
          child: ElevatedButton.icon(
            icon: const Icon(Icons.play_arrow_rounded),
            label: Text(s.startScouting, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
            onPressed: _requestLocationAndStart,
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.forest, foregroundColor: Colors.white, elevation: 0,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
            ),
          ),
        ),
      ]),
    );
  }

  Widget _buildHeader(bool isWide, AppStrings s) {
    final now = DateTime.now();
    final days = s.chartLabelsWeek;
    final months = s.monthsShort;
    final dateStr = '${days[now.weekday-1]}, ${now.day.toString().padLeft(2,"0")} ${months[now.month-1]} ${now.year}';
    return Container(
      width: double.infinity,
      decoration: BoxDecoration(
        gradient: const LinearGradient(begin: Alignment.topLeft, end: Alignment.bottomRight, colors: [AppColors.forest, AppColors.canopy, AppColors.leaf]),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [BoxShadow(color: AppColors.canopy.withValues(alpha: 0.30), blurRadius: 20, offset: const Offset(0, 8))],
      ),
      child: Stack(children: [
        Positioned(right: -30, top: -30,
          child: Container(width: 160, height: 160,
            decoration: BoxDecoration(shape: BoxShape.circle, color: Colors.white.withValues(alpha: 0.06)))),
        Padding(
          padding: EdgeInsets.all(isWide ? 36 : 24),
          child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(color: Colors.white.withValues(alpha: 0.15), borderRadius: BorderRadius.circular(20)),
                child: Text(s.scoutingInspection, style: const TextStyle(color: Colors.white70, fontSize: 11, fontWeight: FontWeight.w600, letterSpacing: 1.4))),
              const SizedBox(height: 12),
              Text(_scoutingStarted ? s.inspectionInProgress : s.newInspectionReport,
                style: TextStyle(fontFamily: 'Georgia', color: Colors.white, fontSize: isWide ? 32 : 26, fontWeight: FontWeight.w700, height: 1.15)),
              const SizedBox(height: 10),
              Text(dateStr, style: const TextStyle(color: Colors.white60, fontSize: 13)),
            ])),
            const SizedBox(width: 16),
            if (_scoutingStarted)
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                decoration: BoxDecoration(color: Colors.white.withValues(alpha: 0.15), borderRadius: BorderRadius.circular(14)),
                child: Column(children: [
                  const Icon(Icons.timer_rounded, color: Colors.white70, size: 18),
                  const SizedBox(height: 4),
                  Text(_timerLabel, style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.w700, fontFamily: 'monospace')),
                  if (_gpsPosition != null)
                    const Padding(padding: EdgeInsets.only(top: 4), child: Icon(Icons.gps_fixed_rounded, color: AppColors.mint, size: 14)),
                  if (_locationDenied)
                    const Padding(padding: EdgeInsets.only(top: 4), child: Icon(Icons.gps_off_rounded, color: Colors.white38, size: 14)),
                ]),
              )
            else
              Container(
                width: 56, height: 56,
                decoration: BoxDecoration(color: Colors.white.withValues(alpha: 0.12), borderRadius: BorderRadius.circular(16)),
                child: const Icon(Icons.eco_rounded, color: Colors.white, size: 28),
              ),
          ]),
        ),
      ]),
    );
  }

  Widget _buildSelectorRow(bool isWide, List<FarmModel> farms, AppStrings s) {
    return Wrap(spacing: 12, runSpacing: 12, children: [
      _dropdown<FarmModel>(
        label: s.farm, hint: s.selectFarm,
        value: selectedFarm, items: farms, display: (f) => f.name, enabled: true,
        onChanged: (f) => setState(() { selectedFarm = f; selectedGreenhouse = null; selectedVariety = null; }),
      ),
      _dropdown<GreenhouseModel>(
        label: s.greenhouse,
        hint: selectedFarm == null ? s.selectFarmFirst : s.selectGreenhouse,
        value: selectedGreenhouse,
        items: selectedFarm?.greenhouses.where((g) => g.isActive).toList() ?? [],
        display: (g) => g.code, enabled: selectedFarm != null,
        onChanged: (g) => setState(() { selectedGreenhouse = g; selectedVariety = null; }),
      ),
      _dropdown<String>(
        label: s.variety,
        hint: selectedGreenhouse == null ? s.selectGhFirst : s.selectVariety,
        value: selectedVariety,
        items: selectedGreenhouse?.varietyNames ?? [],
        display: (v) => v, enabled: selectedGreenhouse != null,
        onChanged: (v) => setState(() => selectedVariety = v),
      ),
    ]);
  }

  Widget _dropdown<T>({
    required String label, required String hint,
    required T? value, required List<T> items,
    required String Function(T) display,
    required bool enabled, required ValueChanged<T?> onChanged,
  }) {
    return SizedBox(width: 200, child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Padding(padding: const EdgeInsets.only(left: 2, bottom: 6),
        child: Text(label, style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w700, letterSpacing: 1.0, color: AppColors.slate))),
      Container(
        decoration: BoxDecoration(color: enabled ? AppColors.surface : AppColors.surfaceAlt, borderRadius: BorderRadius.circular(12), border: Border.all(color: AppColors.divider)),
        child: DropdownButtonHideUnderline(child: DropdownButton<T>(
          value: value,
          hint: Text(hint, style: const TextStyle(fontSize: 14, color: AppColors.slate)),
          isExpanded: true,
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 2),
          borderRadius: BorderRadius.circular(12),
          icon: const Icon(Icons.keyboard_arrow_down_rounded, color: AppColors.graphite),
          items: items.map((i) => DropdownMenuItem(value: i, child: Text(display(i), style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w500)))).toList(),
          onChanged: enabled ? onChanged : null,
        )),
      ),
    ]));
  }

  Widget _buildProgressCard(AppStrings s) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(color: AppColors.surface, borderRadius: BorderRadius.circular(16), border: Border.all(color: AppColors.divider)),
      child: Column(children: [
        Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
          Text(s.inspectionProgress, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: AppColors.ink)),
          Text('${(progress * 100).toInt()}%', style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: AppColors.leaf)),
        ]),
        const SizedBox(height: 12),
        ClipRRect(borderRadius: BorderRadius.circular(4),
          child: LinearProgressIndicator(value: progress, backgroundColor: AppColors.surfaceAlt,
            valueColor: const AlwaysStoppedAnimation(AppColors.leaf), minHeight: 6)),
        const SizedBox(height: 16),
        Row(mainAxisAlignment: MainAxisAlignment.spaceAround, children: [
          _progressStep(s.farm, selectedFarm != null),
          _progressStep(s.greenhouse, selectedGreenhouse != null),
          _progressStep(s.variety, selectedVariety != null),
          _progressStep(s.findings, findings.any((f) => f.issue.trim().isNotEmpty)),
        ]),
      ]),
    );
  }

  Widget _progressStep(String label, bool done) => Column(children: [
    Container(width: 28, height: 28,
      decoration: BoxDecoration(shape: BoxShape.circle, color: done ? AppColors.leaf : AppColors.surfaceAlt),
      child: Icon(done ? Icons.check_rounded : Icons.circle_outlined, color: done ? Colors.white : AppColors.slate, size: 16)),
    const SizedBox(height: 4),
    Text(label, style: TextStyle(fontSize: 11, color: done ? AppColors.forest : AppColors.slate, fontWeight: done ? FontWeight.w600 : FontWeight.normal)),
  ]);

  Widget _buildQuickButtons(AppStrings s) => Wrap(spacing: 8, runSpacing: 8, children: [
    _quickBtn(s.disease, Icons.coronavirus_rounded, AppColors.disease),
    _quickBtn(s.pest, Icons.bug_report_rounded, AppColors.pest),
    _quickBtn(s.waterStress, Icons.water_drop_rounded, AppColors.water),
    _quickBtn(s.nutrition, Icons.eco_rounded, AppColors.nutrition),
    _quickBtn(s.irrigation, Icons.water_rounded, AppColors.irrigation),
    _quickBtn(s.other, Icons.warning_amber_rounded, AppColors.other),
  ]);

  Widget _quickBtn(String label, IconData icon, Color color) => InkWell(
    borderRadius: BorderRadius.circular(12),
    onTap: () => _addFinding(label),
    child: Container(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
      decoration: BoxDecoration(color: color.withValues(alpha: 0.08), borderRadius: BorderRadius.circular(12), border: Border.all(color: color.withValues(alpha: 0.25))),
      child: Row(mainAxisSize: MainAxisSize.min, children: [
        Icon(icon, color: color, size: 16),
        const SizedBox(width: 6),
        Text(label, style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: color)),
        const SizedBox(width: 4),
        Icon(Icons.add_rounded, color: color, size: 14),
      ]),
    ),
  );

  Widget _buildSectionLabel(String label) => Text(label,
    style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w700, letterSpacing: 1.2, color: AppColors.slate));

  Widget _buildAddFindingButton(AppStrings s) => OutlinedButton.icon(
    icon: const Icon(Icons.add_rounded, size: 18),
    label: Text(s.addFinding),
    onPressed: _addFinding,
    style: OutlinedButton.styleFrom(
      foregroundColor: AppColors.canopy,
      side: const BorderSide(color: AppColors.divider),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
    ),
  );

  Widget _buildSubmitButton(AppStrings s) => Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      if (_queueCount > 0)
        Padding(
          padding: const EdgeInsets.only(bottom: 8),
          child: Row(children: [
            const Icon(Icons.cloud_off_rounded, size: 14, color: Color(0xFFBA7517)),
            const SizedBox(width: 6),
            Text(
              '$_queueCount report${_queueCount > 1 ? "s" : ""} queued — will sync when online',
              style: const TextStyle(fontSize: 12, color: Color(0xFFBA7517),
                  fontWeight: FontWeight.w500),
            ),
          ]),
        ),
      SizedBox(
        width: double.infinity, height: 54,
        child: ElevatedButton.icon(
          icon: _submitting
              ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
              : const Icon(Icons.check_circle_rounded),
          label: Text(_submitting ? s.submitting : s.submitReport,
            style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
          // Disabled if submitting OR already submitted (duplicate guard)
          onPressed: (_submitting || _submitted) ? null : _submitReport,
          style: ElevatedButton.styleFrom(
            backgroundColor: AppColors.forest, foregroundColor: Colors.white, elevation: 0,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
          ),
        ),
      ),
    ],
  );
}

class _FindingCard extends StatefulWidget {
  final int index;
  final FindingData data;
  final bool isWide;
  final AppStrings s;
  final VoidCallback? onRemove;
  final VoidCallback onChanged;

  const _FindingCard({
    super.key, required this.index, required this.data,
    required this.isWide, required this.s,
    required this.onRemove, required this.onChanged,
  });

  @override
  State<_FindingCard> createState() => _FindingCardState();
}

class _FindingCardState extends State<_FindingCard> {
  late TextEditingController _issueCtrl;
  final _picker = ImagePicker();
  bool _pickingPhoto = false;
  final Map<String, Uint8List> _bytesCache = {}; // prevents FutureBuilder blink

  List<String> get _categories => [
    widget.s.disease, widget.s.pest, widget.s.waterStress,
    widget.s.nutrition, widget.s.irrigation, widget.s.other,
  ];
  List<String> get _severities => [
    widget.s.low, widget.s.medium, widget.s.high, widget.s.critical,
  ];

  Color _categoryColor(String c) {
    if (c == widget.s.disease) return AppColors.disease;
    if (c == widget.s.pest) return AppColors.pest;
    if (c == widget.s.waterStress) return AppColors.water;
    if (c == widget.s.nutrition) return AppColors.nutrition;
    if (c == widget.s.irrigation) return AppColors.irrigation;
    return AppColors.other;
  }

  @override
  void initState() {
    super.initState();
    _issueCtrl = TextEditingController(text: widget.data.issue);
  }

  Future<void> _pickPhoto(ImageSource source) async {
    if (_pickingPhoto) return;
    setState(() => _pickingPhoto = true);
    try {
      final file = await _picker.pickImage(source: source, imageQuality: 80, maxWidth: 1920);
      if (file != null) {
        final bytes = await file.readAsBytes();
        _bytesCache[file.name] = bytes;
        setState(() => widget.data.photoFiles.add(file));
        widget.onChanged();
      }
    } catch (e) {
      debugPrint('[photos] pick failed: \$e');
    } finally {
      if (mounted) setState(() => _pickingPhoto = false);
    }
  }

  void _removePhoto(int index) {
    final file = widget.data.photoFiles[index];
    _bytesCache.remove(file.name);
    setState(() => widget.data.photoFiles.removeAt(index));
    widget.onChanged();
  }

  Widget _buildPhotoRow() {
    final photos = widget.data.photoFiles;
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      const SizedBox(height: 14),
      Row(children: [
        const Icon(Icons.photo_camera_rounded, size: 14, color: Color(0xFF6B7F6E)),
        const SizedBox(width: 6),
        Text('Photos (${photos.length}/5)',
            style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600,
                color: Color(0xFF6B7F6E), letterSpacing: 0.5)),
        const Spacer(),
        if (photos.length < 5) ...[
          GestureDetector(
              onTap: () => _pickPhoto(ImageSource.camera),
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                decoration: BoxDecoration(
                  color: AppColors.canopy.withValues(alpha: 0.08),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: AppColors.canopy.withValues(alpha: 0.2)),
                ),
                child: Row(mainAxisSize: MainAxisSize.min, children: [
                  const Icon(Icons.camera_alt_rounded, size: 14, color: Color(0xFF2D6A4F)),
                  const SizedBox(width: 4),
                  const Text('Camera', style: TextStyle(fontSize: 11,
                      color: Color(0xFF2D6A4F), fontWeight: FontWeight.w600)),
                ]),
              ),
            ),
          const SizedBox(width: 8),
          GestureDetector(
            onTap: () => _pickPhoto(ImageSource.gallery),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
              decoration: BoxDecoration(
                color: AppColors.canopy.withValues(alpha: 0.08),
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: AppColors.canopy.withValues(alpha: 0.2)),
              ),
              child: Row(mainAxisSize: MainAxisSize.min, children: [
                const Icon(Icons.photo_library_rounded, size: 14, color: Color(0xFF2D6A4F)),
                const SizedBox(width: 4),
                const Text('Gallery', style: TextStyle(fontSize: 11,
                    color: Color(0xFF2D6A4F), fontWeight: FontWeight.w600)),
              ]),
            ),
          ),
        ],
      ]),
      if (photos.isNotEmpty) ...[
        const SizedBox(height: 10),
        SizedBox(
          height: 80,
          child: ListView.separated(
            scrollDirection: Axis.horizontal,
            itemCount: photos.length,
            separatorBuilder: (_, _) => const SizedBox(width: 8),
            itemBuilder: (context, i) => Stack(children: [
              ClipRRect(
                borderRadius: BorderRadius.circular(8),
                child: Builder(builder: (context) {
                  final bytes = _bytesCache[photos[i].name];
                  if (bytes == null) { return Container(
                    width: 80, height: 80,
                    decoration: BoxDecoration(
                      color: AppColors.surfaceAlt,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Icon(Icons.image_rounded, color: Color(0xFF6B7F6E)),
                  ); }
                  return Image.memory(bytes,
                      width: 80, height: 80, fit: BoxFit.cover);
                }),
              ),
              Positioned(top: 2, right: 2,
                child: GestureDetector(
                  onTap: () => _removePhoto(i),
                  child: Container(
                    width: 20, height: 20,
                    decoration: const BoxDecoration(
                        color: Color(0xFFD32F2F), shape: BoxShape.circle),
                    child: const Icon(Icons.close_rounded, size: 12, color: Colors.white),
                  ),
                ),
              ),
            ]),
          ),
        ),
      ],
    ]);
  }

  @override
  void dispose() { _issueCtrl.dispose(); super.dispose(); }

  @override
  Widget build(BuildContext context) {
    final color = _categoryColor(widget.data.category);
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: Colors.white, borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.divider),
        boxShadow: [BoxShadow(color: Colors.black.withValues(alpha: 0.03), blurRadius: 8, offset: const Offset(0, 2))],
      ),
      child: Column(children: [
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          decoration: BoxDecoration(
            color: color.withValues(alpha: 0.06),
            borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
            border: Border(bottom: BorderSide(color: color.withValues(alpha: 0.15))),
          ),
          child: Row(children: [
            Container(width: 8, height: 8, decoration: BoxDecoration(shape: BoxShape.circle, color: color)),
            const SizedBox(width: 8),
            Text('${widget.s.findingLabel} ${widget.index + 1}', style: TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: color)),
            const Spacer(),
            if (widget.onRemove != null)
              GestureDetector(onTap: widget.onRemove, child: Icon(Icons.close_rounded, size: 18, color: Colors.grey[400])),
          ]),
        ),
        Padding(
          padding: const EdgeInsets.all(16),
          child: Column(children: [
            Row(children: [
              Expanded(child: _labeledDropdown(widget.s.category, widget.data.category, _categories, (v) {
                setState(() => widget.data.category = v!);
                widget.onChanged();
              })),
              const SizedBox(width: 12),
              Expanded(child: _labeledDropdown(widget.s.severity, widget.data.severity, _severities, (v) {
                setState(() => widget.data.severity = v!);
                widget.onChanged();
              })),
            ]),
            const SizedBox(height: 14),
            _labeledField(widget.s.issueObservation, _issueCtrl, hint: widget.s.describeObserved, (v) {
              widget.data.issue = v;
              widget.onChanged();
            }),
            _buildPhotoRow(),
          ]),
        ),
      ]),
    );
  }

  Widget _labeledDropdown(String label, String value, List<String> items, ValueChanged<String?> onChanged) =>
    Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Padding(padding: const EdgeInsets.only(left: 2, bottom: 6),
        child: Text(label, style: const TextStyle(fontSize: 10, fontWeight: FontWeight.w700, letterSpacing: 1.0, color: Color(0xFF6B7F6E)))),
      Container(
        decoration: BoxDecoration(color: AppColors.background, borderRadius: BorderRadius.circular(10), border: Border.all(color: AppColors.divider)),
        child: DropdownButtonHideUnderline(child: DropdownButton<String>(
          value: items.contains(value) ? value : items.first,
          isExpanded: true,
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 2),
          borderRadius: BorderRadius.circular(10),
          icon: const Icon(Icons.keyboard_arrow_down_rounded, color: Color(0xFF3D4F42), size: 18),
          items: items.map((i) => DropdownMenuItem(value: i, child: Text(i, style: const TextStyle(fontSize: 13)))).toList(),
          onChanged: onChanged,
        )),
      ),
    ]);

  Widget _labeledField(String label, TextEditingController ctrl, ValueChanged<String> onChanged, {String hint = ''}) =>
    Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Padding(padding: const EdgeInsets.only(left: 2, bottom: 6),
        child: Text(label, style: const TextStyle(fontSize: 10, fontWeight: FontWeight.w700, letterSpacing: 1.0, color: Color(0xFF6B7F6E)))),
      Container(
        decoration: BoxDecoration(color: AppColors.background, borderRadius: BorderRadius.circular(10), border: Border.all(color: AppColors.divider)),
        child: TextField(
          controller: ctrl, onChanged: onChanged,
          style: const TextStyle(fontSize: 13, color: Color(0xFF0D1B0F)),
          decoration: InputDecoration(
            hintText: hint, hintStyle: const TextStyle(color: Color(0xFF6B7F6E), fontSize: 13),
            border: InputBorder.none, contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
          ),
        ),
      ),
    ]);
}

