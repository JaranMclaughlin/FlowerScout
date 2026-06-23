import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../../features/auth/presentation/login_screen.dart';
import '../../features/dashboard/presentation/dashboard_screen.dart';
import '../../features/scouting/presentation/scouting_screen.dart' hide AppColors;
import '../../features/maps/presentation/maps_screen.dart';
import '../../features/reports/presentation/reports_screen.dart';
import '../../features/settings/presentation/settings_screen.dart';
import '../theme/app_colors.dart' show AppColors;
import '../../core/theme/app_theme.dart' show AppSizes;
import '../providers/shell_tab_provider.dart';

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

  static const _items = [
    _NavItem(Icons.dashboard_rounded,   Icons.dashboard_outlined,   'Dashboard'),
    _NavItem(Icons.grass_rounded,       Icons.grass_outlined,       'Scouting'),
    _NavItem(Icons.map_rounded,         Icons.map_outlined,         'Maps'),
    _NavItem(Icons.bar_chart_rounded,   Icons.bar_chart_outlined,   'Reports'),
    _NavItem(Icons.settings_rounded,    Icons.settings_outlined,    'Settings'),
  ];

  @override
  Widget build(BuildContext context) {
    final isTablet = MediaQuery.of(context).size.width >= 600;
    return isTablet ? _tabletLayout() : _phoneLayout();
  }

  int get _index => ref.watch(selectedTabProvider);
  void _setIndex(int i) => ref.read(selectedTabProvider.notifier).set(i);

  // ── Phone — bottom nav, slightly smaller than Material default ─────────────
  Widget _phoneLayout() {
    return Scaffold(
      body: _pages[_index],
      bottomNavigationBar: NavigationBarTheme(
        data: NavigationBarThemeData(
          height: 58, // was default ~80
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
              size: 20, // was default 24
              color: selected ? AppColors.leaf : AppColors.muted,
            );
          }),
        ),
        child: NavigationBar(
          selectedIndex: _index,
          onDestinationSelected: _setIndex,
          backgroundColor: Colors.white,
          indicatorColor: AppColors.leaf.withValues(alpha: 0.15),
          labelBehavior: NavigationDestinationLabelBehavior.onlyShowSelected,
          destinations: _items.map((item) => NavigationDestination(
            icon: Icon(item.iconOutlined),
            selectedIcon: Icon(item.icon),
            label: item.label,
          )).toList(),
        ),
      ),
    );
  }

  // ── Tablet/Desktop — sidebar, narrower than before ──────────────────────────
  Widget _tabletLayout() {
    final isExtended = MediaQuery.of(context).size.width >= 800;
    return Scaffold(
      body: Row(
        children: [
          NavigationRailTheme(
            data: const NavigationRailThemeData(
              selectedIconTheme: IconThemeData(color: AppColors.leaf, size: 20),
              unselectedIconTheme: IconThemeData(color: AppColors.muted, size: 20),
              selectedLabelTextStyle: TextStyle(
                color: AppColors.leaf, fontWeight: FontWeight.w600, fontSize: 12,
              ),
              unselectedLabelTextStyle: TextStyle(color: AppColors.muted, fontSize: 12),
            ),
            child: NavigationRail(
              selectedIndex: _index,
              onDestinationSelected: _setIndex,
              backgroundColor: Colors.white,
              extended: isExtended,
              minWidth: 64,    // was default 72
              minExtendedWidth: 180, // was default 256
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
                    child: _signOutButton(isExtended),
                  ),
                ),
              ),
              destinations: _items.map((item) => NavigationRailDestination(
                icon: Icon(item.iconOutlined),
                selectedIcon: Icon(item.icon),
                label: Text(item.label),
              )).toList(),
            ),
          ),
          const VerticalDivider(thickness: 0.5, width: 0.5),
          Expanded(child: _pages[_index]),
        ],
      ),
    );
  }

  Widget _signOutButton(bool extended) {
    return Tooltip(
      message: 'Sign out',
      child: InkWell(
        borderRadius: BorderRadius.circular(AppSizes.radiusMd),
        onTap: () async {
          final confirm = await showDialog<bool>(
            context: context,
            builder: (_) => AlertDialog(
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(AppSizes.radiusLg)),
              title: const Text('Sign out?',
                  style: TextStyle(fontFamily: 'Georgia', fontSize: 18)),
              content: const Text(
                  'You will need to log in again to access FlowerScout.'),
              actions: [
                TextButton(
                    onPressed: () => Navigator.pop(context, false),
                    child: const Text('Cancel')),
                TextButton(
                  onPressed: () => Navigator.pop(context, true),
                  child: const Text('Sign out',
                      style: TextStyle(color: AppColors.critical)),
                ),
              ],
            ),
          );
          if (confirm == true) {
            await Supabase.instance.client.auth.signOut();
            if (mounted) {
              Navigator.of(context).pushAndRemoveUntil(
                MaterialPageRoute(builder: (_) => const LoginScreen()),
                (route) => false,
              );
            }
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
              ? const Row(mainAxisSize: MainAxisSize.min, children: [
                  Icon(Icons.logout_rounded, color: AppColors.critical, size: 18),
                  SizedBox(width: 6),
                  Text('Sign out',
                      style: TextStyle(
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
  const _NavItem(this.icon, this.iconOutlined, this.label);
}
