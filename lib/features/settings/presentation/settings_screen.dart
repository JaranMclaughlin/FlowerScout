import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

// ── Design tokens (mirrors scouting_screen.dart) ─────────────────────────────
class _C {
  static const forest    = Color(0xFF1B4332);
  static const canopy    = Color(0xFF2D6A4F);
  static const leaf      = Color(0xFF40916C);
  static const mint      = Color(0xFF74C69D);
  static const mist      = Color(0xFFD8F3DC);
  static const cream     = Color(0xFFF8FAF8);
  static const paper     = Color(0xFFFFFFFF);
  static const ink       = Color(0xFF0D1B0F);
  static const graphite  = Color(0xFF3D4F42);
  static const slate     = Color(0xFF6B7F6E);
  static const fog       = Color(0xFFEAEFEA);
  static const divider   = Color(0xFFDDE5DD);
}

class _T {
  static const heading = TextStyle(
    fontFamily: 'Georgia',
    fontSize: 20,
    fontWeight: FontWeight.w600,
    color: _C.ink,
    letterSpacing: -0.3,
  );
  static const label = TextStyle(
    fontSize: 12,
    fontWeight: FontWeight.w600,
    color: _C.slate,
    letterSpacing: 1.0,
  );
  static const body = TextStyle(
    fontSize: 14,
    color: _C.graphite,
    height: 1.5,
  );
}

// ── Farm / Greenhouse data model ──────────────────────────────────────────────
class _GreenhouseInfo {
  final String id;
  final List<String> varieties;
  bool active;

  _GreenhouseInfo({
    required this.id,
    required this.varieties,
    this.active = true,
  });
}

class _FarmInfo {
  final String name;
  final List<_GreenhouseInfo> greenhouses;
  bool expanded;

  _FarmInfo({
    required this.name,
    required this.greenhouses,
    this.expanded = false,
  });
}

// ── Settings tabs ─────────────────────────────────────────────────────────────
enum _Tab { farms, profile, team, notifications, preferences }

// ── Main screen ───────────────────────────────────────────────────────────────
class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen>
    with SingleTickerProviderStateMixin {
  _Tab _activeTab = _Tab.farms;

  // ── Farm data (same farms as scouting screen) ─────────────────────────────
  final List<_FarmInfo> _farms = [
    _FarmInfo(
      name: 'Kongoni River Farm',
      expanded: true,
      greenhouses: [
        _GreenhouseInfo(id: 'GH-01', varieties: ['Athena', 'Moonwalk']),
        _GreenhouseInfo(id: 'GH-02', varieties: ['Madam Red']),
        _GreenhouseInfo(id: 'GH-03', varieties: ['Explorer']),
        _GreenhouseInfo(id: 'GH-12', varieties: ['Athena', 'Madam Red']),
        _GreenhouseInfo(id: 'GH-25', varieties: ['White Dove']),
      ],
    ),
    _FarmInfo(
      name: 'Main Farm',
      greenhouses: [
        _GreenhouseInfo(id: 'GH-11', varieties: ['Athena']),
        _GreenhouseInfo(id: 'GH-12', varieties: ['Moonwalk']),
        _GreenhouseInfo(id: 'GH-13', varieties: ['Madam Red']),
      ],
    ),
    _FarmInfo(
      name: 'North Farm',
      greenhouses: [
        _GreenhouseInfo(id: 'GH-21', varieties: ['Explorer']),
        _GreenhouseInfo(id: 'GH-22', varieties: ['White Dove']),
      ],
    ),
  ];

  // ── Profile state ─────────────────────────────────────────────────────────
  final _nameCtrl  = TextEditingController(text: 'Jaran Mclauglin');
  final _emailCtrl = TextEditingController(text: 'jaran@flowerscout.co.ke');
  String _selectedRole = 'Admin';
  static const _roles = ['Admin', 'Manager', 'Scout', 'Viewer'];

  // ── Notification toggles ──────────────────────────────────────────────────
  bool _notifOverdue    = true;
  bool _notifCritical   = true;
  bool _notifWeekly     = false;
  bool _notifPush       = true;
  bool _notifEmail      = true;
  bool _notifSms        = false;

  // ── Preferences ───────────────────────────────────────────────────────────
  String _theme         = 'System default';
  String _dateFormat    = 'DD/MM/YYYY';
  String _mapDefault    = 'Satellite';
  bool   _heatmapOnLoad = true;
  int    _inspInterval  = 7;

  // ── Team (static demo) ────────────────────────────────────────────────────
  final _members = <Map<String, dynamic>>[
    {'initials': 'JM', 'name': 'Jaran Mclauglin', 'role': 'Admin',   'farms': 'All farms',       'you': true},
    {'initials': 'AK', 'name': 'Amara K.',         'role': 'Scout',   'farms': 'Kongoni, Main',   'you': false},
    {'initials': 'TM', 'name': 'Thomas M.',         'role': 'Scout',   'farms': 'North Farm',      'you': false},
    {'initials': 'WN', 'name': 'Wanjiku N.',         'role': 'Viewer',  'farms': 'All farms',       'you': false},
  ];
  final _inviteCtrl = TextEditingController();
  String _inviteRole = 'Scout';

  @override
  void dispose() {
    _nameCtrl.dispose();
    _emailCtrl.dispose();
    _inviteCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: _C.cream,
      body: SafeArea(
        child: LayoutBuilder(
          builder: (context, constraints) {
            final isWide = constraints.maxWidth >= 900;
            return isWide
                ? _wideLayout(constraints)
                : _narrowLayout();
          },
        ),
      ),
    );
  }

  // ── Wide: left rail + content ─────────────────────────────────────────────
  Widget _wideLayout(BoxConstraints constraints) {
    return Row(
      children: [
        _buildRail(),
        const VerticalDivider(thickness: 0.5, width: 0.5, color: _C.divider),
        Expanded(child: _buildContent(true)),
      ],
    );
  }

  Widget _buildRail() {
    return Container(
      width: 200,
      color: _C.paper,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(20, 28, 20, 16),
            child: Text('Settings', style: _T.heading),
          ),
          const Divider(height: 0.5, thickness: 0.5, color: _C.divider),
          const SizedBox(height: 8),
          ..._Tab.values.map((t) => _railItem(t)),
          const Spacer(),
          Padding(
            padding: const EdgeInsets.all(16),
            child: _versionBadge(),
          ),
        ],
      ),
    );
  }

  Widget _railItem(_Tab tab) {
    final active = _activeTab == tab;
    final data = _tabMeta(tab);
    return GestureDetector(
      onTap: () => setState(() => _activeTab = tab),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 180),
        margin: const EdgeInsets.symmetric(horizontal: 10, vertical: 2),
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
        decoration: BoxDecoration(
          color: active ? _C.leaf.withValues(alpha: 0.1) : Colors.transparent,
          borderRadius: BorderRadius.circular(12),
          border: Border(
            left: BorderSide(
              color: active ? _C.leaf : Colors.transparent,
              width: 3,
            ),
          ),
        ),
        child: Row(
          children: [
            Icon(data.icon,
                size: 18,
                color: active ? _C.leaf : _C.slate),
            const SizedBox(width: 10),
            Text(
              data.label,
              style: _T.body.copyWith(
                color: active ? _C.forest : _C.slate,
                fontWeight: active ? FontWeight.w600 : FontWeight.w400,
              ),
            ),
          ],
        ),
      ),
    );
  }

  // ── Narrow: top tab bar ───────────────────────────────────────────────────
  Widget _narrowLayout() {
    return Column(
      children: [
        _buildTopBar(),
        Expanded(child: _buildContent(false)),
      ],
    );
  }

  Widget _buildTopBar() {
    return Container(
      color: _C.paper,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Padding(
            padding: EdgeInsets.fromLTRB(20, 20, 20, 12),
            child: Text('Settings',
                style: TextStyle(
                  fontFamily: 'Georgia',
                  fontSize: 22,
                  fontWeight: FontWeight.w700,
                  color: _C.ink,
                )),
          ),
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Row(
              children: _Tab.values.map((t) => _topBarChip(t)).toList(),
            ),
          ),
          const Divider(height: 0.5, thickness: 0.5, color: _C.divider),
        ],
      ),
    );
  }

  Widget _topBarChip(_Tab tab) {
    final active = _activeTab == tab;
    final data = _tabMeta(tab);
    return GestureDetector(
      onTap: () => setState(() => _activeTab = tab),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 180),
        margin: const EdgeInsets.only(right: 6, bottom: 8),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
        decoration: BoxDecoration(
          color: active ? _C.leaf.withValues(alpha: 0.12) : _C.fog,
          borderRadius: BorderRadius.circular(20),
          border: Border.all(
            color: active ? _C.leaf.withValues(alpha: 0.4) : Colors.transparent,
          ),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(data.icon, size: 15, color: active ? _C.leaf : _C.slate),
            const SizedBox(width: 6),
            Text(
              data.label,
              style: _T.body.copyWith(
                fontSize: 13,
                color: active ? _C.forest : _C.slate,
                fontWeight: active ? FontWeight.w600 : FontWeight.w400,
              ),
            ),
          ],
        ),
      ),
    );
  }

  // ── Content router ────────────────────────────────────────────────────────
  Widget _buildContent(bool isWide) {
    return SingleChildScrollView(
      padding: EdgeInsets.symmetric(
        horizontal: isWide ? 36 : 20,
        vertical: 28,
      ),
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 800),
          child: switch (_activeTab) {
            _Tab.farms         => _buildFarmsTab(isWide),
            _Tab.profile       => _buildProfileTab(isWide),
            _Tab.team          => _buildTeamTab(isWide),
            _Tab.notifications => _buildNotificationsTab(),
            _Tab.preferences   => _buildPreferencesTab(isWide),
          },
        ),
      ),
    );
  }

  // ═════════════════════════════════════════════════════════════════════════
  // TAB 1 — Farm & Greenhouse Config
  // ═════════════════════════════════════════════════════════════════════════
  Widget _buildFarmsTab(bool isWide) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _sectionHeader(
          'Farm & greenhouse config',
          'Manage your farms, greenhouses, and growing locations.',
          Icons.agriculture_rounded,
          _C.leaf,
        ),
        const SizedBox(height: 24),
        ..._farms.map((farm) => _farmCard(farm, isWide)),
        const SizedBox(height: 16),
        _card(
          label: 'INSPECTION DEFAULTS',
          child: Column(
            children: [
              _settingRow(
                label: 'Inspection interval',
                subtitle: 'Days between required greenhouse checks',
                trailing: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    _iconBtn(Icons.remove_rounded, () {
                      if (_inspInterval > 1) {
                        setState(() => _inspInterval--);
                      }
                    }),
                    SizedBox(
                      width: 36,
                      child: Text(
                        '$_inspInterval',
                        textAlign: TextAlign.center,
                        style: _T.body.copyWith(
                          fontWeight: FontWeight.w700,
                          color: _C.forest,
                        ),
                      ),
                    ),
                    _iconBtn(Icons.add_rounded, () {
                      if (_inspInterval < 30) {
                        setState(() => _inspInterval++);
                      }
                    }),
                  ],
                ),
              ),
              _divider(),
              _settingRow(
                label: 'GPS format',
                subtitle: 'Coordinate display format on maps',
                trailing: _miniDropdown(
                  value: 'Decimal degrees',
                  items: ['Decimal degrees', 'DMS'],
                  onChanged: (_) {},
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 24),
        _saveButton('Save farm settings'),
      ],
    );
  }

  Widget _farmCard(_FarmInfo farm, bool isWide) {
    final ghCount = farm.greenhouses.length;
    final activeCount = farm.greenhouses.where((g) => g.active).length;

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      decoration: BoxDecoration(
        color: _C.paper,
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: _C.divider),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.03),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        children: [
          // Farm header row
          GestureDetector(
            onTap: () => setState(() => farm.expanded = !farm.expanded),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
              decoration: BoxDecoration(
                color: farm.expanded
                    ? _C.leaf.withValues(alpha: 0.06)
                    : Colors.transparent,
                borderRadius: farm.expanded
                    ? const BorderRadius.vertical(top: Radius.circular(18))
                    : BorderRadius.circular(18),
              ),
              child: Row(
                children: [
                  Container(
                    width: 40,
                    height: 40,
                    decoration: BoxDecoration(
                      color: _C.mist,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: const Icon(Icons.agriculture_rounded,
                        color: _C.leaf, size: 20),
                  ),
                  const SizedBox(width: 14),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          farm.name,
                          style: _T.body.copyWith(
                            fontWeight: FontWeight.w600,
                            color: _C.ink,
                            fontSize: 15,
                          ),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          '$activeCount of $ghCount greenhouses active',
                          style: _T.body.copyWith(
                            fontSize: 12,
                            color: _C.slate,
                          ),
                        ),
                      ],
                    ),
                  ),
                  _statusBadge(activeCount == ghCount ? 'Active' : 'Partial'),
                  const SizedBox(width: 8),
                  AnimatedRotation(
                    turns: farm.expanded ? 0.5 : 0,
                    duration: const Duration(milliseconds: 200),
                    child: const Icon(Icons.keyboard_arrow_down_rounded,
                        color: _C.slate),
                  ),
                ],
              ),
            ),
          ),

          // Greenhouse list (expanded)
          AnimatedSize(
            duration: const Duration(milliseconds: 250),
            curve: Curves.easeOut,
            child: farm.expanded
                ? Column(
                    children: [
                      const Divider(
                          height: 0.5, thickness: 0.5, color: _C.divider),
                      ...farm.greenhouses.map(
                        (gh) => _greenhouseRow(gh, farm.greenhouses.last == gh),
                      ),
                    ],
                  )
                : const SizedBox.shrink(),
          ),
        ],
      ),
    );
  }

  Widget _greenhouseRow(_GreenhouseInfo gh, bool isLast) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
      decoration: BoxDecoration(
        border: isLast
            ? null
            : const Border(
                bottom: BorderSide(color: _C.divider, width: 0.5)),
      ),
      child: Row(
        children: [
          const SizedBox(width: 8),
          Container(
            width: 6,
            height: 6,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: gh.active ? _C.leaf : _C.slate,
            ),
          ),
          const SizedBox(width: 14),
          Container(
            width: 52,
            padding:
                const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
            decoration: BoxDecoration(
              color: _C.fog,
              borderRadius: BorderRadius.circular(6),
            ),
            child: Text(
              gh.id,
              style: _T.label.copyWith(
                fontSize: 11,
                color: _C.graphite,
              ),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              gh.varieties.join(' · '),
              style: _T.body.copyWith(fontSize: 13, color: _C.graphite),
              overflow: TextOverflow.ellipsis,
            ),
          ),
          Transform.scale(
            scale: 0.85,
            child: Switch.adaptive(
              value: gh.active,
              activeColor: _C.leaf,
              onChanged: (v) => setState(() => gh.active = v),
            ),
          ),
        ],
      ),
    );
  }

  // ═════════════════════════════════════════════════════════════════════════
  // TAB 2 — Profile
  // ═════════════════════════════════════════════════════════════════════════
  Widget _buildProfileTab(bool isWide) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _sectionHeader(
          'Your profile',
          'Update your personal details and login credentials.',
          Icons.person_rounded,
          _C.canopy,
        ),
        const SizedBox(height: 24),
        _card(
          label: 'PERSONAL INFO',
          child: Column(
            children: [
              // Avatar row
              Row(
                children: [
                  Container(
                    width: 56,
                    height: 56,
                    decoration: BoxDecoration(
                      color: _C.mist,
                      shape: BoxShape.circle,
                      border: Border.all(color: _C.mint, width: 2),
                    ),
                    child: const Center(
                      child: Text('JM',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.w700,
                            color: _C.forest,
                          )),
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Jaran Mclauglin',
                            style: _T.body.copyWith(
                              fontWeight: FontWeight.w600,
                              color: _C.ink,
                            )),
                        const SizedBox(height: 2),
                        Text('Farm Scout Admin',
                            style: _T.body
                                .copyWith(fontSize: 12, color: _C.slate)),
                      ],
                    ),
                  ),
                  _outlineBtn('Change photo', () {}),
                ],
              ),
              _divider(),
              _styledTextField(
                  label: 'FULL NAME', controller: _nameCtrl),
              const SizedBox(height: 14),
              _styledTextField(
                  label: 'EMAIL',
                  controller: _emailCtrl,
                  keyboardType: TextInputType.emailAddress),
              const SizedBox(height: 14),
              _labeledDropdown(
                label: 'ROLE',
                value: _selectedRole,
                items: _roles,
                onChanged: (v) => setState(() => _selectedRole = v!),
              ),
            ],
          ),
        ),
        const SizedBox(height: 12),
        _card(
          label: 'CHANGE PASSWORD',
          child: Column(
            children: [
              _styledTextField(
                  label: 'CURRENT PASSWORD',
                  controller: TextEditingController(),
                  obscure: true),
              const SizedBox(height: 14),
              if (isWide)
                Row(
                  children: [
                    Expanded(
                        child: _styledTextField(
                            label: 'NEW PASSWORD',
                            controller: TextEditingController(),
                            obscure: true)),
                    const SizedBox(width: 14),
                    Expanded(
                        child: _styledTextField(
                            label: 'CONFIRM',
                            controller: TextEditingController(),
                            obscure: true)),
                  ],
                )
              else ...[
                _styledTextField(
                    label: 'NEW PASSWORD',
                    controller: TextEditingController(),
                    obscure: true),
                const SizedBox(height: 14),
                _styledTextField(
                    label: 'CONFIRM',
                    controller: TextEditingController(),
                    obscure: true),
              ],
            ],
          ),
        ),
        const SizedBox(height: 24),
        _saveButton('Save profile'),
      ],
    );
  }

  // ═════════════════════════════════════════════════════════════════════════
  // TAB 3 — Team
  // ═════════════════════════════════════════════════════════════════════════
  Widget _buildTeamTab(bool isWide) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _sectionHeader(
          'Team management',
          'Control who has access and what they can see.',
          Icons.group_rounded,
          _C.canopy,
        ),
        const SizedBox(height: 24),
        _card(
          label: 'TEAM MEMBERS',
          child: Column(
            children: [
              ..._members.asMap().entries.map((e) {
                final m = e.value;
                final isLast = e.key == _members.length - 1;
                return _memberRow(m, isLast);
              }),
            ],
          ),
        ),
        const SizedBox(height: 12),
        _card(
          label: 'INVITE A NEW MEMBER',
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              if (isWide)
                Row(
                  children: [
                    Expanded(
                      child: _styledTextField(
                        label: 'EMAIL ADDRESS',
                        controller: _inviteCtrl,
                        hint: 'colleague@farm.co.ke',
                        keyboardType: TextInputType.emailAddress,
                      ),
                    ),
                    const SizedBox(width: 14),
                    SizedBox(
                      width: 160,
                      child: _labeledDropdown(
                        label: 'ROLE',
                        value: _inviteRole,
                        items: ['Scout', 'Viewer', 'Admin'],
                        onChanged: (v) => setState(() => _inviteRole = v!),
                      ),
                    ),
                  ],
                )
              else ...[
                _styledTextField(
                  label: 'EMAIL ADDRESS',
                  controller: _inviteCtrl,
                  hint: 'colleague@farm.co.ke',
                  keyboardType: TextInputType.emailAddress,
                ),
                const SizedBox(height: 14),
                _labeledDropdown(
                  label: 'ROLE',
                  value: _inviteRole,
                  items: ['Scout', 'Viewer', 'Admin'],
                  onChanged: (v) => setState(() => _inviteRole = v!),
                ),
              ],
              const SizedBox(height: 16),
              _saveButton('Send invite',
                  icon: Icons.send_rounded, color: _C.canopy),
            ],
          ),
        ),
      ],
    );
  }

  Widget _memberRow(Map<String, dynamic> m, bool isLast) {
    final colors = [_C.mist, _C.fog, const Color(0xFFEDE7F6), const Color(0xFFFFF8E1)];
    final textColors = [_C.forest, _C.graphite, const Color(0xFF4527A0), const Color(0xFFE65100)];
    final idx = _members.indexOf(m) % colors.length;

    return Container(
      padding: const EdgeInsets.symmetric(vertical: 12),
      decoration: BoxDecoration(
        border: isLast
            ? null
            : const Border(
                bottom: BorderSide(color: _C.divider, width: 0.5)),
      ),
      child: Row(
        children: [
          Container(
            width: 38,
            height: 38,
            decoration: BoxDecoration(
              color: colors[idx],
              shape: BoxShape.circle,
            ),
            child: Center(
              child: Text(
                m['initials'] as String,
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w700,
                  color: textColors[idx],
                ),
              ),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Text(m['name'] as String,
                        style: _T.body.copyWith(
                            fontWeight: FontWeight.w600, color: _C.ink)),
                    if (m['you'] == true) ...[
                      const SizedBox(width: 6),
                      _statusBadge('You', color: _C.leaf),
                    ],
                  ],
                ),
                const SizedBox(height: 2),
                Text('${m['role']} · ${m['farms']}',
                    style:
                        _T.body.copyWith(fontSize: 12, color: _C.slate)),
              ],
            ),
          ),
          if (m['you'] != true)
            _outlineBtn('Manage', () {}),
        ],
      ),
    );
  }

  // ═════════════════════════════════════════════════════════════════════════
  // TAB 4 — Notifications
  // ═════════════════════════════════════════════════════════════════════════
  Widget _buildNotificationsTab() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _sectionHeader(
          'Notifications & alerts',
          'Control when and how FlowerScout notifies you.',
          Icons.notifications_rounded,
          _C.canopy,
        ),
        const SizedBox(height: 24),
        _card(
          label: 'INSPECTION ALERTS',
          child: Column(
            children: [
              _toggleRow(
                label: 'Overdue inspection reminder',
                subtitle: 'Notify when a greenhouse passes its inspection date',
                value: _notifOverdue,
                onChanged: (v) => setState(() => _notifOverdue = v),
              ),
              _divider(),
              _toggleRow(
                label: 'Critical pest / disease alert',
                subtitle: 'Immediate push when health score drops below threshold',
                value: _notifCritical,
                onChanged: (v) => setState(() => _notifCritical = v),
              ),
              _divider(),
              _toggleRow(
                label: 'Weekly summary report',
                subtitle: 'Every Monday 7 AM — farm health digest',
                value: _notifWeekly,
                onChanged: (v) => setState(() => _notifWeekly = v),
              ),
            ],
          ),
        ),
        const SizedBox(height: 12),
        _card(
          label: 'DELIVERY CHANNELS',
          child: Column(
            children: [
              _toggleRow(
                label: 'Push notifications',
                subtitle: 'Mobile and desktop',
                value: _notifPush,
                onChanged: (v) => setState(() => _notifPush = v),
              ),
              _divider(),
              _toggleRow(
                label: 'Email',
                subtitle: _emailCtrl.text,
                value: _notifEmail,
                onChanged: (v) => setState(() => _notifEmail = v),
              ),
              _divider(),
              _toggleRow(
                label: 'SMS',
                subtitle: '+254 ··· ····',
                value: _notifSms,
                onChanged: (v) => setState(() => _notifSms = v),
              ),
            ],
          ),
        ),
        const SizedBox(height: 24),
        _saveButton('Save notification settings'),
      ],
    );
  }

  // ═════════════════════════════════════════════════════════════════════════
  // TAB 5 — Preferences
  // ═════════════════════════════════════════════════════════════════════════
  Widget _buildPreferencesTab(bool isWide) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _sectionHeader(
          'App preferences',
          'Personalise how FlowerScout looks and behaves.',
          Icons.tune_rounded,
          _C.canopy,
        ),
        const SizedBox(height: 24),
        _card(
          label: 'APPEARANCE',
          child: Column(
            children: [
              _labeledDropdown(
                label: 'THEME',
                value: _theme,
                items: ['System default', 'Light', 'Dark'],
                onChanged: (v) => setState(() => _theme = v!),
              ),
              const SizedBox(height: 14),
              _labeledDropdown(
                label: 'DATE FORMAT',
                value: _dateFormat,
                items: ['DD/MM/YYYY', 'MM/DD/YYYY', 'YYYY-MM-DD (ISO)'],
                onChanged: (v) => setState(() => _dateFormat = v!),
              ),
            ],
          ),
        ),
        const SizedBox(height: 12),
        _card(
          label: 'MAP DEFAULTS',
          child: Column(
            children: [
              _labeledDropdown(
                label: 'DEFAULT VIEW',
                value: _mapDefault,
                items: ['Satellite', 'Terrain', 'Street'],
                onChanged: (v) => setState(() => _mapDefault = v!),
              ),
              _divider(),
              _toggleRow(
                label: 'Show heatmap on load',
                subtitle: 'Auto-display scouting heatmap when opening Maps',
                value: _heatmapOnLoad,
                onChanged: (v) => setState(() => _heatmapOnLoad = v),
              ),
            ],
          ),
        ),
        const SizedBox(height: 12),
        _card(
          label: 'ABOUT',
          child: Column(
            children: [
              _settingRow(
                label: 'FlowerScout',
                subtitle: 'Version 1.0.0 · Flutter',
                trailing: _statusBadge('Latest'),
              ),
              _divider(),
              _settingRow(
                label: 'Sign out',
                subtitle: 'Log out of FlowerScout',
                trailing: const Icon(Icons.logout_rounded,
                    color: Color(0xFFD32F2F), size: 18),
                labelColor: const Color(0xFFD32F2F),
                onTap: () => _confirmSignOut(),
              ),
            ],
          ),
        ),
        const SizedBox(height: 24),
        _saveButton('Save preferences'),
      ],
    );
  }

  // ═════════════════════════════════════════════════════════════════════════
  // Shared widgets
  // ═════════════════════════════════════════════════════════════════════════
  Widget _sectionHeader(
      String title, String subtitle, IconData icon, Color color) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          width: 44,
          height: 44,
          decoration: BoxDecoration(
            color: color.withValues(alpha: 0.12),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Icon(icon, color: color, size: 22),
        ),
        const SizedBox(width: 14),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(title,
                  style: const TextStyle(
                    fontFamily: 'Georgia',
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                    color: _C.ink,
                  )),
              const SizedBox(height: 3),
              Text(subtitle,
                  style: _T.body.copyWith(fontSize: 13, color: _C.slate)),
            ],
          ),
        ),
      ],
    );
  }

  Widget _card({required String label, required Widget child}) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: _C.paper,
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: _C.divider),
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
          Text(label, style: _T.label),
          const SizedBox(height: 16),
          child,
        ],
      ),
    );
  }

  Widget _toggleRow({
    required String label,
    required String subtitle,
    required bool value,
    required ValueChanged<bool> onChanged,
  }) {
    return Row(
      children: [
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(label,
                  style: _T.body.copyWith(
                      color: _C.ink, fontWeight: FontWeight.w500)),
              const SizedBox(height: 2),
              Text(subtitle,
                  style: _T.body.copyWith(fontSize: 12, color: _C.slate)),
            ],
          ),
        ),
        const SizedBox(width: 12),
        Switch.adaptive(
          value: value,
          activeColor: _C.leaf,
          onChanged: onChanged,
        ),
      ],
    );
  }

  Widget _settingRow({
    required String label,
    required String subtitle,
    required Widget trailing,
    Color? labelColor,
    VoidCallback? onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(label,
                    style: _T.body.copyWith(
                      color: labelColor ?? _C.ink,
                      fontWeight: FontWeight.w500,
                    )),
                const SizedBox(height: 2),
                Text(subtitle,
                    style: _T.body.copyWith(fontSize: 12, color: _C.slate)),
              ],
            ),
          ),
          trailing,
        ],
      ),
    );
  }

  Widget _styledTextField({
    required String label,
    required TextEditingController controller,
    String hint = '',
    TextInputType keyboardType = TextInputType.text,
    bool obscure = false,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 2, bottom: 6),
          child: Text(label, style: _T.label),
        ),
        Container(
          decoration: BoxDecoration(
            color: _C.cream,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: _C.divider),
          ),
          child: TextField(
            controller: controller,
            keyboardType: keyboardType,
            obscureText: obscure,
            style: _T.body,
            decoration: InputDecoration(
              hintText: hint,
              hintStyle: _T.body.copyWith(color: _C.slate),
              border: InputBorder.none,
              contentPadding:
                  const EdgeInsets.symmetric(horizontal: 14, vertical: 14),
            ),
          ),
        ),
      ],
    );
  }

  Widget _labeledDropdown({
    required String label,
    required String value,
    required List<String> items,
    required ValueChanged<String?> onChanged,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 2, bottom: 6),
          child: Text(label, style: _T.label),
        ),
        Container(
          decoration: BoxDecoration(
            color: _C.paper,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: _C.divider),
          ),
          child: DropdownButtonHideUnderline(
            child: DropdownButton<String>(
              value: value,
              isExpanded: true,
              padding:
                  const EdgeInsets.symmetric(horizontal: 14, vertical: 2),
              borderRadius: BorderRadius.circular(12),
              icon: const Icon(Icons.keyboard_arrow_down_rounded,
                  color: _C.graphite),
              items: items
                  .map((i) => DropdownMenuItem(
                        value: i,
                        child: Text(i,
                            style: _T.body
                                .copyWith(fontWeight: FontWeight.w500)),
                      ))
                  .toList(),
              onChanged: onChanged,
            ),
          ),
        ),
      ],
    );
  }

  Widget _miniDropdown({
    required String value,
    required List<String> items,
    required ValueChanged<String?> onChanged,
  }) {
    return Container(
      decoration: BoxDecoration(
        color: _C.fog,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: _C.divider),
      ),
      child: DropdownButtonHideUnderline(
        child: DropdownButton<String>(
          value: value,
          isDense: true,
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
          borderRadius: BorderRadius.circular(8),
          icon: const Icon(Icons.keyboard_arrow_down_rounded,
              color: _C.slate, size: 16),
          style: _T.body.copyWith(fontSize: 13),
          items: items
              .map((i) => DropdownMenuItem(value: i, child: Text(i)))
              .toList(),
          onChanged: onChanged,
        ),
      ),
    );
  }

  Widget _saveButton(String label,
      {IconData icon = Icons.check_rounded, Color color = _C.forest}) {
    return SizedBox(
      width: double.infinity,
      height: 52,
      child: Material(
        color: color,
        borderRadius: BorderRadius.circular(14),
        child: InkWell(
          borderRadius: BorderRadius.circular(14),
          onTap: () {
            HapticFeedback.mediumImpact();
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                backgroundColor: _C.forest,
                behavior: SnackBarBehavior.floating,
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12)),
                content: Row(
                  children: [
                    const Icon(Icons.check_circle, color: _C.mint),
                    const SizedBox(width: 10),
                    Text('$label saved',
                        style: const TextStyle(color: Colors.white)),
                  ],
                ),
                duration: const Duration(seconds: 2),
              ),
            );
          },
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, color: Colors.white, size: 18),
              const SizedBox(width: 8),
              Text(label,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 15,
                    fontWeight: FontWeight.w600,
                  )),
            ],
          ),
        ),
      ),
    );
  }

  Widget _outlineBtn(String label, VoidCallback onTap) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
        decoration: BoxDecoration(
          color: _C.fog,
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: _C.divider),
        ),
        child: Text(label,
            style: _T.body.copyWith(fontSize: 13, color: _C.graphite)),
      ),
    );
  }

  Widget _iconBtn(IconData icon, VoidCallback onTap) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 30,
        height: 30,
        decoration: BoxDecoration(
          color: _C.fog,
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: _C.divider),
        ),
        child: Icon(icon, size: 16, color: _C.graphite),
      ),
    );
  }

  Widget _statusBadge(String text, {Color color = _C.leaf}) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.12),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Text(
        text,
        style: TextStyle(
          fontSize: 11,
          fontWeight: FontWeight.w700,
          color: color == _C.leaf ? _C.forest : color,
        ),
      ),
    );
  }

  Widget _divider() => const Padding(
        padding: EdgeInsets.symmetric(vertical: 12),
        child: Divider(height: 0.5, thickness: 0.5, color: _C.divider),
      );

  Widget _versionBadge() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: _C.fog,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Text('v1.0.0',
          style: _T.label.copyWith(fontSize: 11, color: _C.slate)),
    );
  }

  void _confirmSignOut() {
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: const Text('Sign out?',
            style: TextStyle(fontFamily: 'Georgia', fontSize: 18)),
        content: const Text('You will need to log in again to access FlowerScout.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Sign out',
                style: TextStyle(color: Color(0xFFD32F2F))),
          ),
        ],
      ),
    );
  }

  // ── Tab metadata ──────────────────────────────────────────────────────────
  ({String label, IconData icon}) _tabMeta(_Tab tab) => switch (tab) {
        _Tab.farms         => (label: 'Farm config',    icon: Icons.agriculture_rounded),
        _Tab.profile       => (label: 'Profile',        icon: Icons.person_rounded),
        _Tab.team          => (label: 'Team',           icon: Icons.group_rounded),
        _Tab.notifications => (label: 'Notifications',  icon: Icons.notifications_rounded),
        _Tab.preferences   => (label: 'Preferences',    icon: Icons.tune_rounded),
      };
}
