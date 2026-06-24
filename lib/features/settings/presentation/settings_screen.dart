import 'package:flutter/material.dart';
import '../../auth/presentation/login_screen.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../../../shared/providers/farm_providers.dart';
import '../../../shared/providers/locale_provider.dart';
import '../../../shared/l10n/app_strings.dart';
import '../../../shared/providers/farm_repository.dart';

// ── Design tokens ─────────────────────────────────────────────────────────────
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
}

class _T {
  static const heading = TextStyle(fontFamily: 'Georgia', fontSize: 20,
      fontWeight: FontWeight.w600, color: _C.ink, letterSpacing: -0.3);
  static const label = TextStyle(fontSize: 12, fontWeight: FontWeight.w600,
      color: _C.slate, letterSpacing: 1.0);
  static const body = TextStyle(fontSize: 14, color: _C.graphite, height: 1.5);
}

enum _Tab { farms, profile, team, notifications, preferences }

// ── Main screen ───────────────────────────────────────────────────────────────
class SettingsScreen extends ConsumerStatefulWidget {
  const SettingsScreen({super.key});
  @override
  ConsumerState<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends ConsumerState<SettingsScreen> {
  _Tab _activeTab = _Tab.farms;

  // Profile controllers — populated from Supabase
  late TextEditingController _nameCtrl;
  late TextEditingController _emailCtrl;
  late TextEditingController _phoneCtrl;
  bool _profileLoaded = false;

  // Notification toggles
  bool _notifOverdue  = true;
  bool _notifCritical = true;
  bool _notifWeekly   = false;
  bool _notifPush     = true;
  bool _notifEmail    = true;
  bool _notifSms      = false;

  // Preferences
  String _theme      = s.systemDefault;
  String _dateFormat = 'DD/MM/YYYY';
  String _mapDefault = 'Satellite';
  bool   _heatmap    = true;
  int    _interval   = 7;

  // Team invite
  final _inviteCtrl = TextEditingController();
  String _inviteRole = 'scout';

  @override
  void initState() {
    super.initState();
    _nameCtrl  = TextEditingController();
    _emailCtrl = TextEditingController();
    _phoneCtrl = TextEditingController();
  }

  @override
  void dispose() {
    _nameCtrl.dispose();
    _emailCtrl.dispose();
    _phoneCtrl.dispose();
    _inviteCtrl.dispose();
    super.dispose();
  }

  // Role visibility helpers
  bool get _isAdmin {
    final profile = ref.read(profileProvider).value;
    return profile?.role == 'system_admin';
  }
  bool get _isManager {
    final profile = ref.read(profileProvider).value;
    return profile?.role == 'manager' || profile?.role == 'system_admin';
  }

  AppStrings get s => AppStrings.of(ref.watch(localeProvider));

  @override
  Widget build(BuildContext context) {
    // Populate profile fields once loaded
    final profileAsync = ref.watch(profileProvider);
    profileAsync.whenData((profile) {
      if (profile != null && !_profileLoaded) {
        _nameCtrl.text  = profile.fullName;
        _emailCtrl.text = ref.read(supabaseClientProvider).auth.currentUser?.email ?? '';
        _phoneCtrl.text = profile.phone ?? '';
        _profileLoaded  = true;
      }
    });

    return Scaffold(
      backgroundColor: _C.cream,
      body: SafeArea(
        child: LayoutBuilder(builder: (context, constraints) {
          final isWide = constraints.maxWidth >= 900;
          return isWide ? _wideLayout() : _narrowLayout();
        }),
      ),
    );
  }

  // ── Wide layout ───────────────────────────────────────────────────────────
  Widget _wideLayout() => Row(children: [
    _buildRail(),
    const VerticalDivider(thickness: 0.5, width: 0.5, color: _C.divider),
    Expanded(child: _buildContent(true)),
  ]);

  Widget _buildRail() => Container(
    width: 200,
    color: _C.paper,
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(20, 28, 20, 16),
          child: Text(s.settingsTitle, style: const TextStyle(fontFamily: 'Georgia',
              fontSize: 22, fontWeight: FontWeight.w700, color: _C.ink)),
        ),
        const Divider(height: 0.5, thickness: 0.5, color: _C.divider),
        const SizedBox(height: 8),
        ..._visibleTabs().map(_railItem),
        const Spacer(),
        Padding(padding: const EdgeInsets.all(16), child: _versionBadge()),
      ],
    ),
  );

  Widget _railItem(_Tab tab) {
    final active = _activeTab == tab;
    final meta = _tabMeta(tab);
    return GestureDetector(
      onTap: () => setState(() => _activeTab = tab),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 180),
        margin: const EdgeInsets.symmetric(horizontal: 10, vertical: 2),
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
        decoration: BoxDecoration(
          color: active ? _C.leaf.withValues(alpha: 0.1) : Colors.transparent,
          borderRadius: BorderRadius.circular(12),
          border: Border(left: BorderSide(
            color: active ? _C.leaf : Colors.transparent, width: 3)),
        ),
        child: Row(children: [
          Icon(meta.icon, size: 18, color: active ? _C.leaf : _C.slate),
          const SizedBox(width: 10),
          Expanded(child: Text(meta.label, style: _T.body.copyWith(
            color: active ? _C.forest : _C.slate,
            fontWeight: active ? FontWeight.w600 : FontWeight.w400,
          ), overflow: TextOverflow.ellipsis)),
        ]),
      ),
    );
  }

  // ── Narrow layout ─────────────────────────────────────────────────────────
  Widget _narrowLayout() => Column(children: [
    _buildTopBar(),
    Expanded(child: _buildContent(false)),
  ]);

  Widget _buildTopBar() => Container(
    color: _C.paper,
    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Padding(
        padding: const EdgeInsets.fromLTRB(20, 20, 20, 12),
        child: Text(s.settingsTitle, style: const TextStyle(fontFamily: 'Georgia',
            fontSize: 22, fontWeight: FontWeight.w700, color: _C.ink)),
      ),
      SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.symmetric(horizontal: 16),
        child: Row(children: _visibleTabs().map(_topBarChip).toList()),
      ),
      const Divider(height: 0.5, thickness: 0.5, color: _C.divider),
    ]),
  );

  Widget _topBarChip(_Tab tab) {
    final active = _activeTab == tab;
    final meta = _tabMeta(tab);
    return GestureDetector(
      onTap: () => setState(() => _activeTab = tab),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 180),
        margin: const EdgeInsets.only(right: 6, bottom: 8),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
        decoration: BoxDecoration(
          color: active ? _C.leaf.withValues(alpha: 0.12) : _C.fog,
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: active
              ? _C.leaf.withValues(alpha: 0.4) : Colors.transparent),
        ),
        child: Row(mainAxisSize: MainAxisSize.min, children: [
          Icon(meta.icon, size: 15, color: active ? _C.leaf : _C.slate),
          const SizedBox(width: 6),
          Text(meta.label, style: _T.body.copyWith(
            fontSize: 13,
            color: active ? _C.forest : _C.slate,
            fontWeight: active ? FontWeight.w600 : FontWeight.w400,
          )),
        ]),
      ),
    );
  }

  // ── Visible tabs based on role ────────────────────────────────────────────
  List<_Tab> _visibleTabs() {
    final all = _Tab.values.toList();
    if (_isAdmin) return all;
    if (_isManager) return all; // manager sees all but RLS filters data
    // Scout: no farm config, no team
    return [_Tab.profile, _Tab.notifications, _Tab.preferences];
  }

  // ── Content router ────────────────────────────────────────────────────────
  Widget _buildContent(bool isWide) => SingleChildScrollView(
    padding: EdgeInsets.symmetric(
        horizontal: isWide ? 36 : 20, vertical: 28),
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

  // ═══════════════════════════════════════════════════════════════════════════
  // TAB 1 — Farm config (live from Supabase via RLS)
  // ═══════════════════════════════════════════════════════════════════════════
  Widget _buildFarmsTab(bool isWide) {
    final farmsAsync = ref.watch(farmsProvider);

    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      _sectionHeader(s.farmGhConfigTitle,
          s.farmGhConfigDesc,
          Icons.agriculture_rounded, _C.leaf),
      const SizedBox(height: 24),

      farmsAsync.when(
        loading: () => const _LoadingCard(message: s.loadingFarms),
        error:   (e, _) => _ErrorCard(message: e.toString(),
            onRetry: () => ref.read(farmsProvider.notifier).refresh()),
        data: (farms) => farms.isEmpty
            ? const _EmptyCard(message: s.noFarmsAssigned)
            : Column(children: [
                ...farms.map((farm) => _farmCard(farm, isWide)),
                const SizedBox(height: 16),
                _card(
                  label: 'INSPECTION DEFAULTS',
                  child: Column(children: [
                    _settingRow(
                      label: s.inspectionInterval,
                      subtitle: s.inspectionIntervalDesc,
                      trailing: Row(mainAxisSize: MainAxisSize.min, children: [
                        _iconBtn(Icons.remove_rounded, () {
                          if (_interval > 1) setState(() => _interval--);
                        }),
                        SizedBox(width: 36,
                          child: Text('$_interval',
                            textAlign: TextAlign.center,
                            style: _T.body.copyWith(
                              fontWeight: FontWeight.w700, color: _C.forest))),
                        _iconBtn(Icons.add_rounded, () {
                          if (_interval < 30) setState(() => _interval++);
                        }),
                      ]),
                    ),
                    _divider(),
                    _settingRow(
                      label: s.refreshData,
                      subtitle: s.refreshDataDesc,
                      trailing: _outlineBtn('Refresh', () =>
                          ref.read(farmsProvider.notifier).refresh()),
                    ),
                  ]),
                ),
              ]),
      ),
      const SizedBox(height: 24),
    ]);
  }

  Widget _farmCard(FarmModel farm, bool isWide) {
    final activeCount = farm.greenhouses.where((g) => g.isActive).length;
    final total       = farm.greenhouses.length;
    final expanded    = ValueNotifier(true);

    return ValueListenableBuilder<bool>(
      valueListenable: expanded,
      builder: (_, isExpanded, __) => Container(
        margin: const EdgeInsets.only(bottom: 12),
        decoration: BoxDecoration(
          color: _C.paper, borderRadius: BorderRadius.circular(18),
          border: Border.all(color: _C.divider),
          boxShadow: [BoxShadow(color: Colors.black.withValues(alpha: 0.03),
              blurRadius: 8, offset: const Offset(0, 2))],
        ),
        child: Column(children: [
          // Farm header
          GestureDetector(
            onTap: () => expanded.value = !isExpanded,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
              decoration: BoxDecoration(
                color: isExpanded
                    ? _C.leaf.withValues(alpha: 0.06) : Colors.transparent,
                borderRadius: isExpanded
                    ? const BorderRadius.vertical(top: Radius.circular(18))
                    : BorderRadius.circular(18),
              ),
              child: Row(children: [
                Container(width: 40, height: 40,
                  decoration: BoxDecoration(
                    color: _C.mist, borderRadius: BorderRadius.circular(10)),
                  child: const Icon(Icons.agriculture_rounded,
                      color: _C.leaf, size: 20)),
                const SizedBox(width: 14),
                Expanded(child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(farm.name, style: _T.body.copyWith(
                      fontWeight: FontWeight.w600, color: _C.ink, fontSize: 15)),
                    const SizedBox(height: 2),
                    Text('$activeCount of $total greenhouses active',
                        style: _T.body.copyWith(fontSize: 12, color: _C.slate)),
                  ],
                )),
                // Medium badges
                if (farm.greenhouses.any((g) => g.medium == 'HYDROPONIC'))
                  _mediumBadge('HYDRO', const Color(0xFF0277BD)),
                if (farm.greenhouses.any((g) => g.medium == 'SOIL'))
                  _mediumBadge('SOIL', _C.leaf),
                const SizedBox(width: 8),
                _statusBadge(activeCount == total ? 'Active' : 'Partial'),
                const SizedBox(width: 8),
                AnimatedRotation(
                  turns: isExpanded ? 0.5 : 0,
                  duration: const Duration(milliseconds: 200),
                  child: const Icon(Icons.keyboard_arrow_down_rounded,
                      color: _C.slate)),
              ]),
            ),
          ),
          // Greenhouse list
          AnimatedSize(
            duration: const Duration(milliseconds: 250),
            curve: Curves.easeOut,
            child: isExpanded
                ? Column(children: [
                    const Divider(height: 0.5, thickness: 0.5, color: _C.divider),
                    ...farm.greenhouses.map((gh) =>
                      _greenhouseRow(gh, farm.greenhouses.last == gh)),
                  ])
                : const SizedBox.shrink(),
          ),
        ]),
      ),
    );
  }

  Widget _greenhouseRow(GreenhouseModel gh, bool isLast) {
    final medColor = gh.medium == 'HYDROPONIC'
        ? const Color(0xFF0277BD) : gh.medium == 'OUTSOURCED'
        ? _C.slate : _C.leaf;

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 11),
      decoration: BoxDecoration(border: isLast ? null
          : const Border(bottom: BorderSide(color: _C.divider, width: 0.5))),
      child: Row(children: [
        const SizedBox(width: 8),
        Container(width: 6, height: 6,
          decoration: BoxDecoration(shape: BoxShape.circle,
            color: gh.isActive ? _C.leaf : _C.slate)),
        const SizedBox(width: 12),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
          decoration: BoxDecoration(color: _C.fog,
              borderRadius: BorderRadius.circular(6)),
          child: Text(gh.code, style: _T.label.copyWith(
              fontSize: 11, color: _C.graphite)),
        ),
        const SizedBox(width: 8),
        Container(width: 4, height: 4,
          decoration: BoxDecoration(shape: BoxShape.circle, color: medColor)),
        const SizedBox(width: 6),
        Expanded(
          child: Text(gh.varietyNames.take(3).join(' · ')
              + (gh.varietyNames.length > 3
                  ? ' +${gh.varietyNames.length - 3}' : ''),
            style: _T.body.copyWith(fontSize: 12, color: _C.graphite),
            overflow: TextOverflow.ellipsis),
        ),
        Transform.scale(
          scale: 0.82,
          child: Switch.adaptive(
            value: gh.isActive,
            activeColor: _C.leaf,
            onChanged: _isManager
                ? (v) => ref.read(farmsProvider.notifier)
                    .toggleGreenhouse(gh.id, v)
                : null,
          ),
        ),
      ]),
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // TAB 2 — Profile (live from Supabase)
  // ═══════════════════════════════════════════════════════════════════════════
  Widget _buildProfileTab(bool isWide) {
    final profileAsync = ref.watch(profileProvider);
    return profileAsync.when(
      loading: () => const _LoadingCard(message: s.loadingProfile),
      error:   (e, _) => _ErrorCard(message: e.toString(),
          onRetry: () => ref.read(profileProvider.notifier).refresh()),
      data: (profile) => Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _sectionHeader(s.yourProfile,
              s.yourProfileDesc,
              Icons.person_rounded, _C.canopy),
          const SizedBox(height: 24),
          _card(label: s.personalInfo, child: Column(children: [
            // Avatar row
            Row(children: [
              Container(width: 56, height: 56,
                decoration: BoxDecoration(color: _C.mist,
                  shape: BoxShape.circle,
                  border: Border.all(color: _C.mint, width: 2)),
                child: Center(child: Text(
                  _initials(profile?.fullName ?? ''),
                  style: const TextStyle(fontSize: 18,
                    fontWeight: FontWeight.w700, color: _C.forest),
                )),
              ),
              const SizedBox(width: 16),
              Expanded(child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(profile?.fullName ?? '',
                    style: _T.body.copyWith(
                      fontWeight: FontWeight.w600, color: _C.ink)),
                  Text(_roleLabel(profile?.role ?? 'scout'),
                    style: _T.body.copyWith(fontSize: 12, color: _C.slate)),
                ],
              )),
            ]),
            _divider(),
            _styledTextField(label: s.fullName, controller: _nameCtrl),
            const SizedBox(height: 14),
            _styledTextField(label: s.emailLabel, controller: _emailCtrl,
                keyboardType: TextInputType.emailAddress),
            const SizedBox(height: 14),
            _styledTextField(label: s.phone, controller: _phoneCtrl,
                keyboardType: TextInputType.phone),
          ])),
          const SizedBox(height: 24),
          _saveButton(s.saveProfile, onTap: () async {
            await ref.read(profileProvider.notifier).save(
              fullName: _nameCtrl.text.trim(),
              phone: _phoneCtrl.text.trim().isEmpty
                  ? null : _phoneCtrl.text.trim(),
            );
          }),
        ],
      ),
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // TAB 3 — Team (live, manager/admin only, RLS filtered)
  // ═══════════════════════════════════════════════════════════════════════════
  Widget _buildTeamTab(bool isWide) {
    final teamAsync = ref.watch(teamProvider);
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      _sectionHeader(s.teamManagement,
          s.teamManagementDesc,
          Icons.group_rounded, _C.canopy),
      const SizedBox(height: 24),
      teamAsync.when(
        loading: () => const _LoadingCard(message: s.loadingTeam),
        error:   (e, _) => _ErrorCard(message: e.toString(), onRetry: () {
          ref.invalidate(teamProvider);
        }),
        data: (members) => _card(
          label: 'TEAM MEMBERS (${members.length})',
          child: members.isEmpty
              ? const _EmptyCard(message: s.noTeamMembers)
              : Column(
                  children: members.asMap().entries.map((e) {
                    final m = e.value;
                    final isLast = e.key == members.length - 1;
                    return _memberRow(m, isLast);
                  }).toList(),
                ),
        ),
      ),
      const SizedBox(height: 12),
      if (_isAdmin) _card(
        label: 'INVITE A NEW MEMBER',
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          if (isWide)
            Row(children: [
              Expanded(child: _styledTextField(label: 'EMAIL',
                  controller: _inviteCtrl, hint: 'colleague@farm.co.ke',
                  keyboardType: TextInputType.emailAddress)),
              const SizedBox(width: 14),
              SizedBox(width: 160, child: _labeledDropdown(
                label: 'ROLE', value: _inviteRole,
                items: ['scout', 'viewer', 'manager'],
                onChanged: (v) => setState(() => _inviteRole = v!),
              )),
            ])
          else ...[
            _styledTextField(label: 'EMAIL', controller: _inviteCtrl,
                hint: 'colleague@farm.co.ke',
                keyboardType: TextInputType.emailAddress),
            const SizedBox(height: 14),
            _labeledDropdown(label: 'ROLE', value: _inviteRole,
                items: const ['Scout', 'Viewer', 'Manager'],
                onChanged: (v) => setState(() => _inviteRole = v!)),
          ],
          const SizedBox(height: 16),
          _saveButton(s.sendInvite,
              icon: Icons.send_rounded, color: _C.canopy),
        ]),
      ),
    ]);
  }

  Widget _memberRow(UserProfileModel m, bool isLast) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 12),
      decoration: BoxDecoration(border: isLast ? null
          : const Border(bottom: BorderSide(color: _C.divider, width: 0.5))),
      child: Row(children: [
        Container(width: 38, height: 38,
          decoration: const BoxDecoration(color: _C.mist, shape: BoxShape.circle),
          child: Center(child: Text(_initials(m.fullName),
            style: const TextStyle(fontSize: 13,
                fontWeight: FontWeight.w700, color: _C.forest)))),
        const SizedBox(width: 12),
        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(m.fullName, style: _T.body.copyWith(
                fontWeight: FontWeight.w600, color: _C.ink)),
            Text(_roleLabel(m.role),
                style: _T.body.copyWith(fontSize: 12, color: _C.slate)),
          ],
        )),
        _statusBadge(_roleLabel(m.role),
            color: m.role == 'system_admin' ? const Color(0xFF7F77DD) : _C.leaf),
      ]),
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // TAB 4 — Notifications
  // ═══════════════════════════════════════════════════════════════════════════
  Widget _buildNotificationsTab() => Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      _sectionHeader(s.notificationsAlerts,
          s.controlNotif,
          Icons.notifications_rounded, _C.canopy),
      const SizedBox(height: 24),
      _card(label: s.inspectionAlerts, child: Column(children: [
        _toggleRow(s.overdueReminder,
            s.overdueDesc,
            _notifOverdue, (v) => setState(() => _notifOverdue = v)),
        _divider(),
        _toggleRow(s.criticalAlert,
            s.criticalAlertDesc,
            _notifCritical, (v) => setState(() => _notifCritical = v)),
        _divider(),
        _toggleRow(s.weeklySummary,
            s.weeklyDescFull,
            _notifWeekly, (v) => setState(() => _notifWeekly = v)),
      ])),
      const SizedBox(height: 12),
      _card(label: s.deliveryChannels, child: Column(children: [
        _toggleRow(s.pushNotifications, s.pushDesc,
            _notifPush, (v) => setState(() => _notifPush = v)),
        _divider(),
        _toggleRow('Email', _emailCtrl.text.isEmpty
            ? s.notSet : _emailCtrl.text,
            _notifEmail, (v) => setState(() => _notifEmail = v)),
        _divider(),
        _toggleRow('SMS', s.addPhoneForSms,
            _notifSms, (v) => setState(() => _notifSms = v)),
      ])),
      const SizedBox(height: 24),
      _saveButton(s.saveNotifSettings),
    ],
  );

  // ═══════════════════════════════════════════════════════════════════════════
  // TAB 5 — Preferences
  // ═══════════════════════════════════════════════════════════════════════════
  Widget _buildPreferencesTab(bool isWide) => Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      _sectionHeader(s.appPreferences,
          s.personaliseDesc,
          Icons.tune_rounded, _C.canopy),
      const SizedBox(height: 24),
      Consumer(builder: (context, ref, _) {
        final lang = ref.watch(localeProvider);
        final s    = ref.watch(stringsProvider);
        return _card(label: s.language, child: Row(children: [
          Expanded(child: GestureDetector(
            onTap: () => ref.read(localeProvider.notifier).setLanguage('en'),
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 180),
              padding: const EdgeInsets.symmetric(vertical: 12),
              alignment: Alignment.center,
              decoration: BoxDecoration(
                color: lang == 'en' ? _C.leaf : Colors.white,
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: lang == 'en' ? _C.leaf : _C.divider),
              ),
              child: Text('🇬🇧  ', style: TextStyle(fontSize: 13,
                  fontWeight: FontWeight.w600,
                  color: lang == 'en' ? Colors.white : _C.slate)),
            ),
          )),
          const SizedBox(width: 10),
          Expanded(child: GestureDetector(
            onTap: () => ref.read(localeProvider.notifier).setLanguage('sw'),
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 180),
              padding: const EdgeInsets.symmetric(vertical: 12),
              alignment: Alignment.center,
              decoration: BoxDecoration(
                color: lang == 'sw' ? _C.leaf : Colors.white,
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: lang == 'sw' ? _C.leaf : _C.divider),
              ),
              child: Text('🇰🇪  ', style: TextStyle(fontSize: 13,
                  fontWeight: FontWeight.w600,
                  color: lang == 'sw' ? Colors.white : _C.slate)),
            ),
          )),
        ]));
      }),
      const SizedBox(height: 12),
      _card(label: 'APPEARANCE', child: Column(children: [
        _labeledDropdown(label: 'THEME', value: _theme,
            items: [s.systemDefault, 'Light', 'Dark'],
            onChanged: (v) => setState(() => _theme = v!)),
        const SizedBox(height: 14),
        _labeledDropdown(label: 'DATE FORMAT', value: _dateFormat,
            items: ['DD/MM/YYYY', 'MM/DD/YYYY', 'YYYY-MM-DD (ISO)'],
            onChanged: (v) => setState(() => _dateFormat = v!)),
      ])),
      const SizedBox(height: 12),
      _card(label: 'MAP DEFAULTS', child: Column(children: [
        _labeledDropdown(label: 'DEFAULT VIEW', value: _mapDefault,
            items: ['Satellite', 'Terrain', 'Street'],
            onChanged: (v) => setState(() => _mapDefault = v!)),
        _divider(),
        _toggleRow(s.showHeatmap,
            s.showHeatmapDesc,
            _heatmap, (v) => setState(() => _heatmap = v)),
      ])),
      const SizedBox(height: 12),
      _card(label: 'ABOUT', child: Column(children: [
        _settingRow(label: 'FlowerScout', subtitle: s.versionLabel,
            trailing: _statusBadge('Latest')),
        _divider(),
        _settingRow(
          label: s.signOutLabel,
          subtitle: s.logOut,
          labelColor: const Color(0xFFD32F2F),
          trailing: const Icon(Icons.logout_rounded,
              color: Color(0xFFD32F2F), size: 18),
          onTap: _confirmSignOut,
        ),
      ])),
      const SizedBox(height: 24),
      _saveButton(s.savePreferences),
    ],
  );

  // ═══════════════════════════════════════════════════════════════════════════
  // Shared widgets
  // ═══════════════════════════════════════════════════════════════════════════

  Widget _sectionHeader(String title, String subtitle,
      IconData icon, Color color) {
    return Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Container(width: 44, height: 44,
        decoration: BoxDecoration(color: color.withValues(alpha: 0.12),
            borderRadius: BorderRadius.circular(12)),
        child: Icon(icon, color: color, size: 22)),
      const SizedBox(width: 14),
      Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: const TextStyle(fontFamily: 'Georgia',
              fontSize: 18, fontWeight: FontWeight.w600, color: _C.ink)),
          const SizedBox(height: 3),
          Text(subtitle, style: _T.body.copyWith(fontSize: 13, color: _C.slate)),
        ],
      )),
    ]);
  }

  Widget _card({required String label, required Widget child}) =>
    Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: _C.paper, borderRadius: BorderRadius.circular(18),
        border: Border.all(color: _C.divider),
        boxShadow: [BoxShadow(color: Colors.black.withValues(alpha: 0.03),
            blurRadius: 8, offset: const Offset(0, 2))],
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(label, style: _T.label),
        const SizedBox(height: 16),
        child,
      ]),
    );

  Widget _toggleRow(String label, String subtitle,
      bool value, ValueChanged<bool> onChanged) =>
    Row(children: [
      Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label, style: _T.body.copyWith(
              color: _C.ink, fontWeight: FontWeight.w500)),
          const SizedBox(height: 2),
          Text(subtitle, style: _T.body.copyWith(fontSize: 12, color: _C.slate)),
        ],
      )),
      const SizedBox(width: 12),
      Switch.adaptive(value: value, activeColor: _C.leaf, onChanged: onChanged),
    ]);

  Widget _settingRow({required String label, required String subtitle,
      required Widget trailing, Color? labelColor, VoidCallback? onTap}) =>
    GestureDetector(onTap: onTap,
      child: Row(children: [
        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(label, style: _T.body.copyWith(
              color: labelColor ?? _C.ink, fontWeight: FontWeight.w500)),
            const SizedBox(height: 2),
            Text(subtitle, style: _T.body.copyWith(
                fontSize: 12, color: _C.slate)),
          ],
        )),
        trailing,
      ]),
    );

  Widget _styledTextField({required String label,
      required TextEditingController controller, String hint = '',
      TextInputType keyboardType = TextInputType.text,
      bool obscure = false}) =>
    Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Padding(padding: const EdgeInsets.only(left: 2, bottom: 6),
          child: Text(label, style: _T.label)),
      Container(
        decoration: BoxDecoration(color: _C.cream,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: _C.divider)),
        child: TextField(
          controller: controller, keyboardType: keyboardType,
          obscureText: obscure, style: _T.body,
          decoration: InputDecoration(hintText: hint,
            hintStyle: _T.body.copyWith(color: _C.slate),
            border: InputBorder.none,
            contentPadding: const EdgeInsets.symmetric(
                horizontal: 14, vertical: 14)),
        ),
      ),
    ]);

  Widget _labeledDropdown({required String label, required String value,
      required List<String> items, required ValueChanged<String?> onChanged}) =>
    Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Padding(padding: const EdgeInsets.only(left: 2, bottom: 6),
          child: Text(label, style: _T.label)),
      Container(
        decoration: BoxDecoration(color: _C.paper,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: _C.divider)),
        child: DropdownButtonHideUnderline(child: DropdownButton<String>(
          value: value, isExpanded: true,
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 2),
          borderRadius: BorderRadius.circular(12),
          icon: const Icon(Icons.keyboard_arrow_down_rounded, color: _C.graphite),
          items: items.map((i) => DropdownMenuItem(value: i,
            child: Text(i, style: _T.body.copyWith(
                fontWeight: FontWeight.w500)))).toList(),
          onChanged: onChanged,
        )),
      ),
    ]);

  Widget _saveButton(String label, {IconData icon = Icons.check_rounded,
      Color color = _C.forest, VoidCallback? onTap}) =>
    SizedBox(width: double.infinity, height: 52,
      child: Material(color: color, borderRadius: BorderRadius.circular(14),
        child: InkWell(
          borderRadius: BorderRadius.circular(14),
          onTap: onTap ?? () {
            HapticFeedback.mediumImpact();
            ScaffoldMessenger.of(context).showSnackBar(SnackBar(
              backgroundColor: _C.forest,
              behavior: SnackBarBehavior.floating,
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12)),
              content: Row(children: [
                const Icon(Icons.check_circle, color: _C.mint),
                const SizedBox(width: 10),
                Text('$label saved',
                    style: const TextStyle(color: Colors.white)),
              ]),
              duration: const Duration(seconds: 2),
            ));
          },
          child: Row(mainAxisAlignment: MainAxisAlignment.center, children: [
            Icon(icon, color: Colors.white, size: 18),
            const SizedBox(width: 8),
            Text(label, style: const TextStyle(color: Colors.white,
                fontSize: 15, fontWeight: FontWeight.w600)),
          ]),
        ),
      ),
    );

  Widget _outlineBtn(String label, VoidCallback onTap) => GestureDetector(
    onTap: onTap,
    child: Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(color: _C.fog,
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: _C.divider)),
      child: Text(label, style: _T.body.copyWith(
          fontSize: 13, color: _C.graphite)),
    ),
  );

  Widget _iconBtn(IconData icon, VoidCallback onTap) => GestureDetector(
    onTap: onTap,
    child: Container(width: 30, height: 30,
      decoration: BoxDecoration(color: _C.fog,
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: _C.divider)),
      child: Icon(icon, size: 16, color: _C.graphite)),
  );

  Widget _statusBadge(String text, {Color color = _C.leaf}) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
    decoration: BoxDecoration(color: color.withValues(alpha: 0.12),
        borderRadius: BorderRadius.circular(20)),
    child: Text(text, style: TextStyle(fontSize: 11,
        fontWeight: FontWeight.w700,
        color: color == _C.leaf ? _C.forest : color)),
  );

  Widget _mediumBadge(String label, Color color) => Container(
    margin: const EdgeInsets.only(right: 4),
    padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
    decoration: BoxDecoration(color: color.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(4),
        border: Border.all(color: color.withValues(alpha: 0.2))),
    child: Text(label, style: TextStyle(fontSize: 9,
        fontWeight: FontWeight.w700, color: color)),
  );

  Widget _divider() => const Padding(
    padding: EdgeInsets.symmetric(vertical: 12),
    child: Divider(height: 0.5, thickness: 0.5, color: _C.divider));

  Widget _versionBadge() => Container(
    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
    decoration: BoxDecoration(color: _C.fog,
        borderRadius: BorderRadius.circular(8)),
    child: Text('v1.0.0', style: _T.label.copyWith(
        fontSize: 11, color: _C.slate)));

  void _confirmSignOut() {
    showDialog(context: context, builder: (_) => AlertDialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      title: const Text(s.signOutQ, style: TextStyle(
          fontFamily: 'Georgia', fontSize: 18)),
      content: const Text(
          'You will need to log in again to access FlowerScout.'),
      actions: [
        TextButton(onPressed: () => Navigator.pop(context),
            child: const Text('Cancel')),
        TextButton(
          onPressed: () async {
            Navigator.pop(context);
            await Supabase.instance.client.auth.signOut();
            if (context.mounted) {
              Navigator.of(context).pushAndRemoveUntil(
                MaterialPageRoute(builder: (_) => const LoginScreen()),
                (route) => false,
              );
            }
          },
          child: const Text(s.signOutLabel,
              style: TextStyle(color: Color(0xFFD32F2F))),
        ),
      ],
    ));
  }

  // ── Helpers ───────────────────────────────────────────────────────────────
  String _initials(String name) {
    final parts = name.trim().split(' ')
        .where((p) => p.isNotEmpty).toList();
    if (parts.isEmpty) return '?';
    if (parts.length == 1) return parts[0][0].toUpperCase();
    return '${parts[0][0]}${parts.last[0]}'.toUpperCase();
  }

  String _roleLabel(String role) => switch (role) {
    'system_admin' => s.systemAdmin,
    'manager'      => s.roleManager,
    'scout'        => s.roleScout,
    'viewer'       => s.roleViewer,
    _              => role,
  };

  ({String label, IconData icon}) _tabMeta(_Tab tab) => switch (tab) {
    _Tab.farms         => (label: s.tabFarms,   icon: Icons.agriculture_rounded),
    _Tab.profile       => (label: s.tabProfile,       icon: Icons.person_rounded),
    _Tab.team          => (label: s.tabTeam,          icon: Icons.group_rounded),
    _Tab.notifications => (label: s.tabNotifications, icon: Icons.notifications_rounded),
    _Tab.preferences   => (label: s.tabPreferences,  icon: Icons.tune_rounded),
  };
}

// ── Helper widgets ────────────────────────────────────────────────────────────

class _LoadingCard extends StatelessWidget {
  final String message;
  const _LoadingCard({required this.message});
  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.all(32),
    alignment: Alignment.center,
    child: Column(children: [
      const CircularProgressIndicator(color: Color(0xFF40916C), strokeWidth: 2),
      const SizedBox(height: 16),
      Text(message, style: const TextStyle(
          fontSize: 13, color: Color(0xFF6B7F6E))),
    ]),
  );
}

class _ErrorCard extends StatelessWidget {
  final String message;
  final VoidCallback onRetry;
  const _ErrorCard({required this.message, required this.onRetry});
  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.all(20),
    decoration: BoxDecoration(
      color: const Color(0xFFFEF2F2),
      borderRadius: BorderRadius.circular(14),
      border: Border.all(color: const Color(0xFFFECACA)),
    ),
    child: Column(children: [
      const Icon(Icons.error_outline_rounded,
          color: Color(0xFFD32F2F), size: 28),
      const SizedBox(height: 8),
      Text(message, style: const TextStyle(
          fontSize: 13, color: Color(0xFF991B1B)), textAlign: TextAlign.center),
      const SizedBox(height: 12),
      TextButton.icon(onPressed: onRetry,
        icon: const Icon(Icons.refresh_rounded, size: 16),
        label: const Text('Retry'),
        style: TextButton.styleFrom(foregroundColor: const Color(0xFF40916C)),
      ),
    ]),
  );
}

class _EmptyCard extends StatelessWidget {
  final String message;
  const _EmptyCard({required this.message});
  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.symmetric(vertical: 20),
    child: Center(child: Text(message, style: const TextStyle(
        fontSize: 13, color: Color(0xFF6B7F6E)))),
  );
}

// WRITE_TEST
