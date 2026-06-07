import 'package:flutter/material.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7F4),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(28),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [
                    Color(0xFF2E7D32),
                    Color(0xFF43A047),
                  ],
                ),
                borderRadius: BorderRadius.circular(24),
              ),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Farm Health Score',
                    style: TextStyle(
                      color: Colors.white70,
                      fontSize: 18,
                    ),
                  ),
                  SizedBox(height: 12),
                  Text(
                    '87%',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 56,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(height: 6),
                  Text(
                    'Excellent Condition • +4% This Week',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 16,
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 30),

            const Text(
              'Farm Overview',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 20),

            GridView.extent(
              maxCrossAxisExtent: 280,
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              crossAxisSpacing: 18,
              mainAxisSpacing: 18,
              childAspectRatio: 1.3,
              children: const [
                DashboardCard(
                  title: 'Active Scouts',
                  value: '8',
                  icon: Icons.people,
                  color: Color(0xFF2E7D32),
                ),
                DashboardCard(
                  title: 'Critical Issues',
                  value: '4',
                  icon: Icons.warning_amber_rounded,
                  color: Colors.orange,
                ),
                DashboardCard(
                  title: 'Disease Reports',
                  value: '25',
                  icon: Icons.coronavirus,
                  color: Colors.red,
                ),
                DashboardCard(
                  title: 'Pest Reports',
                  value: '17',
                  icon: Icons.bug_report,
                  color: Colors.purple,
                ),
              ],
            ),
                        const SizedBox(height: 30),

            const Text(
              'Quick Actions',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 16),

            Wrap(
              spacing: 12,
              runSpacing: 12,
              children: const [
                ActionButton(
                  icon: Icons.add_circle_outline,
                  label: 'New Report',
                ),
                ActionButton(
                  icon: Icons.map_outlined,
                  label: 'Open Maps',
                ),
                ActionButton(
                  icon: Icons.analytics_outlined,
                  label: 'Analytics',
                ),
                ActionButton(
                  icon: Icons.download_outlined,
                  label: 'Export Report',
                ),
              ],
            ),

            const SizedBox(height: 35),

            const Text(
              'Recent Activity',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 16),

            const ActivityTile(
              icon: Icons.assignment_turned_in,
              title: 'Scout John submitted inspection report',
            ),

            const ActivityTile(
              icon: Icons.warning,
              title: 'Greenhouse GH-13 flagged as critical',
            ),

            const ActivityTile(
              icon: Icons.bug_report,
              title: 'Pest outbreak detected in GH-08',
            ),

            const ActivityTile(
              icon: Icons.description,
              title: 'Weekly farm report generated',
            ),

            const SizedBox(height: 35),

            const Text(
              'Areas Requiring Attention',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 16),

            const AttentionCard(
              greenhouse: 'GH-13',
              issue: 'Powdery Mildew',
              severity: 'Critical',
              color: Colors.red,
            ),

            const SizedBox(height: 12),

            const AttentionCard(
              greenhouse: 'GH-08',
              issue: 'Red Spider Mite',
              severity: 'High',
              color: Colors.orange,
            ),

            const SizedBox(height: 12),

            const AttentionCard(
              greenhouse: 'GH-21',
              issue: 'Water Stress',
              severity: 'Medium',
              color: Colors.blue,
            ),
          ],
        ),
      ),
    );
  }
}
class DashboardCard extends StatelessWidget {
  final String title;
  final String value;
  final IconData icon;
  final Color color;

  const DashboardCard({
    super.key,
    required this.title,
    required this.value,
    required this.icon,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(22),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 12,
            offset: const Offset(0, 5),
          ),
        ],
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            icon,
            color: color,
            size: 36,
          ),
          const SizedBox(height: 10),
          Text(
            value,
            style: const TextStyle(
              fontSize: 28,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 6),
          Text(
            title,
            textAlign: TextAlign.center,
            style: const TextStyle(fontSize: 13),
          ),
        ],
      ),
    );
  }
}

class ActionButton extends StatelessWidget {
  final IconData icon;
  final String label;

  const ActionButton({
    super.key,
    required this.icon,
    required this.label,
  });

  @override
  Widget build(BuildContext context) {
    return ElevatedButton.icon(
      onPressed: () {},
      icon: Icon(icon),
      label: Text(label),
    );
  }
}

class ActivityTile extends StatelessWidget {
  final IconData icon;
  final String title;

  const ActivityTile({
    super.key,
    required this.icon,
    required this.title,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: Icon(icon),
        title: Text(title),
      ),
    );
  }
}

class AttentionCard extends StatelessWidget {
  final String greenhouse;
  final String issue;
  final String severity;
  final Color color;

  const AttentionCard({
    super.key,
    required this.greenhouse,
    required this.issue,
    required this.severity,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: color.withOpacity(0.15),
          child: Icon(
            Icons.location_on,
            color: color,
          ),
        ),
        title: Text(greenhouse),
        subtitle: Text(issue),
        trailing: Text(
          severity,
          style: TextStyle(
            color: color,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }
}