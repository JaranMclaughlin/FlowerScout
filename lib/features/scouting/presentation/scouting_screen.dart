import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:geolocator/geolocator.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../../../shared/providers/farm_providers.dart';
import '../../../shared/providers/farm_repository.dart';

// ── Finding model ─────────────────────────────────────────────────────────
class FindingData {
  String category;
  String severity;
  String issue;
  FindingData({
    this.category = 'Disease',
    this.severity = 'Medium',
    this.issue = '',
  });
}

// ── Design tokens ─────────────────────────────────────────────────────────
class _C {
  static const forest   = Color(0xFF1B4332);
  static const canopy   = Color(0xFF2D6A4F);
  static const leaf     = Color(0xFF40916C);
  static const mint     = Color(0xFF74C69D);
  static const mist     = Color(0xFFD8F3DC);
  static const cream    = Color(0xFFF8FAF8);
  static const paper    = Color(0xFFFFFFFF);
  static const ink      = Color(0xFF0D1B0F);
  static const graphite = Color(0xFF3D4F42);
  static const slate    = Color(0xFF6B7F6E);
  static const fog      = Color(0xFFEAEFEA);
  static const divider  = Color(0xFFDDE5DD);
  static const disease  = Color(0xFFD32F2F);
  static const pest     = Color(0xFFE65100);
  static const water    = Color(0xFF0277BD);
  static const nutrition= Color(0xFF388E3C);
  static const irrigation=Color(0xFF00838F);
  static const other    = Color(0xFF455A64);
  static const high     = Color(0xFFEF6C00);
  static const critical = Color(0xFFD32F2F);
}

// ── Main screen ───────────────────────────────────────────────────────────
class ScoutingScreen extends ConsumerStatefulWidget {
  const ScoutingScreen({super.key});
  @override
  ConsumerState<ScoutingScreen> createState() => _ScoutingScreenState();
}

class _ScoutingScreenState extends ConsumerState<ScoutingScreen>
    with TickerProviderStateMixin {

  // Session state
  bool _scoutingStarted = false;
  DateTime? _sessionStart;
  Timer? _timer;
  int _elapsedSeconds = 0;
  Position? _gpsPosition;
  bool _locationDenied = false;

  // Form state
  FarmModel? selectedFarm;
  GreenhouseModel? selectedGreenhouse;
  String? selectedVariety;
  final List<FindingData> findings = [FindingData()];
  bool _submitting = false;

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
    _headerAnim = AnimationController(
        vsync: this, duration: const Duration(milliseconds: 800));
    _headerFade = CurvedAnimation(parent: _headerAnim, curve: Curves.easeOut);
    _headerAnim.forward();
  }

  @override
  void dispose() {
    _headerAnim.dispose();
    _timer?.cancel();
    super.dispose();
  }

  // ── Location ────────────────────────────────────────────────────────────
  Future<void> _requestLocationAndStart() async {
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      _showLocationDialog(
        title: 'Location services off',
        message: 'Please enable location services to geo-tag your inspections.',
        showSettings: true,
      );
      _startSession(withLocation: false);
      return;
    }

    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
    }

    if (permission == LocationPermission.deniedForever) {
      if (mounted) {
        _showLocationDialog(
          title: 'Location permission required',
          message: 'Location access is denied. Findings will not be geo-tagged. You can enable it in app settings.',
          showSettings: true,
        );
      }
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
        locationSettings: const LocationSettings(
          accuracy: LocationAccuracy.high,
          timeLimit: Duration(seconds: 10),
        ),
      );
      setState(() => _gpsPosition = pos);
    } catch (_) {}

    _startSession(withLocation: true);
  }

  void _startSession({required bool withLocation}) {
    setState(() {
      _scoutingStarted = true;
      _sessionStart = DateTime.now();
      _elapsedSeconds = 0;
    });
    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      if (mounted) setState(() => _elapsedSeconds++);
    });
  }

  void _showLocationDialog({
    required String title,
    required String message,
    bool showSettings = false,
  }) {
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: Text(title, style: const TextStyle(
            fontFamily: 'Georgia', fontSize: 17)),
        content: Text(message, style: const TextStyle(fontSize: 13)),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Continue anyway'),
          ),
          if (showSettings)
            TextButton(
              onPressed: () {
                Navigator.pop(context);
                Geolocator.openAppSettings();
              },
              child: const Text('Open settings'),
            ),
        ],
      ),
    );
  }

  // ── Submit ───────────────────────────────────────────────────────────────
  Future<void> _submitReport() async {
    if (selectedFarm == null || selectedGreenhouse == null || selectedVariety == null) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
        content: Text('Please select Farm, Greenhouse and Variety'),
        backgroundColor: _C.high,
      ));
      return;
    }
    if (!findings.any((f) => f.issue.trim().isNotEmpty)) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
        content: Text('Please add at least one finding'),
        backgroundColor: _C.high,
      ));
      return;
    }

    setState(() => _submitting = true);
    _timer?.cancel();

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
          })
          .select('id')
          .single();

      for (final finding in findings.where((f) => f.issue.trim().isNotEmpty)) {
        await Supabase.instance.client.from('inspection_findings').insert({
          'report_id': reportId['id'],
          'category': finding.category,
          'severity': finding.severity,
          'issue': finding.issue.trim(),
        });
      }

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          backgroundColor: _C.forest,
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          content: Row(children: const [
            Icon(Icons.check_circle_rounded, color: _C.mint),
            SizedBox(width: 10),
            Text('Report submitted successfully!',
                style: TextStyle(color: Colors.white)),
          ]),
        ));
        // Reset session
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
        });
        _headerAnim.reset();
        _headerAnim.forward();
      }
    } catch (e) {
      if (mounted) {
        setState(() => _submitting = false);
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text('Failed to submit: $e'),
          backgroundColor: _C.critical,
        ));
      }
    }
  }

  void _addFinding([String category = 'Disease']) =>
      setState(() => findings.add(FindingData(category: category)));

  void _removeFinding(int index) {
    if (findings.length == 1) return;
    setState(() => findings.removeAt(index));
  }

  // ── Build ────────────────────────────────────────────────────────────────
  @override
  Widget build(BuildContext context) {
    final farmsAsync = ref.watch(farmsProvider);

    return Scaffold(
      backgroundColor: _C.cream,
      body: SafeArea(
        child: farmsAsync.when(
          loading: () => const Center(child: CircularProgressIndicator(
              color: _C.leaf, strokeWidth: 2)),
          error: (e, _) => Center(child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(mainAxisSize: MainAxisSize.min, children: [
              const Icon(Icons.error_outline_rounded,
                  size: 40, color: _C.critical),
              const SizedBox(height: 16),
              const Text('Could not load farm data',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
              const SizedBox(height: 4),
              Text(e.toString(),
                  style: const TextStyle(fontSize: 12, color: _C.slate),
                  textAlign: TextAlign.center),
            ]),
          )),
          data: (farms) => LayoutBuilder(
            builder: (context, constraints) {
              final isWide = constraints.maxWidth >= 900;
              return CustomScrollView(
                slivers: [
                  SliverToBoxAdapter(
                    child: Padding(
                      padding: EdgeInsets.symmetric(
                          horizontal: isWide ? 40 : 20, vertical: 24),
                      child: Center(
                        child: ConstrainedBox(
                          constraints: const BoxConstraints(maxWidth: 1200),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              FadeTransition(
                                opacity: _headerFade,
                                child: _buildHeader(isWide),
                              ),
                              const SizedBox(height: 28),
                              if (!_scoutingStarted)
                                _buildReadyCard()
                              else ...[
                                _buildSelectorRow(isWide, farms),
                                const SizedBox(height: 24),
                                _buildProgressCard(),
                                const SizedBox(height: 32),
                                _buildSectionLabel('QUICK ADD'),
                                const SizedBox(height: 12),
                                _buildQuickButtons(),
                                const SizedBox(height: 32),
                                _buildSectionLabel('FINDINGS'),
                                const SizedBox(height: 12),
                                ...List.generate(findings.length, (i) =>
                                  _FindingCard(
                                    key: ValueKey(findings[i]),
                                    index: i,
                                    data: findings[i],
                                    isWide: isWide,
                                    onRemove: findings.length > 1
                                        ? () => _removeFinding(i) : null,
                                    onChanged: () => setState(() {}),
                                  ),
                                ),
                                const SizedBox(height: 8),
                                _buildAddFindingButton(),
                                const SizedBox(height: 32),
                                _buildSubmitButton(),
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

  // ── Ready card ───────────────────────────────────────────────────────────
  Widget _buildReadyCard() {
    final now = DateTime.now();
    final days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
    final months = ['Jan','Feb','Mar','Apr','May','Jun',
                    'Jul','Aug','Sep','Oct','Nov','Dec'];
    final dateStr =
        '${days[now.weekday-1]}, ${now.day} ${months[now.month-1]} ${now.year}';

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(28),
      decoration: BoxDecoration(
        color: _C.paper,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: _C.divider),
        boxShadow: [BoxShadow(
            color: Colors.black.withValues(alpha: 0.04),
            blurRadius: 12, offset: const Offset(0, 4))],
      ),
      child: Column(children: [
        Container(
          width: 72, height: 72,
          decoration: BoxDecoration(
            color: _C.mist,
            shape: BoxShape.circle,
          ),
          child: const Icon(Icons.grass_rounded, color: _C.forest, size: 36),
        ),
        const SizedBox(height: 20),
        const Text('Ready to Scout?', style: TextStyle(
            fontFamily: 'Georgia', fontSize: 22,
            fontWeight: FontWeight.w700, color: _C.ink)),
        const SizedBox(height: 8),
        Text(dateStr, style: const TextStyle(fontSize: 14, color: _C.slate)),
        const SizedBox(height: 8),
        const Text(
          'Tap Start Scouting to begin your inspection.\nYour location will be captured to geo-tag findings.',
          textAlign: TextAlign.center,
          style: TextStyle(fontSize: 13, color: _C.graphite, height: 1.5),
        ),
        const SizedBox(height: 28),
        SizedBox(
          width: double.infinity,
          height: 52,
          child: ElevatedButton.icon(
            icon: const Icon(Icons.play_arrow_rounded),
            label: const Text('Start Scouting',
                style: TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
            onPressed: _requestLocationAndStart,
            style: ElevatedButton.styleFrom(
              backgroundColor: _C.forest,
              foregroundColor: Colors.white,
              elevation: 0,
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(14)),
            ),
          ),
        ),
      ]),
    );
  }

  // ── Header ───────────────────────────────────────────────────────────────
  Widget _buildHeader(bool isWide) {
    final now = DateTime.now();
    final days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
    final months = ['Jan','Feb','Mar','Apr','May','Jun',
                    'Jul','Aug','Sep','Oct','Nov','Dec'];
    final dateStr =
        '${days[now.weekday-1]}, ${now.day.toString().padLeft(2,"0")} ${months[now.month-1]} ${now.year}';

    return Container(
      width: double.infinity,
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          begin: Alignment.topLeft, end: Alignment.bottomRight,
          colors: [_C.forest, _C.canopy, _C.leaf],
        ),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [BoxShadow(
            color: _C.canopy.withValues(alpha: 0.30),
            blurRadius: 20, offset: const Offset(0, 8))],
      ),
      child: Stack(children: [
        Positioned(right: -30, top: -30,
          child: Container(width: 160, height: 160,
            decoration: BoxDecoration(shape: BoxShape.circle,
              color: Colors.white.withValues(alpha: 0.06)))),
        Padding(
          padding: EdgeInsets.all(isWide ? 36 : 24),
          child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Expanded(child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: Colors.white.withValues(alpha: 0.15),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: const Text('SCOUTING INSPECTION',
                    style: TextStyle(color: Colors.white70, fontSize: 11,
                        fontWeight: FontWeight.w600, letterSpacing: 1.4)),
                ),
                const SizedBox(height: 12),
                Text(_scoutingStarted ? 'Inspection In\nProgress' : 'New Inspection\nReport',
                  style: TextStyle(fontFamily: 'Georgia', color: Colors.white,
                      fontSize: isWide ? 32 : 26,
                      fontWeight: FontWeight.w700, height: 1.15)),
                const SizedBox(height: 10),
                Text(dateStr,
                    style: const TextStyle(color: Colors.white60, fontSize: 13)),
              ],
            )),
            const SizedBox(width: 16),
            if (_scoutingStarted)
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(14),
                ),
                child: Column(children: [
                  const Icon(Icons.timer_rounded, color: Colors.white70, size: 18),
                  const SizedBox(height: 4),
                  Text(_timerLabel, style: const TextStyle(
                      color: Colors.white, fontSize: 16,
                      fontWeight: FontWeight.w700, fontFamily: 'monospace')),
                  if (_gpsPosition != null)
                    const Padding(
                      padding: EdgeInsets.only(top: 4),
                      child: Icon(Icons.gps_fixed_rounded,
                          color: _C.mint, size: 14),
                    ),
                  if (_locationDenied)
                    const Padding(
                      padding: EdgeInsets.only(top: 4),
                      child: Icon(Icons.gps_off_rounded,
                          color: Colors.white38, size: 14),
                    ),
                ]),
              )
            else
              Container(
                width: 56, height: 56,
                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.12),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: const Icon(Icons.eco_rounded, color: Colors.white, size: 28),
              ),
          ]),
        ),
      ]),
    );
  }

  // ── Selectors ─────────────────────────────────────────────────────────────
  Widget _buildSelectorRow(bool isWide, List<FarmModel> farms) {
    return Wrap(spacing: 12, runSpacing: 12, children: [
      _dropdown<FarmModel>(
        label: 'FARM', hint: 'Select farm',
        value: selectedFarm, items: farms,
        display: (f) => f.name, enabled: true,
        onChanged: (f) => setState(() {
          selectedFarm = f;
          selectedGreenhouse = null;
          selectedVariety = null;
        }),
      ),
      _dropdown<GreenhouseModel>(
        label: 'GREENHOUSE',
        hint: selectedFarm == null ? 'Select farm first' : 'Select greenhouse',
        value: selectedGreenhouse,
        items: selectedFarm?.greenhouses.where((g) => g.isActive).toList() ?? [],
        display: (g) => g.code,
        enabled: selectedFarm != null,
        onChanged: (g) => setState(() {
          selectedGreenhouse = g;
          selectedVariety = null;
        }),
      ),
      _dropdown<String>(
        label: 'VARIETY',
        hint: selectedGreenhouse == null ? 'Select GH first' : 'Select variety',
        value: selectedVariety,
        items: selectedGreenhouse?.varietyNames ?? [],
        display: (v) => v,
        enabled: selectedGreenhouse != null,
        onChanged: (v) => setState(() => selectedVariety = v),
      ),
    ]);
  }

  Widget _dropdown<T>({
    required String label,
    required String hint,
    required T? value,
    required List<T> items,
    required String Function(T) display,
    required bool enabled,
    required ValueChanged<T?> onChanged,
  }) {
    return SizedBox(width: 200, child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(padding: const EdgeInsets.only(left: 2, bottom: 6),
          child: Text(label, style: const TextStyle(fontSize: 11,
              fontWeight: FontWeight.w700, letterSpacing: 1.0, color: _C.slate))),
        Container(
          decoration: BoxDecoration(
            color: enabled ? _C.paper : _C.fog,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: _C.divider),
          ),
          child: DropdownButtonHideUnderline(child: DropdownButton<T>(
            value: value,
            hint: Text(hint, style: const TextStyle(fontSize: 14, color: _C.slate)),
            isExpanded: true,
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 2),
            borderRadius: BorderRadius.circular(12),
            icon: const Icon(Icons.keyboard_arrow_down_rounded, color: _C.graphite),
            items: items.map((i) => DropdownMenuItem(
              value: i,
              child: Text(display(i), style: const TextStyle(
                  fontSize: 14, fontWeight: FontWeight.w500)))).toList(),
            onChanged: enabled ? onChanged : null,
          )),
        ),
      ],
    ));
  }

  // ── Progress ─────────────────────────────────────────────────────────────
  Widget _buildProgressCard() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(color: _C.paper,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: _C.divider)),
      child: Column(children: [
        Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
          const Text('Inspection Progress', style: TextStyle(
              fontSize: 14, fontWeight: FontWeight.w600, color: _C.ink)),
          Text('${(progress * 100).toInt()}%', style: const TextStyle(
              fontSize: 13, fontWeight: FontWeight.w700, color: _C.leaf)),
        ]),
        const SizedBox(height: 12),
        ClipRRect(
          borderRadius: BorderRadius.circular(4),
          child: LinearProgressIndicator(
            value: progress,
            backgroundColor: _C.fog,
            valueColor: const AlwaysStoppedAnimation(_C.leaf),
            minHeight: 6,
          ),
        ),
        const SizedBox(height: 16),
        Row(mainAxisAlignment: MainAxisAlignment.spaceAround, children: [
          _progressStep('Farm', selectedFarm != null),
          _progressStep('Greenhouse', selectedGreenhouse != null),
          _progressStep('Variety', selectedVariety != null),
          _progressStep('Findings',
              findings.any((f) => f.issue.trim().isNotEmpty)),
        ]),
      ]),
    );
  }

  Widget _progressStep(String label, bool done) => Column(children: [
    Container(width: 28, height: 28,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        color: done ? _C.leaf : _C.fog,
      ),
      child: Icon(done ? Icons.check_rounded : Icons.circle_outlined,
          color: done ? Colors.white : _C.slate, size: 16)),
    const SizedBox(height: 4),
    Text(label, style: TextStyle(fontSize: 11,
        color: done ? _C.forest : _C.slate,
        fontWeight: done ? FontWeight.w600 : FontWeight.normal)),
  ]);

  // ── Quick add ─────────────────────────────────────────────────────────────
  Widget _buildQuickButtons() => Wrap(spacing: 8, runSpacing: 8, children: [
    _quickBtn('Disease', Icons.coronavirus_rounded, _C.disease),
    _quickBtn('Pest', Icons.bug_report_rounded, _C.pest),
    _quickBtn('Water Stress', Icons.water_drop_rounded, _C.water),
    _quickBtn('Nutrition', Icons.eco_rounded, _C.nutrition),
    _quickBtn('Irrigation', Icons.water_rounded, _C.irrigation),
    _quickBtn('Other', Icons.warning_amber_rounded, _C.other),
  ]);

  Widget _quickBtn(String label, IconData icon, Color color) =>
    InkWell(
      borderRadius: BorderRadius.circular(12),
      onTap: () => _addFinding(label),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
        decoration: BoxDecoration(
          color: color.withValues(alpha: 0.08),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: color.withValues(alpha: 0.25)),
        ),
        child: Row(mainAxisSize: MainAxisSize.min, children: [
          Icon(icon, color: color, size: 16),
          const SizedBox(width: 6),
          Text(label, style: TextStyle(fontSize: 13,
              fontWeight: FontWeight.w600, color: color)),
          const SizedBox(width: 4),
          Icon(Icons.add_rounded, color: color, size: 14),
        ]),
      ),
    );

  // ── Section label ─────────────────────────────────────────────────────────
  Widget _buildSectionLabel(String label) => Text(label,
    style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w700,
        letterSpacing: 1.2, color: _C.slate));

  // ── Add finding ───────────────────────────────────────────────────────────
  Widget _buildAddFindingButton() => OutlinedButton.icon(
    icon: const Icon(Icons.add_rounded, size: 18),
    label: const Text('Add finding'),
    onPressed: _addFinding,
    style: OutlinedButton.styleFrom(
      foregroundColor: _C.canopy,
      side: const BorderSide(color: _C.divider),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
    ),
  );

    // ── Submit ────────────────────────────────────────────────────────────────
  Widget _buildSubmitButton() => SizedBox(
    width: double.infinity, height: 54,
    child: ElevatedButton.icon(
      icon: _submitting
          ? const SizedBox(width: 20, height: 20,
              child: CircularProgressIndicator(
                  color: Colors.white, strokeWidth: 2))
          : const Icon(Icons.check_circle_rounded),
      label: Text(_submitting ? 'Submitting...' : 'Submit Report',
          style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
      onPressed: _submitting ? null : _submitReport,
      style: ElevatedButton.styleFrom(
        backgroundColor: _C.forest,
        foregroundColor: Colors.white,
        elevation: 0,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      ),
    ),
  );
}

// ── Finding card ──────────────────────────────────────────────────────────
class _FindingCard extends StatefulWidget {
  final int index;
  final FindingData data;
  final bool isWide;
  final VoidCallback? onRemove;
  final VoidCallback onChanged;

  const _FindingCard({
    super.key,
    required this.index,
    required this.data,
    required this.isWide,
    required this.onRemove,
    required this.onChanged,
  });

  @override
  State<_FindingCard> createState() => _FindingCardState();
}

class _FindingCardState extends State<_FindingCard> {
  late TextEditingController _issueCtrl;

  static const _categories = [
    'Disease','Pest','Water Stress','Nutrition','Irrigation','Other'];
  static const _severities = ['Low','Medium','High','Critical'];

  Color _categoryColor(String c) => switch(c) {
    'Disease'      => const Color(0xFFD32F2F),
    'Pest'         => const Color(0xFFE65100),
    'Water Stress' => const Color(0xFF0277BD),
    'Nutrition'    => const Color(0xFF388E3C),
    'Irrigation'   => const Color(0xFF00838F),
    _              => const Color(0xFF455A64),
  };

  @override
  void initState() {
    super.initState();
    _issueCtrl = TextEditingController(text: widget.data.issue);
  }

  @override
  void dispose() {
    _issueCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final color = _categoryColor(widget.data.category);
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: const Color(0xFFFFFFFF),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: const Color(0xFFDDE5DD)),
        boxShadow: [BoxShadow(
            color: Colors.black.withValues(alpha: 0.03),
            blurRadius: 8, offset: const Offset(0, 2))],
      ),
      child: Column(children: [
        // Header
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          decoration: BoxDecoration(
            color: color.withValues(alpha: 0.06),
            borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
            border: Border(bottom: BorderSide(color: color.withValues(alpha: 0.15))),
          ),
          child: Row(children: [
            Container(width: 8, height: 8,
                decoration: BoxDecoration(shape: BoxShape.circle, color: color)),
            const SizedBox(width: 8),
            Text('Finding ${widget.index + 1}',
                style: TextStyle(fontSize: 13,
                    fontWeight: FontWeight.w700, color: color)),
            const Spacer(),
            if (widget.onRemove != null)
              GestureDetector(
                onTap: widget.onRemove,
                child: Icon(Icons.close_rounded,
                    size: 18, color: Colors.grey[400]),
              ),
          ]),
        ),
        // Body
        Padding(
          padding: const EdgeInsets.all(16),
          child: Column(children: [
            // Category + Severity
            Row(children: [
              Expanded(child: _labeledDropdown('CATEGORY',
                widget.data.category, _categories, (v) {
                  setState(() => widget.data.category = v!);
                  widget.onChanged();
                })),
              const SizedBox(width: 12),
              Expanded(child: _labeledDropdown('SEVERITY',
                widget.data.severity, _severities, (v) {
                  setState(() => widget.data.severity = v!);
                  widget.onChanged();
                })),
            ]),
            const SizedBox(height: 14),
            // Issue
            _labeledField('ISSUE / OBSERVATION', _issueCtrl,
              hint: 'Describe what you observed...', (v) {
                widget.data.issue = v;
                widget.onChanged();
              }),
            const SizedBox(height: 14),
          ]),
        ),
      ]),
    );
  }

  Widget _labeledDropdown(String label, String value,
      List<String> items, ValueChanged<String?> onChanged) =>
    Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Padding(padding: const EdgeInsets.only(left: 2, bottom: 6),
        child: Text(label, style: const TextStyle(fontSize: 10,
            fontWeight: FontWeight.w700, letterSpacing: 1.0,
            color: Color(0xFF6B7F6E)))),
      Container(
        decoration: BoxDecoration(color: const Color(0xFFF8FAF8),
            borderRadius: BorderRadius.circular(10),
            border: Border.all(color: const Color(0xFFDDE5DD))),
        child: DropdownButtonHideUnderline(child: DropdownButton<String>(
          value: value, isExpanded: true,
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 2),
          borderRadius: BorderRadius.circular(10),
          icon: const Icon(Icons.keyboard_arrow_down_rounded,
              color: Color(0xFF3D4F42), size: 18),
          items: items.map((i) => DropdownMenuItem(value: i,
            child: Text(i, style: const TextStyle(fontSize: 13)))).toList(),
          onChanged: onChanged,
        )),
      ),
    ]);

  Widget _labeledField(String label, TextEditingController ctrl,
      ValueChanged<String> onChanged, {
      String hint = '', TextInputType keyboardType = TextInputType.text}) =>
    Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Padding(padding: const EdgeInsets.only(left: 2, bottom: 6),
        child: Text(label, style: const TextStyle(fontSize: 10,
            fontWeight: FontWeight.w700, letterSpacing: 1.0,
            color: Color(0xFF6B7F6E)))),
      Container(
        decoration: BoxDecoration(color: const Color(0xFFF8FAF8),
            borderRadius: BorderRadius.circular(10),
            border: Border.all(color: const Color(0xFFDDE5DD))),
        child: TextField(
          controller: ctrl,
          keyboardType: keyboardType,
          onChanged: onChanged,
          style: const TextStyle(fontSize: 13, color: Color(0xFF0D1B0F)),
          decoration: InputDecoration(
            hintText: hint,
            hintStyle: const TextStyle(color: Color(0xFF6B7F6E), fontSize: 13),
            border: InputBorder.none,
            contentPadding: const EdgeInsets.symmetric(
                horizontal: 12, vertical: 10),
          ),
        ),
      ),
    ]);
}
