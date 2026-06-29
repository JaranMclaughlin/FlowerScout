import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../../features/auth/presentation/login_screen.dart';
import '../../features/dashboard/presentation/dashboard_screen.dart';
import '../../features/scouting/presentation/scouting_screen.dart';
import '../../features/maps/presentation/maps_screen.dart';
import '../../features/reports/presentation/reports_screen.dart';
import '../../features/settings/presentation/settings_screen.dart';
import '../theme/app_colors.dart' show AppColors;
import '../../core/theme/app_theme.dart' show AppSizes;
import '../providers/shell_tab_provider.dart';
import '../providers/locale_provider.dart';
import '../l10n/app_strings.dart';
import '../../core/session/user_session.dart';

class AppShell extends ConsumerStatefulWidget {
  const AppShell({super.key});
  @override
  ConsumerState<AppShell> createState() => _AppShellState();
}

class _AppShellState extends ConsumerState<AppShell> {
  static const _pages = [
    DashboardScreen(),
    ScoutingScreen(),
    MapsScreen(),
    ReportsScreen(),
    SettingsScreen(),
  ];

  // Tabs visible to scouts: Dashboard, Scouting, Settings only
  // Tabs visible to managers/admins: all five
  List<_NavItem> _navItems(AppStrings s, bool isScout) {
    final all = [
      _NavItem(Icons.dashboard_rounded,  Icons.dashboard_outlined,  s.navDashboard, 0),
      _NavItem(Icons.grass_rounded,      Icons.grass_outlined,      s.navScouting,  1),
      _NavItem(Icons.map_rounded,        Icons.map_outlined,        s.navMaps,      2),
      _NavItem(Icons.bar_chart_rounded,  Icons.bar_chart_outlined,  s.navReports,   3),
      _NavItem(Icons.settings_rounded,   Icons.settings_outlined,   s.navSettings,  4),
    ];
    if (isScout) return [all[0], all[1], all[4]]; // Dashboard, Scouting, Settings
    return all;
  }

  @override
  Widget build(BuildContext context) {
    final s = ref.watch(stringsProvider);
    final profile = UserSession.currentProfile;
    final isScout = profile == UserProfile.scout;
    final items = _navItems(s, isScout);

    // Clamp tab index so scouts don't land on a hidden tab
    final rawIndex = ref.watch(selectedTabProvider);
    final validPageIndices = items.map((i) => i.pageIndex).toList();
    final currentPageIndex = validPageIndices.contains(rawIndex)
        ? rawIndex
        : items.first.pageIndex;

    final isTablet = MediaQuery.of(context).size.width >= 600;
    return isTablet
        ? _tabletLayout(s, items, currentPageIndex)
        : _phoneLayout(s, items, currentPageIndex);
  }

  void _setIndex(int pageIndex) =>
      ref.read(selectedTabProvider.notifier).set(pageIndex);

  // ── Phone ─────────────────────────────────────────────────────────────────
  Widget _phoneLayout(AppStrings s, List<_NavItem> items, int currentPageIndex) {
    return Scaffold(
      body: _pages[currentPageIndex],
      bottomNavigationBar: NavigationBarTheme(
        data: NavigationBarThemeData(
          height: 58,
          labelTextStyle: WidgetStateProperty.resolveWith((states) {
            final selected = states.contains(WidgetState.selected);
            return TextStyle(
              fontSize: 10.5,
              fontWeight: selected ? FontWeight.w600 : FontWeight.w400,
              color: selected ? AppColors.leaf : AppColors.muted,
            );
          }),
          iconTheme: WidgetStateProperty.resolveWith((states) {
            final selected = states.contains(WidgetState.selected);
            return IconThemeData(
              size: 20,
              color: selected ? AppColors.leaf : AppColors.muted,
            );
          }),
        ),
        child: NavigationBar(
          selectedIndex: items.indexWhere((i) => i.pageIndex == currentPageIndex),
          onDestinationSelected: (i) => _setIndex(items[i].pageIndex),
          backgroundColor: Colors.white,
          indicatorColor: AppColors.leaf.withValues(alpha: 0.15),
          labelBehavior: NavigationDestinationLabelBehavior.onlyShowSelected,
          destinations: items.map((item) => NavigationDestination(
            icon: Icon(item.iconOutlined),
            selectedIcon: Icon(item.icon),
            label: item.label,
          )).toList(),
        ),
      ),
    );
  }

  // ── Tablet/Desktop ────────────────────────────────────────────────────────
  Widget _tabletLayout(AppStrings s, List<_NavItem> items, int currentPageIndex) {
    final isExtended = MediaQuery.of(context).size.width >= 800;
    return Scaffold(
      body: Row(
        children: [
          NavigationRailTheme(
            data: const NavigationRailThemeData(
              selectedIconTheme: IconThemeData(color: AppColors.leaf, size: 20),
              unselectedIconTheme: IconThemeData(color: AppColors.muted, size: 20),
              selectedLabelTextStyle: TextStyle(
                  color: AppColors.leaf, fontWeight: FontWeight.w600, fontSize: 12),
              unselectedLabelTextStyle: TextStyle(color: AppColors.muted, fontSize: 12),
            ),
            child: NavigationRail(
              selectedIndex: items.indexWhere((i) => i.pageIndex == currentPageIndex),
              onDestinationSelected: (i) => _setIndex(items[i].pageIndex),
              backgroundColor: Colors.white,
              extended: isExtended,
              minWidth: 64,
              minExtendedWidth: 180,
              indicatorColor: AppColors.leaf.withValues(alpha: 0.15),
              groupAlignment: -1.0,
              leading: Padding(
                padding: const EdgeInsets.symmetric(vertical: 12),
                child: Container(
                  width: 36, height: 36,
                  decoration: BoxDecoration(
                    color: const Color(0xFFE1F5EE),
                    shape: BoxShape.circle,
                    border: Border.all(color: const Color(0xFF9FE1CB)),
                  ),
                  child: const Icon(Icons.local_florist,
                      color: AppColors.leaf, size: 18),
                ),
              ),
              trailing: Expanded(
                child: Align(
                  alignment: Alignment.bottomCenter,
                  child: Padding(
                    padding: const EdgeInsets.only(bottom: AppSizes.space2xl),
                    child: _signOutButton(s, isExtended),
                  ),
                ),
              ),
              destinations: items.map((item) => NavigationRailDestination(
                icon: Icon(item.iconOutlined),
                selectedIcon: Icon(item.icon),
                label: Text(item.label),
              )).toList(),
            ),
          ),
          const VerticalDivider(thickness: 0.5, width: 0.5),
          Expanded(child: _pages[currentPageIndex]),
        ],
      ),
    );
  }

  Widget _signOutButton(AppStrings s, bool extended) {
    return Tooltip(
      message: s.signOut,
      child: InkWell(
        borderRadius: BorderRadius.circular(AppSizes.radiusMd),
        onTap: () async {
          final confirm = await showDialog<bool>(
            context: context,
            builder: (_) => AlertDialog(
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(AppSizes.radiusLg)),
              title: Text(s.signOutConfirm,
                  style: const TextStyle(fontFamily: 'Georgia', fontSize: 18)),
              content: Text(s.signOutMsg),
              actions: [
                TextButton(
                    onPressed: () => Navigator.pop(context, false),
                    child: Text(s.cancel)),
                TextButton(
                  onPressed: () => Navigator.pop(context, true),
                  child: Text(s.signOut,
                      style: const TextStyle(color: AppColors.critical)),
                ),
              ],
            ),
          );
          if (confirm == true) {
            await Supabase.instance.client.auth.signOut();
            if (!mounted) return;
            Navigator.of(context).pushAndRemoveUntil(
              MaterialPageRoute(builder: (_) => const LoginScreen()),
              (route) => false,
            );
          }
        },
        child: Container(
          padding: EdgeInsets.symmetric(
              horizontal: extended ? 14 : 8, vertical: 8),
          decoration: BoxDecoration(
            color: const Color(0xFFFEF2F2),
            borderRadius: BorderRadius.circular(AppSizes.radiusMd),
          ),
          child: extended
              ? Row(mainAxisSize: MainAxisSize.min, children: [
                  const Icon(Icons.logout_rounded, color: AppColors.critical, size: 18),
                  const SizedBox(width: 6),
                  Text(s.signOut,
                      style: const TextStyle(
                          color: AppColors.critical,
                          fontSize: 12,
                          fontWeight: FontWeight.w600)),
                ])
              : const Icon(Icons.logout_rounded, color: AppColors.critical, size: 18),
        ),
      ),
    );
  }
}

class _NavItem {
  final IconData icon;
  final IconData iconOutlined;
  final String label;
  final int pageIndex;
  const _NavItem(this.icon, this.iconOutlined, this.label, this.pageIndex);
}


