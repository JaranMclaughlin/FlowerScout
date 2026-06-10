import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

//  Design tokens
class AppColors {
  static const forest = Color(0xFF1B4332);
  static const canopy = Color(0xFF2D6A4F);
  static const leaf = Color(0xFF40916C);
  static const mint = Color(0xFF74C69D);
  static const mist = Color(0xFFD8F3DC);
  static const cream = Color(0xFFF8FAF8);
  static const paper = Color(0xFFFFFFFF);
  static const ink = Color(0xFF0D1B0F);
  static const graphite = Color(0xFF3D4F42);
  static const slate = Color(0xFF6B7F6E);
  static const fog = Color(0xFFEAEFEA);
  static const divider = Color(0xFFDDE5DD);

  // Severity
  static const low = Color(0xFF4CAF50);
  static const medium = Color(0xFFF59E0B);
  static const high = Color(0xFFEF6C00);
  static const critical = Color(0xFFD32F2F);

  // Category accents
  static const disease = Color(0xFFD32F2F);
  static const pest = Color(0xFFE65100);
  static const water = Color(0xFF0277BD);
  static const nutrition = Color(0xFF388E3C);
  static const irrigation = Color(0xFF00838F);
  static const environmental = Color(0xFF6A1B9A);
  static const other = Color(0xFF455A64);
}

class AppText {
  // Use Google Fonts or system serif for elegance
  static const displayStyle = TextStyle(
    fontFamily: 'Georgia',
    fontSize: 28,
    fontWeight: FontWeight.w700,
    color: AppColors.ink,
    letterSpacing: -0.5,
    height: 1.2,
  );
  static const headingStyle = TextStyle(
    fontFamily: 'Georgia',
    fontSize: 20,
    fontWeight: FontWeight.w600,
    color: AppColors.ink,
    letterSpacing: -0.3,
  );
  static const labelStyle = TextStyle(
    fontSize: 12,
    fontWeight: FontWeight.w600,
    color: AppColors.slate,
    letterSpacing: 1.0,
  );
  static const bodyStyle = TextStyle(
    fontSize: 14,
    color: AppColors.graphite,
    height: 1.5,
  );
}

//  Data models
class FindingData {
  String category;
  String severity;
  String issue;
  double? affectedArea;
  String notes;

  FindingData({
    this.category = 'Disease',
    this.severity = 'Medium',
    this.issue = '',
    this.affectedArea,
    this.notes = '',
  });
}

//  Main screen
class ScoutingScreen extends StatefulWidget {
  const ScoutingScreen({super.key});

  @override
  State<ScoutingScreen> createState() => _ScoutingScreenState();
}

class _ScoutingScreenState extends State<ScoutingScreen>
    with TickerProviderStateMixin {
  final Map<String, Map<String, List<String>>> farmData = {
    'Kongoni River Farm': {
      'GH-01': ['Athena', 'Moonwalk'],
      'GH-02': ['Madam Red'],
      'GH-03': ['Explorer'],
      'GH-12': ['Athena', 'Madam Red'],
      'GH-25': ['White Dove'],
    },
    'Main Farm': {
      'GH-11': ['Athena'],
      'GH-12': ['Moonwalk'],
      'GH-13': ['Madam Red'],
    },
    'North Farm': {
      'GH-21': ['Explorer'],
      'GH-22': ['White Dove'],
    },
  };

  String? selectedFarm;
  String? selectedGreenhouse;
  String? selectedVariety;
  List<String> availableGreenhouses = [];
  List<String> availableVarieties = [];

  final List<FindingData> findings = [FindingData()];
  final TextEditingController generalNotesController = TextEditingController();

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

  int get progressPercent => (progress * 100).toInt();

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
    generalNotesController.dispose();
    super.dispose();
  }

  void _addFinding([String category = 'Disease']) {
    setState(() => findings.add(FindingData(category: category)));
  }

  void _removeFinding(int index) {
    if (findings.length == 1) return;
    setState(() => findings.removeAt(index));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.cream,
      body: SafeArea(
        child: LayoutBuilder(
          builder: (context, constraints) {
            final isWide = constraints.maxWidth >= 900;
            return CustomScrollView(
              slivers: [
                SliverToBoxAdapter(
                  child: Padding(
                    padding: EdgeInsets.symmetric(
                      horizontal: isWide ? 40 : 20,
                      vertical: 24,
                    ),
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
                            _buildSelectorRow(isWide),
                            const SizedBox(height: 24),
                            _buildProgressCard(),
                            const SizedBox(height: 32),
                            _buildSectionLabel('QUICK ADD'),
                            const SizedBox(height: 12),
                            _buildQuickButtons(),
                            const SizedBox(height: 32),
                            const SizedBox(height: 12),
                            ...List.generate(findings.length, (i) {
                              return _AnimatedFindingCard(
                                key: ValueKey(findings[i]),
                                index: i,
                                data: findings[i],
                                isWide: isWide,
                                onRemove: findings.length > 1
                                    ? () => _removeFinding(i)
                                    : null,
                                onChanged: () => setState(() {}),
                              );
                            }),
                            const SizedBox(height: 8),
                            _buildAddFindingButton(),
                            const SizedBox(height: 32),
                            _buildSectionLabel('GENERAL NOTES'),
                            const SizedBox(height: 12),
                            _buildNotesCard(),
                            const SizedBox(height: 32),
                            _buildSubmitButton(),
                            const SizedBox(height: 40),
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
    );
  }

  Widget _buildHeader(bool isWide) {
    final now = DateTime.now();
    final dateStr = '${_dayName(now.weekday)}, ${_pad(now.day)} ${_monthName(now.month)} ${now.year}';
        return Container(
      width: double.infinity,
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [AppColors.forest, AppColors.canopy, AppColors.leaf],
        ),
        borderRadius: BorderRadius.circular(24),
        boxShadow: [
          BoxShadow(
            color: AppColors.canopy.withValues(alpha: 0.35),
            blurRadius: 24,
            offset: const Offset(0, 8),
          ),
        ],
      ),
      child: Stack(
        children: [
          // Decorative circles
          Positioned(
            right: -30,
            top: -30,
            child: Container(
              width: 160,
              height: 160,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: Colors.white.withValues(alpha: 0.06),
              ),
            ),
          ),
          Positioned(
            right: 40,
            bottom: -20,
            child: Container(
              width: 100,
              height: 100,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: Colors.white.withValues(alpha: 0.04),
              ),
            ),
          ),
          Padding(
            padding: EdgeInsets.all(isWide ? 36 : 24),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 10, vertical: 4),
                        decoration: BoxDecoration(
                          color: Colors.white.withValues(alpha: 0.15),
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: Text(
                          'SCOUTING INSPECTION',
                          style: AppText.labelStyle.copyWith(
                            color: Colors.white70,
                            letterSpacing: 1.4,
                            fontSize: 11,
                          ),
                        ),
                      ),
                      const SizedBox(height: 12),
                      Text(
                        'New Inspection\nReport',
                        style: AppText.displayStyle.copyWith(
                          color: Colors.white,
                          fontSize: isWide ? 32 : 26,
                          height: 1.15,
                        ),
                      ),
                      const SizedBox(height: 10),
                      Text(
                        dateStr,
                        style: AppText.bodyStyle.copyWith(
                          color: Colors.white60,
                          fontSize: 13,
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 16),
                Container(
                  width: 56,
                  height: 56,
                  decoration: BoxDecoration(
                    color: Colors.white.withValues(alpha: 0.12),
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: const Icon(Icons.eco_rounded,
                      color: Colors.white, size: 28),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSelectorRow(bool isWide) {
    final selectors = [
      _buildStyledDropdown<String>(
        label: 'FARM',
        icon: Icons.agriculture_rounded,
        value: selectedFarm,
        hint: 'Select farm',
        items: farmData.keys.toList(),
        enabled: true,
        onChanged: (v) {
          setState(() {
            selectedFarm = v;
            availableGreenhouses = farmData[v]!.keys.toList();
            selectedGreenhouse = null;
            selectedVariety = null;
            availableVarieties = [];
          });
        },
      ),
      _buildStyledDropdown<String>(
        label: 'GREENHOUSE',
        icon: Icons.house_siding_rounded,
        value: selectedGreenhouse,
        hint: selectedFarm == null ? 'Select farm first' : 'Select greenhouse',
        items: availableGreenhouses,
        enabled: selectedFarm != null,
        onChanged: (v) {
          setState(() {
            selectedGreenhouse = v;
            availableVarieties = farmData[selectedFarm]![v]!;
            selectedVariety = null;
          });
        },
      ),
      _buildStyledDropdown<String>(
        label: 'VARIETY',
        icon: Icons.local_florist_rounded,
        value: selectedVariety,
        hint: selectedGreenhouse == null ? 'Select GH first' : 'Select variety',
        items: availableVarieties,
        enabled: selectedGreenhouse != null,
        onChanged: (v) => setState(() => selectedVariety = v),
      ),
    ];

    if (isWide) {
      return Row(
        children: selectors
            .expand((w) => [Expanded(child: w), const SizedBox(width: 16)])
            .toList()
          ..removeLast(),
      );
    }
    return Column(
      children: selectors
          .expand((w) => [w, const SizedBox(height: 12)])
          .toList()
        ..removeLast(),
    );
  }

  Widget _buildStyledDropdown<T>({
    required String label,
    required IconData icon,
    required T? value,
    String hint = '',
    required List<T> items,
    required bool enabled,
    required ValueChanged<T?> onChanged,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 4, bottom: 6),
          child: Text(label, style: AppText.labelStyle),
        ),
        Container(
          decoration: BoxDecoration(
            color: AppColors.paper,
            borderRadius: BorderRadius.circular(14),
            border: Border.all(
              color: value != null ? AppColors.leaf : AppColors.divider,
              width: value != null ? 1.5 : 1,
            ),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.04),
                blurRadius: 8,
                offset: const Offset(0, 2),
              ),
            ],
          ),
          child: DropdownButtonHideUnderline(
            child: DropdownButton<T>(
              value: value,
              isExpanded: true,
              hint: Padding(
                padding: const EdgeInsets.only(left: 4),
                child: Text(hint,
                    style: AppText.bodyStyle.copyWith(color: AppColors.slate)),
              ),
              padding:
                  const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
              borderRadius: BorderRadius.circular(14),
              icon: Icon(Icons.keyboard_arrow_down_rounded,
                  color: enabled ? AppColors.graphite : AppColors.slate),
              items: !enabled
                  ? null
                  : items
                      .map((item) => DropdownMenuItem<T>(
                            value: item,
                            child: Row(
                              children: [
                                Icon(icon,
                                    size: 16, color: AppColors.leaf),
                                const SizedBox(width: 8),
                                Text(item.toString(),
                                    style: AppText.bodyStyle.copyWith(
                                        fontWeight: FontWeight.w500)),
                              ],
                            ),
                          ))
                      .toList(),
              onChanged: enabled ? onChanged : null,
              selectedItemBuilder: (_) => items
                  .map((item) => Align(
                        alignment: Alignment.centerLeft,
                        child: Text(item.toString(),
                            style: AppText.bodyStyle.copyWith(
                                fontWeight: FontWeight.w600,
                                color: AppColors.forest)),
                      ))
                  .toList(),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildProgressCard() {
    final steps = [
      ('Farm', selectedFarm != null),
      ('Greenhouse', selectedGreenhouse != null),
      ('Variety', selectedVariety != null),
      ('Findings', findings.any((f) => f.issue.trim().isNotEmpty)),
    ];

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.paper,
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: AppColors.divider),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.03),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text('Inspection Progress', style: AppText.headingStyle),
              Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                decoration: BoxDecoration(
                  color: progressPercent == 100
                      ? AppColors.mist
                      : AppColors.fog,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  '$progressPercent%',
                  style: TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.w700,
                    color: progressPercent == 100
                        ? AppColors.forest
                        : AppColors.graphite,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 14),
          TweenAnimationBuilder<double>(
            tween: Tween(begin: 0, end: progress),
            duration: const Duration(milliseconds: 600),
            curve: Curves.easeOutCubic,
            builder: (_, v, _) => ClipRRect(
              borderRadius: BorderRadius.circular(8),
              child: LinearProgressIndicator(
                value: v,
                minHeight: 8,
                backgroundColor: AppColors.fog,
                valueColor: const AlwaysStoppedAnimation(AppColors.leaf),
              ),
            ),
          ),
          const SizedBox(height: 16),
          Row(
            children: steps.map((step) {
              final done = step.$2;
              return Expanded(
                child: Row(
                  children: [
                    AnimatedContainer(
                      duration: const Duration(milliseconds: 300),
                      width: 20,
                      height: 20,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: done ? AppColors.leaf : AppColors.fog,
                        border: Border.all(
                          color: done ? AppColors.leaf : AppColors.divider,
                        ),
                      ),
                      child: done
                          ? const Icon(Icons.check,
                              size: 12, color: Colors.white)
                          : null,
                    ),
                    const SizedBox(width: 6),
                    Flexible(
                      child: Text(
                        step.$1,
                        style: AppText.labelStyle.copyWith(
                          color: done ? AppColors.forest : AppColors.slate,
                          fontSize: 11,
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    if (steps.indexOf(step) < steps.length - 1)
                      Expanded(
                        child: Container(
                          height: 1,
                          margin:
                              const EdgeInsets.symmetric(horizontal: 6),
                          color: AppColors.divider,
                        ),
                      ),
                  ],
                ),
              );
            }).toList(),
          ),
        ],
      ),
    );
  }

  static const _quickItems = [
    ('Disease', Icons.coronavirus_rounded, AppColors.disease),
    ('Pest', Icons.bug_report_rounded, AppColors.pest),
    ('Water Stress', Icons.water_drop_rounded, AppColors.water),
    ('Nutrition', Icons.eco_rounded, AppColors.nutrition),
    ('Irrigation', Icons.grass_rounded, AppColors.irrigation),
    ('Other', Icons.warning_amber_rounded, AppColors.other),
  ];

  Widget _buildQuickButtons() {
    return Wrap(
      spacing: 10,
      runSpacing: 10,
      children: _quickItems.map((item) {
        return _QuickChip(
          label: item.$1,
          icon: item.$2,
          color: item.$3,
          onTap: () => _addFinding(item.$1),
        );
      }).toList(),
    );
  }

  Widget _buildAddFindingButton() {
    return GestureDetector(
      onTap: () => _addFinding(),
      child: Container(
        height: 52,
        decoration: BoxDecoration(
          color: AppColors.paper,
          borderRadius: BorderRadius.circular(14),
          border: Border.all(
            color: AppColors.leaf,
            style: BorderStyle.solid,
            width: 1.5,
          ),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.add_circle_outline_rounded,
                color: AppColors.leaf, size: 20),
            const SizedBox(width: 8),
            Text(
              'Add Another Finding',
              style: AppText.bodyStyle.copyWith(
                color: AppColors.leaf,
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildNotesCard() {
    return Container(
      decoration: BoxDecoration(
        color: AppColors.paper,
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: AppColors.divider),
      ),
      child: TextField(
        controller: generalNotesController,
        maxLines: 5,
        style: AppText.bodyStyle,
        decoration: InputDecoration(
          hintText: '',
          hintStyle: AppText.bodyStyle.copyWith(color: AppColors.slate),
          contentPadding: const EdgeInsets.all(20),
          border: InputBorder.none,
        ),
      ),
    );
  }

  Widget _buildSubmitButton() {
    final ready = selectedFarm != null &&
        selectedGreenhouse != null &&
        selectedVariety != null;

    return AnimatedContainer(
      duration: const Duration(milliseconds: 300),
      height: 58,
      decoration: BoxDecoration(
        gradient: ready
            ? const LinearGradient(
                colors: [AppColors.forest, AppColors.canopy],
              )
            : null,
        color: ready ? null : AppColors.fog,
        borderRadius: BorderRadius.circular(16),
        boxShadow: ready
            ? [
                BoxShadow(
                  color: AppColors.canopy.withValues(alpha: 0.4),
                  blurRadius: 16,
                  offset: const Offset(0, 6),
                )
              ]
            : [],
      ),
      child: Material(
        color: Colors.transparent,
        borderRadius: BorderRadius.circular(16),
        child: InkWell(
          borderRadius: BorderRadius.circular(16),
          onTap: ready
              ? () {
                  HapticFeedback.mediumImpact();
                  _showSuccessSnackbar();
                }
              : null,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                Icons.check_circle_outline_rounded,
                color: ready ? Colors.white : AppColors.slate,
                size: 22,
              ),
              const SizedBox(width: 10),
              Text(
                ready ? 'Submit Inspection' : 'Complete all fields to submit',
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w700,
                  color: ready ? Colors.white : AppColors.slate,
                  letterSpacing: 0.2,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _showSuccessSnackbar() {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        backgroundColor: AppColors.forest,
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        content: const Row(
          children: [
            Icon(Icons.check_circle, color: AppColors.mint),
            SizedBox(width: 10),
            Text('Inspection submitted successfully',
                style: TextStyle(color: Colors.white)),
          ],
        ),
        duration: const Duration(seconds: 3),
      ),
    );
  }

  Widget _buildSectionLabel(String text) {
    return Text(text, style: AppText.labelStyle);
  }

  String _dayName(int d) =>
      ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][d - 1];
  String _monthName(int m) => [
        'Jan','Feb','Mar','Apr','May','Jun',
        'Jul','Aug','Sep','Oct','Nov','Dec'
      ][m - 1];
  String _pad(int n) => n.toString().padLeft(2, '0');
}

//  Quick chip
class _QuickChip extends StatefulWidget {
  final String label;
  final IconData icon;
  final Color color;
  final VoidCallback onTap;

  const _QuickChip({
    required this.label,
    required this.icon,
    required this.color,
    required this.onTap,
  });

  @override
  State<_QuickChip> createState() => _QuickChipState();
}

class _QuickChipState extends State<_QuickChip>
    with SingleTickerProviderStateMixin {
  late AnimationController _ctrl;
  late Animation<double> _scale;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(
        vsync: this, duration: const Duration(milliseconds: 120));
    _scale = Tween(begin: 1.0, end: 0.93)
        .animate(CurvedAnimation(parent: _ctrl, curve: Curves.easeOut));
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ScaleTransition(
      scale: _scale,
      child: GestureDetector(
        onTapDown: (_) => _ctrl.forward(),
        onTapUp: (_) {
          _ctrl.reverse();
          HapticFeedback.selectionClick();
          widget.onTap();
        },
        onTapCancel: () => _ctrl.reverse(),
        child: Container(
          padding:
              const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
          decoration: BoxDecoration(
            color: widget.color.withValues(alpha: 0.08),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(
                color: widget.color.withValues(alpha: 0.2), width: 1.5),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(widget.icon, size: 16, color: widget.color),
              const SizedBox(width: 6),
              Text(
                widget.label,
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                  color: widget.color,
                ),
              ),
              const SizedBox(width: 6),
              Container(
                width: 18,
                height: 18,
                decoration: BoxDecoration(
                  color: widget.color.withValues(alpha: 0.15),
                  shape: BoxShape.circle,
                ),
                child: Icon(Icons.add, size: 12, color: widget.color),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

//  Animated Finding Card
class _AnimatedFindingCard extends StatefulWidget {
  final int index;
  final FindingData data;
  final bool isWide;
  final VoidCallback? onRemove;
  final VoidCallback onChanged;

  const _AnimatedFindingCard({
    super.key,
    required this.index,
    required this.data,
    required this.isWide,
    this.onRemove,
    required this.onChanged,
  });

  @override
  State<_AnimatedFindingCard> createState() => _AnimatedFindingCardState();
}

class _AnimatedFindingCardState extends State<_AnimatedFindingCard>
    with SingleTickerProviderStateMixin {
  late AnimationController _ctrl;
  late Animation<double> _fade;
  late Animation<Offset> _slide;

  final TextEditingController _issueCtrl = TextEditingController();
  final TextEditingController _areaCtrl = TextEditingController();
  final TextEditingController _notesCtrl = TextEditingController();

  static const _categories = [
    'Disease', 'Pest', 'Nutrition', 'Water Stress',
    'Irrigation', 'Environmental', 'Other',
  ];
  static const _severities = ['Low', 'Medium', 'High', 'Critical'];

  static const _severityColors = {
    'Low': AppColors.low,
    'Medium': AppColors.medium,
    'High': AppColors.high,
    'Critical': AppColors.critical,
  };

  static const _categoryColors = {
    'Disease': AppColors.disease,
    'Pest': AppColors.pest,
    'Nutrition': AppColors.nutrition,
    'Water Stress': AppColors.water,
    'Irrigation': AppColors.irrigation,
    'Environmental': AppColors.environmental,
    'Other': AppColors.other,
  };

  @override
  void initState() {
    super.initState();
    _issueCtrl.text = widget.data.issue;
    _areaCtrl.text = widget.data.affectedArea?.toString() ?? '';
    _notesCtrl.text = widget.data.notes;

    _issueCtrl.addListener(() {
      widget.data.issue = _issueCtrl.text;
      widget.onChanged();
    });
    _notesCtrl.addListener(() => widget.data.notes = _notesCtrl.text);
    _areaCtrl.addListener(() {
      widget.data.affectedArea = double.tryParse(_areaCtrl.text);
    });

    _ctrl = AnimationController(
        vsync: this, duration: const Duration(milliseconds: 400));
    _fade = CurvedAnimation(parent: _ctrl, curve: Curves.easeOut);
    _slide = Tween<Offset>(
            begin: const Offset(0, 0.06), end: Offset.zero)
        .animate(CurvedAnimation(parent: _ctrl, curve: Curves.easeOut));
    _ctrl.forward();
  }

  @override
  void dispose() {
    _ctrl.dispose();
    _issueCtrl.dispose();
    _areaCtrl.dispose();
    _notesCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final accentColor =
        _categoryColors[widget.data.category] ?? AppColors.graphite;
    final sevColor =
        _severityColors[widget.data.severity] ?? AppColors.medium;

    return FadeTransition(
      opacity: _fade,
      child: SlideTransition(
        position: _slide,
        child: Container(
          margin: const EdgeInsets.only(bottom: 16),
          decoration: BoxDecoration(
            color: AppColors.paper,
            borderRadius: BorderRadius.circular(20),
            border: Border.all(color: AppColors.divider),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.04),
                blurRadius: 10,
                offset: const Offset(0, 3),
              ),
            ],
          ),
          child: Column(
            children: [
              Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
                decoration: BoxDecoration(
                  color: accentColor.withValues(alpha: 0.07),
                  borderRadius: const BorderRadius.vertical(
                      top: Radius.circular(20)),
                  border: Border(
                    left: BorderSide(color: accentColor, width: 4),
                  ),
                ),
                child: Row(
                  children: [
                    Container(
                      width: 32,
                      height: 32,
                      decoration: BoxDecoration(
                        color: accentColor.withValues(alpha: 0.12),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Center(
                        child: Text(
                          '${widget.index + 1}',
                          style: TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.w800,
                            color: accentColor,
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 10),
                    Text(
                      'Finding ${widget.index + 1}',
                      style: AppText.headingStyle.copyWith(fontSize: 16),
                    ),
                    const SizedBox(width: 8),
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 8, vertical: 3),
                      decoration: BoxDecoration(
                        color: sevColor.withValues(alpha: 0.12),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        widget.data.severity,
                        style: TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.w700,
                          color: sevColor,
                        ),
                      ),
                    ),
                    const Spacer(),
                    if (widget.onRemove != null)
                      GestureDetector(
                        onTap: widget.onRemove,
                        child: Container(
                          width: 30,
                          height: 30,
                          decoration: BoxDecoration(
                            color: Colors.red.withValues(alpha: 0.07),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: const Icon(Icons.close_rounded,
                              size: 16, color: Colors.red),
                        ),
                      ),
                  ],
                ),
              ),

              Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  children: [
                    if (widget.isWide)
                      Row(
                        children: [
                          Expanded(child: _buildCategoryDropdown()),
                          const SizedBox(width: 16),
                          Expanded(child: _buildSeverityDropdown(sevColor)),
                        ],
                      )
                    else ...[
                      _buildCategoryDropdown(),
                      const SizedBox(height: 12),
                      _buildSeverityDropdown(sevColor),
                    ],
                    const SizedBox(height: 16),
                    _buildTextField(
                      controller: _issueCtrl,
                      label: 'Issue Description',
                      icon: Icons.description_outlined,
                    ),
                    const SizedBox(height: 16),
                    if (widget.isWide)
                      Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          SizedBox(
                            width: 180,
                            child: _buildTextField(
                              controller: _areaCtrl,
                              label: 'Affected Area',
                              icon: Icons.area_chart_rounded,
                              suffix: '%',
                              keyboardType: TextInputType.number,
                            ),
                          ),
                          const SizedBox(width: 16),
                          Expanded(
                            child: _buildTextField(
                              controller: _notesCtrl,
                              label: 'Notes',
                              icon: Icons.notes_rounded,
                              maxLines: 3,
                            ),
                          ),
                        ],
                      )
                    else ...[
                      _buildTextField(
                        controller: _areaCtrl,
                        label: 'Affected Area (%)',
                        icon: Icons.area_chart_rounded,
                        suffix: '%',
                        keyboardType: TextInputType.number,
                      ),
                      const SizedBox(height: 16),
                      _buildTextField(
                        controller: _notesCtrl,
                        label: 'Notes',
                        icon: Icons.notes_rounded,
                        maxLines: 3,
                      ),
                    ],
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildCategoryDropdown() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 2, bottom: 6),
          child: Text('CATEGORY', style: AppText.labelStyle),
        ),
        Container(
          decoration: BoxDecoration(
            color: AppColors.cream,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: AppColors.divider),
          ),
          child: DropdownButtonHideUnderline(
            child: DropdownButton<String>(
              value: widget.data.category,
              isExpanded: true,
              padding:
                  const EdgeInsets.symmetric(horizontal: 14, vertical: 2),
              borderRadius: BorderRadius.circular(12),
              icon: const Icon(Icons.keyboard_arrow_down_rounded,
                  color: AppColors.graphite),
              items: _categories
                  .map((c) => DropdownMenuItem(
                        value: c,
                        child: Text(c,
                            style: AppText.bodyStyle
                                .copyWith(fontWeight: FontWeight.w500)),
                      ))
                  .toList(),
              onChanged: (v) => setState(() => widget.data.category = v!),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildSeverityDropdown(Color sevColor) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 2, bottom: 6),
          child: Text('SEVERITY', style: AppText.labelStyle),
        ),
        Container(
          decoration: BoxDecoration(
            color: sevColor.withValues(alpha: 0.06),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: sevColor.withValues(alpha: 0.2)),
          ),
          child: DropdownButtonHideUnderline(
            child: DropdownButton<String>(
              value: widget.data.severity,
              isExpanded: true,
              padding:
                  const EdgeInsets.symmetric(horizontal: 14, vertical: 2),
              borderRadius: BorderRadius.circular(12),
              icon: Icon(Icons.keyboard_arrow_down_rounded, color: sevColor),
              items: _severities
                  .map((s) => DropdownMenuItem(
                        value: s,
                        child: Row(
                          children: [
                            Container(
                              width: 8,
                              height: 8,
                              decoration: BoxDecoration(
                                shape: BoxShape.circle,
                                color: _severityColors[s] ?? AppColors.medium,
                              ),
                            ),
                            const SizedBox(width: 8),
                            Text(s,
                                style: AppText.bodyStyle.copyWith(
                                    fontWeight: FontWeight.w500)),
                          ],
                        ),
                      ))
                  .toList(),
              onChanged: (v) => setState(() => widget.data.severity = v!),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildTextField({
    required TextEditingController controller,
    required String label,
    String hint = '',
    required IconData icon,
    String? suffix,
    int maxLines = 1,
    TextInputType keyboardType = TextInputType.text,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 2, bottom: 6),
          child: Text(label.toUpperCase(), style: AppText.labelStyle),
        ),
        Container(
          decoration: BoxDecoration(
            color: AppColors.cream,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: AppColors.divider),
          ),
          child: TextField(
            controller: controller,
            maxLines: maxLines,
            keyboardType: keyboardType,
            style: AppText.bodyStyle,
            decoration: InputDecoration(
              hintText: hint,
              hintStyle: AppText.bodyStyle.copyWith(color: AppColors.slate),
              prefixIcon: Icon(icon, size: 18, color: AppColors.slate),
              suffixText: suffix,
              suffixStyle: AppText.bodyStyle.copyWith(
                  color: AppColors.graphite, fontWeight: FontWeight.w600),
              border: InputBorder.none,
              contentPadding:
                  const EdgeInsets.symmetric(horizontal: 14, vertical: 14),
            ),
          ),
        ),
      ],
    );
  }
}



