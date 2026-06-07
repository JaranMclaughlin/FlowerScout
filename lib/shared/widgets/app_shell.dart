import 'package:flutter/material.dart';

import '../../features/dashboard/presentation/dashboard_screen.dart';
import '../../features/scouting/presentation/scouting_screen.dart';
import '../../features/maps/presentation/maps_screen.dart';
import '../../features/reports/presentation/reports_screen.dart';
import '../../features/analytics/presentation/analytics_screen.dart';
import '../../features/settings/presentation/settings_screen.dart';

class AppShell extends StatefulWidget {
  const AppShell({super.key});

  @override
  State<AppShell> createState() => _AppShellState();
}

class _AppShellState extends State<AppShell> {
  int selectedIndex = 0;

  final List<Widget> pages = const [
    DashboardScreen(),
    ScoutingScreen(),
    MapsScreen(),
    ReportsScreen(),
    AnalyticsScreen(),
    SettingsScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF4F7F2),
      body: Row(
        children: [
          _buildSidebar(),
          _buildMainContent(),
        ],
      ),
    );
  }

  // ================= SIDEBAR =================
  Widget _buildSidebar() {
    return Container(
      width: 260,
      decoration: const BoxDecoration(
        color: Colors.white,
        border: Border(
          right: BorderSide(color: Color(0xFFEAEAEA)),
        ),
      ),
      child: Column(
        children: [
          const SizedBox(height: 30),

          // Logo
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: const Color(0xFFE8F5E9),
              borderRadius: BorderRadius.circular(20),
            ),
            child: const Icon(
              Icons.local_florist,
              color: Color(0xFF2E7D32),
              size: 40,
            ),
          ),

          const SizedBox(height: 16),

          const Text(
            'FlowerScout',
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),

          const Text(
            'Kongoni River Farm',
            style: TextStyle(color: Colors.grey),
          ),

          const SizedBox(height: 30),

          // Navigation
          Expanded(
            child: ListView(
              padding: EdgeInsets.zero,
              children: [
                _navItem(Icons.dashboard, 'Dashboard', 0),
                _navItem(Icons.search, 'Scouting', 1),
                _navItem(Icons.map, 'Maps', 2),
                _navItem(Icons.description, 'Reports', 3),
                _navItem(Icons.analytics, 'Analytics', 4),
                _navItem(Icons.settings, 'Settings', 5),
              ],
            ),
          ),

          // User card
          Container(
            margin: const EdgeInsets.all(16),
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: const Color(0xFFE8F5E9),
              borderRadius: BorderRadius.circular(18),
            ),
            child: const Row(
              children: [
                CircleAvatar(
                  backgroundColor: Color(0xFF2E7D32),
                  child: Icon(Icons.person, color: Colors.white),
                ),
                SizedBox(width: 12),
                Expanded(
                  child: Text(
                    'Farm Manager',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  // ================= MAIN CONTENT =================
  Widget _buildMainContent() {
    return Expanded(
      child: Column(
        children: [
          _buildTopBar(),

          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: pages[selectedIndex],
            ),
          ),
        ],
      ),
    );
  }

  // ================= TOP BAR =================
  Widget _buildTopBar() {
    return Container(
      height: 70,
      padding: const EdgeInsets.symmetric(horizontal: 24),
      alignment: Alignment.centerLeft,
      decoration: const BoxDecoration(
        color: Colors.white,
        border: Border(
          bottom: BorderSide(color: Color(0xFFEAEAEA)),
        ),
      ),
      child: const Text(
        'FlowerScout',
        style: TextStyle(
          fontSize: 22,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }

  // ================= NAV ITEM =================
  Widget _navItem(IconData icon, String title, int index) {
    final selected = selectedIndex == index;

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      child: InkWell(
        borderRadius: BorderRadius.circular(14),
        onTap: () {
          setState(() {
            selectedIndex = index;
          });
        },
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
          decoration: BoxDecoration(
            color: selected ? const Color(0xFFE8F5E9) : Colors.transparent,
            borderRadius: BorderRadius.circular(14),
          ),
          child: Row(
            children: [
              Icon(
                icon,
                color:
                    selected ? const Color(0xFF2E7D32) : Colors.black54,
              ),
              const SizedBox(width: 12),
              Text(
                title,
                style: TextStyle(
                  fontSize: 16,
                  fontWeight:
                      selected ? FontWeight.bold : FontWeight.normal,
                  color:
                      selected ? const Color(0xFF2E7D32) : Colors.black87,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}