import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import '../../../shared/l10n/app_strings.dart';
import '../../../shared/providers/locale_provider.dart';

class _C {
  static const forest = Color(0xFF1B4332);
  static const leaf = Color(0xFF40916C);
  static const mist = Color(0xFFD8F3DC);
  static const paper = Color(0xFFFFFFFF);
  static const ink = Color(0xFF0D1B0F);
  static const graphite = Color(0xFF3D4F42);
  static const slate = Color(0xFF6B7F6E);
  static const divider = Color(0xFFDDE5DD);
  static const amber = Color(0xFFF59E0B);
  static const red = Color(0xFFE53935);
}

class WeatherData {
  final double tempC;
  final String description;
  final String iconCode; // OpenWeatherMap icon id e.g. "01d"
  final double humidity;
  final double windKph;
  final DateTime fetchedAt;

  const WeatherData({
    required this.tempC,
    required this.description,
    required this.iconCode,
    required this.humidity,
    required this.windKph,
    required this.fetchedAt,
  });

  factory WeatherData.mock() => WeatherData(
        tempC: 24,
        description: 'Partly Cloudy',
        iconCode: '02d',
        humidity: 62,
        windKph: 14,
        fetchedAt: DateTime.now(),
      );

  factory WeatherData.fromJson(Map<String, dynamic> json) {
    final main = json['main'] as Map<String, dynamic>;
    final weather =
        (json['weather'] as List).first as Map<String, dynamic>;
    final wind = json['wind'] as Map<String, dynamic>;
    return WeatherData(
      tempC: (main['temp'] as num).toDouble() - 273.15,
      description: weather['description'] as String,
      iconCode: weather['icon'] as String,
      humidity: (main['humidity'] as num).toDouble(),
      windKph: ((wind['speed'] as num).toDouble() * 3.6),
      fetchedAt: DateTime.now(),
    );
  }
}

class NotificationItem {
  final String id;
  final String title;
  final String body;
  final IconData icon;
  final Color color;
  final DateTime time;
  bool isRead;

  NotificationItem({
    required this.id,
    required this.title,
    required this.body,
    required this.icon,
    required this.color,
    required this.time,
    this.isRead = false,
  });
}

//  WEATHER SERVICE

class WeatherService {
  //     Free tier: https://openweathermap.org/api
  //     Leave empty to use realistic mock data.
  static const _apiKey = '';

  // Default coordinates: Nairobi, Kenya (change to your farm location)
  static const _lat = -1.286389;
  static const _lon = 36.817223;

  static Future<WeatherData> fetch() async {
    if (_apiKey.isEmpty) return WeatherData.mock();
    try {
      final uri = Uri.parse(
        'https://api.openweathermap.org/data/2.5/weather'
        '?lat=$_lat&lon=$_lon&appid=$_apiKey',
      );
      final response = await http.get(uri).timeout(const Duration(seconds: 8));
      if (response.statusCode == 200) {
        return WeatherData.fromJson(
            jsonDecode(response.body) as Map<String, dynamic>);
      }
    } catch (_) {}
    return WeatherData.mock();
  }
}

//  WEATHER CHIP  (real-time, auto-refreshes every 10 min)

class WeatherChip extends StatefulWidget {
  const WeatherChip({super.key});

  @override
  State<WeatherChip> createState() => _WeatherChipState();
}

class _WeatherChipState extends State<WeatherChip>
    with SingleTickerProviderStateMixin {
  WeatherData? _weather;
  bool _loading = true;
  Timer? _refreshTimer;

  late AnimationController _pulseCtrl;
  late Animation<double> _pulseAnim;

  @override
  void initState() {
    super.initState();

    _pulseCtrl = AnimationController(
        vsync: this,
        duration: const Duration(milliseconds: 1200),
        lowerBound: 0.85,
        upperBound: 1.0)
      ..repeat(reverse: true);
    _pulseAnim = CurvedAnimation(parent: _pulseCtrl, curve: Curves.easeInOut);

    _fetchWeather();
    // Auto-refresh every 10 minutes
    _refreshTimer =
        Timer.periodic(const Duration(minutes: 10), (_) => _fetchWeather());
  }

  @override
  void dispose() {
    _refreshTimer?.cancel();
    _pulseCtrl.dispose();
    super.dispose();
  }

  Future<void> _fetchWeather() async {
    if (!mounted) return;
    setState(() => _loading = true);
    final data = await WeatherService.fetch();
    if (!mounted) return;
    setState(() {
      _weather = data;
      _loading = false;
      _pulseCtrl.stop();
    });
  }

  Widget _weatherIcon(String code, double size) {
    final isDay = code.endsWith('d');
    final condition = code.substring(0, 2);

    switch (condition) {
      case '01': // clear
        return Icon(Icons.wb_sunny_rounded,
            size: size, color: const Color(0xFFFDB813));
      case '02': // few clouds
        return Stack(
          alignment: Alignment.center,
          children: [
            Positioned(
              right: 0,
              top: 0,
              child: Icon(Icons.cloud_rounded,
                  size: size * 0.7, color: Colors.white70),
            ),
            Icon(Icons.wb_sunny_rounded,
                size: size * 0.8, color: const Color(0xFFFDB813)),
          ],
        );
      case '03':
      case '04': // clouds
        return Icon(Icons.cloud_rounded, size: size, color: Colors.white70);
      case '09':
      case '10': // rain
        return Icon(Icons.grain_rounded,
            size: size, color: const Color(0xFF90CAF9));
      case '11': // thunder
        return Icon(Icons.bolt_rounded,
            size: size, color: const Color(0xFFFDD835));
      case '13': // snow
        return Icon(Icons.ac_unit_rounded, size: size, color: Colors.white);
      case '50': // mist/fog
        return Icon(Icons.blur_on_rounded,
            size: size, color: Colors.white60);
      default:
        return Icon(isDay ? Icons.wb_sunny_rounded : Icons.nightlight_round,
            size: size, color: const Color(0xFFFDB813));
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading && _weather == null) {
      return ScaleTransition(
        scale: _pulseAnim,
        child: _chipShell(
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              SizedBox(
                width: 16,
                height: 16,
                child: CircularProgressIndicator(
                  strokeWidth: 2,
                  color: _C.leaf,
                ),
              ),
              Text(
                'Loading...',
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                  color: _C.graphite,
                ),
              ),
            ],
          ),
        ),
      );
    }

    final w = _weather!;
    return GestureDetector(
      onTap: () => _showWeatherDetail(context, w),
      child: _chipShell(
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            SizedBox(
              width: 22,
              height: 22,
              child: _weatherIcon(w.iconCode, 22),
            ),
            const SizedBox(width: 6),
            TweenAnimationBuilder<double>(
              tween: Tween(begin: w.tempC - 2, end: w.tempC),
              duration: const Duration(milliseconds: 800),
              curve: Curves.easeOut,
              builder: (_, val, _) => Text(
                '�C',
                style: const TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w700,
                  color: _C.ink,
                ),
              ),
            ),
            // Live indicator dot
            const SizedBox(width: 6),
            _LiveDot(),
          ],
        ),
      ),
    );
  }

  Widget _chipShell({required Widget child}) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: _C.paper,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: _C.divider, width: 1),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: child,
    );
  }

  void _showWeatherDetail(BuildContext context, WeatherData w) {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.transparent,
      builder: (_) => _WeatherDetailSheet(weather: w, iconBuilder: _weatherIcon),
    );
  }
}

//  LIVE DOT  (animated green pulse = data is live)

class _LiveDot extends StatefulWidget {
  @override
  State<_LiveDot> createState() => _LiveDotState();
}

class _LiveDotState extends State<_LiveDot> with SingleTickerProviderStateMixin {
  late AnimationController _ctrl;
  late Animation<double> _anim;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(
        vsync: this, duration: const Duration(milliseconds: 1600))
      ..repeat(reverse: true);
    _anim = CurvedAnimation(parent: _ctrl, curve: Curves.easeInOut);
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: _anim,
      child: Container(
        width: 6,
        height: 6,
        decoration: const BoxDecoration(
          shape: BoxShape.circle,
          color: _C.leaf,
        ),
      ),
    );
  }
}

//  WEATHER DETAIL BOTTOM SHEET

class _WeatherDetailSheet extends ConsumerWidget {
  final WeatherData weather;
  final Widget Function(String, double) iconBuilder;

  const _WeatherDetailSheet({
    required this.weather,
    required this.iconBuilder,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = AppStrings.of(ref.watch(localeProvider));
    final mins =
        DateTime.now().difference(weather.fetchedAt).inMinutes;
    final freshLabel = mins == 0 ? s.justNow : '${mins}m ago';

    return Container(
      margin: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: _C.paper,
        borderRadius: BorderRadius.circular(24),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.12),
            blurRadius: 30,
            offset: const Offset(0, -4),
          ),
        ],
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Handle
          Container(
            margin: const EdgeInsets.only(top: 12, bottom: 4),
            width: 40,
            height: 4,
            decoration: BoxDecoration(
              color: _C.divider,
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          // Header
          Container(
            margin: const EdgeInsets.all(16),
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              gradient: const LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [Color(0xFF1565C0), Color(0xFF0288D1)],
              ),
              borderRadius: BorderRadius.circular(18),
            ),
            child: Row(
              children: [
                SizedBox(
                    width: 56, height: 56,
                    child: iconBuilder(weather.iconCode, 48)),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '${weather.tempC.round()}°C',
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 36,
                          fontWeight: FontWeight.w800,
                          height: 1,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        weather.description
                            .split(' ')
                            .map((w) =>
                                w[0].toUpperCase() + w.substring(1))
                            .join(' '),
                        style: const TextStyle(
                          color: Colors.white70,
                          fontSize: 15,
                        ),
                      ),
                    ],
                  ),
                ),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    const Text('Nairobi',
                        style: TextStyle(
                            color: Colors.white, fontWeight: FontWeight.w600)),
                    const SizedBox(height: 4),
                    Row(
                      children: [
                        const Icon(Icons.sync_rounded,
                            size: 12, color: Colors.white54),
                        const SizedBox(width: 4),
                        Text(freshLabel,
                            style: const TextStyle(
                                color: Colors.white54, fontSize: 11)),
                      ],
                    ),
                  ],
                ),
              ],
            ),
          ),
          // Stats row
          Padding(
            padding:
                const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
            child: Row(
              children: [
                _StatTile(
                    icon: Icons.water_drop_rounded,
                    color: const Color(0xFF0288D1),
                    label: 'Humidity',
                    value: '${weather.humidity.round()}%'),
                const SizedBox(width: 12),
                _StatTile(
                    icon: Icons.air_rounded,
                    color: const Color(0xFF00838F),
                    label: 'Wind',
                    value: '${weather.windKph.round()} km/h'),
                const SizedBox(width: 12),
                _StatTile(
                    icon: Icons.thermostat_rounded,
                    color: const Color(0xFFE65100),
                    label: s.feelsLike,
                    value: '${weather.tempC.round()}°C'),
              ],
            ),
          ),
          const SizedBox(height: 20),
        ],
      ),
    );
  }
}

class _StatTile extends StatelessWidget {
  final IconData icon;
  final Color color;
  final String label;
  final String value;

  const _StatTile(
      {required this.icon,
      required this.color,
      required this.label,
      required this.value});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        padding:
            const EdgeInsets.symmetric(horizontal: 12, vertical: 14),
        decoration: BoxDecoration(
          color: color.withValues(alpha: 0.07),
          borderRadius: BorderRadius.circular(14),
          border: Border.all(color: color.withValues(alpha: 0.15)),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, size: 18, color: color),
            const SizedBox(height: 6),
            Text(value,
                style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w700,
                    color: _C.ink)),
            const SizedBox(height: 2),
            Text(label,
                style: TextStyle(fontSize: 11, color: _C.slate)),
          ],
        ),
      ),
    );
  }
}

//  NOTIFICATION BELL  (with badge, panel, mark-all-read)

class NotificationBell extends StatefulWidget {
  const NotificationBell({super.key});

  @override
  State<NotificationBell> createState() => _NotificationBellState();
}

class _NotificationBellState extends State<NotificationBell>
    with SingleTickerProviderStateMixin {
  late AnimationController _shakeCtrl;
  late Animation<double> _shakeAnim;

  final List<NotificationItem> _notifications = [
    NotificationItem(
      id: '1',
      title: 'High Severity Alert',
      body: 'Potential pest outbreak detected',
      icon: Icons.bug_report_rounded,
      color: _C.red,
      time: DateTime.now().subtract(const Duration(minutes: 8)),
    ),
    NotificationItem(
      id: '2',
      title: 'Inspection Due',
      body: 'North Farm GH-21 scheduled for today',
      icon: Icons.assignment_rounded,
      color: _C.amber,
      time: DateTime.now().subtract(const Duration(hours: 1)),
    ),
    NotificationItem(
      id: '3',
      title: 'Report Ready',
      body: 'Weekly scouting summary is ready to view',
      icon: Icons.bar_chart_rounded,
      color: _C.leaf,
      time: DateTime.now().subtract(const Duration(hours: 3)),
    ),
    NotificationItem(
      id: '4',
      title: 'Irrigation Alert',
      body: 'GH-03 moisture levels below threshold',
      icon: Icons.water_drop_rounded,
      color: const Color(0xFF0288D1),
      time: DateTime.now().subtract(const Duration(hours: 5)),
      isRead: true,
    ),
  ];

  int get _unread => _notifications.where((n) => !n.isRead).length;

  @override
  void initState() {
    super.initState();
    _shakeCtrl = AnimationController(
        vsync: this, duration: const Duration(milliseconds: 500));
    _shakeAnim = Tween<double>(begin: -0.05, end: 0.05).animate(
        CurvedAnimation(parent: _shakeCtrl, curve: Curves.elasticIn));

    // Shake bell on startup if there are unread notifications
    if (_unread > 0) {
      Future.delayed(const Duration(seconds: 1), () {
        if (mounted) _shakeCtrl.repeat(reverse: true);
        Future.delayed(const Duration(milliseconds: 800), () {
          if (mounted) _shakeCtrl.stop();
        });
      });
    }
  }

  @override
  void dispose() {
    _shakeCtrl.dispose();
    super.dispose();
  }

  void _markAllRead() {
    setState(() {
      for (final n in _notifications) {
        n.isRead = true;
      }
    });
  }

  void _showPanel(BuildContext context) {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.transparent,
      isScrollControlled: true,
      builder: (_) => StatefulBuilder(
        builder: (ctx, setSheetState) {
          return _NotificationPanel(
            notifications: _notifications,
            onMarkAllRead: () {
              _markAllRead();
              setSheetState(() {});
              setState(() {});
            },
            onMarkRead: (id) {
              setState(() {
                _notifications
                    .firstWhere((n) => n.id == id)
                    .isRead = true;
              });
              setSheetState(() {});
            },
            onDismiss: (id) {
              setState(() => _notifications.removeWhere((n) => n.id == id));
              setSheetState(() {});
            },
          );
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => _showPanel(context),
      child: AnimatedBuilder(
        animation: _shakeAnim,
        builder: (_, child) => Transform.rotate(
          angle: _shakeAnim.value,
          child: child,
        ),
        child: Container(
          width: 44,
          height: 44,
          decoration: BoxDecoration(
            color: _C.paper,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: _C.divider, width: 1),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.05),
                blurRadius: 8,
                offset: const Offset(0, 2),
              ),
            ],
          ),
          child: Stack(
            alignment: Alignment.center,
            children: [
              Icon(
                _unread > 0
                    ? Icons.notifications_rounded
                    : Icons.notifications_none_rounded,
                size: 22,
                color: _unread > 0 ? _C.forest : _C.slate,
              ),
              if (_unread > 0)
                Positioned(
                  top: 6,
                  right: 6,
                  child: AnimatedContainer(
                    duration: const Duration(milliseconds: 300),
                    width: _unread > 9 ? 18 : 14,
                    height: 14,
                    decoration: BoxDecoration(
                      color: _C.red,
                      borderRadius: BorderRadius.circular(7),
                      border: Border.all(color: _C.paper, width: 1.5),
                    ),
                    child: Center(
                      child: Text(
                        _unread > 9 ? '9+' : '$_unread',
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 8,
                          fontWeight: FontWeight.w800,
                          height: 1,
                        ),
                      ),
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}

//  NOTIFICATION PANEL (bottom sheet)

class _NotificationPanel extends ConsumerWidget {
  final List<NotificationItem> notifications;
  final VoidCallback onMarkAllRead;
  final ValueChanged<String> onMarkRead;
  final ValueChanged<String> onDismiss;

  const _NotificationPanel({
    required this.notifications,
    required this.onMarkAllRead,
    required this.onMarkRead,
    required this.onDismiss,
  });

  String _timeAgo(DateTime t, AppStrings s) {
    final diff = DateTime.now().difference(t);
    if (diff.inMinutes < 1) return s.justNow;
    if (diff.inMinutes < 60) return '${diff.inMinutes}m ago';
    if (diff.inHours < 24) return '${diff.inHours}h ago';
    return '${diff.inDays}d ago';
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = AppStrings.of(ref.watch(localeProvider));
    final unread = notifications.where((n) => !n.isRead).length;

    return DraggableScrollableSheet(
      initialChildSize: 0.65,
      minChildSize: 0.4,
      maxChildSize: 0.92,
      builder: (_, scrollCtrl) => Container(
        decoration: const BoxDecoration(
          color: _C.paper,
          borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
        ),
        child: Column(
          children: [
            // Handle
            Container(
              margin: const EdgeInsets.only(top: 12, bottom: 8),
              width: 40,
              height: 4,
              decoration: BoxDecoration(
                color: _C.divider,
                borderRadius: BorderRadius.circular(2),
              ),
            ),
            // Header
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
              child: Row(
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        s.navScouting == 'Ukaguzi' ? 'Arifa' : 'Notifications',
                        style: TextStyle(
                          fontFamily: 'Georgia',
                          fontSize: 20,
                          fontWeight: FontWeight.w700,
                          color: _C.ink,
                        ),
                      ),
                      if (unread > 0)
                        Text(
                          '$unread unread',
                          style: const TextStyle(
                              fontSize: 12, color: _C.slate),
                        ),
                    ],
                  ),
                  const Spacer(),
                  if (unread > 0)
                    TextButton.icon(
                      onPressed: onMarkAllRead,
                      icon: const Icon(Icons.done_all_rounded,
                          size: 16, color: _C.leaf),
                      label: Text(s.markAllRead,
                          style: TextStyle(
                              color: _C.leaf,
                              fontSize: 13,
                              fontWeight: FontWeight.w600)),
                    ),
                ],
              ),
            ),
            const Divider(height: 1, color: _C.divider),
            // List
            Expanded(
              child: notifications.isEmpty
                  ? _buildEmpty(s)
                  : ListView.separated(
                      controller: scrollCtrl,
                      padding: const EdgeInsets.symmetric(vertical: 8),
                      itemCount: notifications.length,
                      separatorBuilder: (_, _) => const Divider(
                          height: 1, indent: 72, color: _C.divider),
                      itemBuilder: (_, i) {
                        final n = notifications[i];
                        return Dismissible(
                          key: Key(n.id),
                          direction: DismissDirection.endToStart,
                          background: Container(
                            alignment: Alignment.centerRight,
                            color: _C.red.withValues(alpha: 0.1),
                            padding:
                                const EdgeInsets.only(right: 20),
                            child: const Icon(Icons.delete_rounded,
                                color: _C.red),
                          ),
                          onDismissed: (_) => onDismiss(n.id),
                          child: _NotificationTile(
                            item: n,
                            timeLabel: _timeAgo(n.time, s),
                            onTap: () => onMarkRead(n.id),
                          ),
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEmpty(AppStrings s) {
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            width: 72,
            height: 72,
            decoration: BoxDecoration(
              color: _C.mist,
              borderRadius: BorderRadius.circular(20),
            ),
            child: const Icon(Icons.notifications_none_rounded,
                size: 36, color: _C.leaf),
          ),
          const SizedBox(height: 16),
          Text(s.allCaughtUp,
              style: const TextStyle(
                  fontFamily: 'Georgia',
                  fontSize: 18,
                  fontWeight: FontWeight.w600,
                  color: _C.ink)),
          const SizedBox(height: 6),
          Text(s.noNewNotifications,
              style: TextStyle(fontSize: 13, color: _C.slate)),
        ],
      ),
    );
  }
}

class _NotificationTile extends StatelessWidget {
  final NotificationItem item;
  final String timeLabel;
  final VoidCallback onTap;

  const _NotificationTile({
    required this.item,
    required this.timeLabel,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 300),
        color: item.isRead ? Colors.transparent : item.color.withValues(alpha: 0.04),
        padding:
            const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: item.color.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Icon(item.icon, size: 20, color: item.color),
            ),
            const SizedBox(width: 14),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Expanded(
                        child: Text(
                          item.title,
                          style: TextStyle(
                            fontSize: 14,
                            fontWeight: item.isRead
                                ? FontWeight.w500
                                : FontWeight.w700,
                            color: _C.ink,
                          ),
                        ),
                      ),
                      if (!item.isRead)
                        Container(
                          width: 8,
                          height: 8,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            color: item.color,
                          ),
                        ),
                    ],
                  ),
                  const SizedBox(height: 3),
                  Text(
                    item.body,
                    style: TextStyle(
                      fontSize: 12,
                      color: item.isRead ? _C.slate : _C.graphite,
                      height: 1.4,
                    ),
                  ),
                  const SizedBox(height: 5),
                  Text(
                    timeLabel,
                    style:
                        const TextStyle(fontSize: 11, color: _C.slate),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

//
//  AppBar(
//    actions: [
//      const WeatherChip(),
//      const SizedBox(width: 8),
//      const NotificationBell(),
//      const SizedBox(width: 16),
//    ],
//  )
//
//  Add to pubspec.yaml:
//    dependencies:
//      http: ^1.2.0


