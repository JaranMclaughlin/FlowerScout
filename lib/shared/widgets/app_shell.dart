import 'package:flutter/material.dart';
import '../../features/dashboard/presentation/dashboard_screen.dart';
import '../../features/scouting/presentation/scouting_screen.dart';
import '../../features/maps/presentation/maps_screen.dart';
import '../../features/reports/presentation/reports_screen.dart';
import '../../features/settings/presentation/settings_screen.dart';

class AppShell extends StatefulWidget {
  const AppShell({super.key});
  @override
  State<AppShell> createState() => _AppShellState();
}

class _AppShellState extends State<AppShell> {
  int _index = 0;

  static const _pages = [
    DashboardScreen(),
    ScoutingScreen(),
    MapsScreen(),
    ReportsScreen(),
    SettingsScreen(),
  ];

  static const _items = [
    _NavItem(Icons.dashboard_rounded,      Icons.dashboard_outlined,      'Dashboard'),
    _NavItem(Icons.grass_rounded,          Icons.grass_outlined,          'Scouting'),
    _NavItem(Icons.map_rounded,            Icons.map_outlined,            'Maps'),
    _NavItem(Icons.bar_chart_rounded,      Icons.bar_chart_outlined,      'Reports'),
    _NavItem(Icons.settings_rounded,       Icons.settings_outlined,       'Settings'),
  ];

  @override
  Widget build(BuildContext context) {
    final isTablet = MediaQuery.of(context).size.shortestSide >= 600;
    return isTablet ? _tabletLayout() : _phoneLayout();
  }

  // ── Phone — bottom navigation bar ────────────────────────
  Widget _phoneLayout() {
    return Scaffold(
      body: _pages[_index],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _index,
        onDestinationSelected: (i) => setState(() => _index = i),
        backgroundColor: Colors.white,
        indicatorColor: const Color(0xFF1D9E75).withValues(alpha: 0.15),
        labelBehavior:
            NavigationDestinationLabelBehavior.onlyShowSelected,
        destinations: _items.map((item) => NavigationDestination(
          icon: Icon(item.iconOutlined, color: const Color(0xFF888780)),
          selectedIcon: Icon(item.icon, color: const Color(0xFF1D9E75)),
          label: item.label,
        )).toList(),
      ),
    );
  }

  // ── Tablet — sidebar navigation ───────────────────────────
  Widget _tabletLayout() {
    return Scaffold(
      body: Row(
        children: [
          NavigationRail(
            selectedIndex: _index,
            onDestinationSelected: (i) =>
                setState(() => _index = i),
            backgroundColor: Colors.white,
            extended: MediaQuery.of(context).size.width >= 800,
            indicatorColor:
                const Color(0xFF1D9E75).withValues(alpha: 0.15),
            selectedIconTheme: const IconThemeData(
                color: Color(0xFF1D9E75)),
            unselectedIconTheme: const IconThemeData(
                color: Color(0xFF888780)),
            selectedLabelTextStyle: const TextStyle(
                color: Color(0xFF1D9E75),
                fontWeight: FontWeight.w600),
            unselectedLabelTextStyle:
                const TextStyle(color: Color(0xFF888780)),
            leading: Padding(
              padding: const EdgeInsets.symmetric(vertical: 16),
              child: Column(children: [
                Container(
                  width: 40, height: 40,
                  decoration: BoxDecoration(
                    color: const Color(0xFFE1F5EE),
                    shape: BoxShape.circle,
                    border: Border.all(
                        color: const Color(0xFF9FE1CB)),
                  ),
                  child: const Icon(Icons.local_florist,
                      color: Color(0xFF1D9E75), size: 20),
                ),
              ]),
            ),
            destinations: _items.map((item) =>
              NavigationRailDestination(
                icon: Icon(item.iconOutlined),
                selectedIcon: Icon(item.icon),
                label: Text(item.label),
              ),
            ).toList(),
          ),
          const VerticalDivider(thickness: 0.5, width: 0.5),
          Expanded(child: _pages[_index]),
        ],
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
