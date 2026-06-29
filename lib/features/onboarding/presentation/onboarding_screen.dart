import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../../shared/widgets/app_shell.dart';

const _kOnboardingKey = 'onboarding_seen_v1';

Future<bool> hasSeenOnboarding() async {
  final prefs = await SharedPreferences.getInstance();
  return prefs.getBool(_kOnboardingKey) ?? false;
}

Future<void> markOnboardingSeen() async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.setBool(_kOnboardingKey, true);
}

class OnboardingScreen extends StatefulWidget {
  const OnboardingScreen({super.key});
  @override
  State<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen> {
  int _page = 0;

  void _go(int page) => setState(() => _page = page);

  Future<void> _finish() async {
    await markOnboardingSeen();
    if (!mounted) return;
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(builder: (_) => const AppShell()));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAF8),
      body: SafeArea(
        child: AnimatedSwitcher(
          duration: const Duration(milliseconds: 280),
          transitionBuilder: (child, anim) => FadeTransition(
            opacity: anim,
            child: SlideTransition(
              position: Tween<Offset>(begin: const Offset(0, 0.04), end: Offset.zero)
                  .animate(anim),
              child: child,
            ),
          ),
          child: KeyedSubtree(
            key: ValueKey(_page),
            child: _pages[_page],
          ),
        ),
      ),
    );
  }

  late final List<Widget> _pages = [
    _WelcomePage(onNext: () => _go(1)),
    _StepPage(
      stepNum: 1,
      totalSteps: 3,
      icon: Icons.play_arrow_rounded,
      badge: 'STARTING A SESSION',
      title: 'Tap, select, scout',
      subtitle: 'From the Scouting tab, tap Start scouting to begin your inspection.',
      progress: 0.33,
      items: const [
        _Item(Icons.business_rounded, 'Select farm, greenhouse and variety',
            'These three dropdowns lock in context for every finding you log.'),
        _Item(Icons.timer_rounded, 'Timer tracks your session',
            'Starts automatically, stops when you submit the report.'),
        _Item(Icons.my_location_rounded, 'GPS records your trail',
            'Managers watch it live on the Maps screen as you move.'),
      ],
      currentPage: 1,
      onBack: () => _go(0),
      onNext: () => _go(2),
      onSkip: _finish,
    ),
    _StepPage(
      stepNum: 2,
      totalSteps: 3,
      icon: Icons.assignment_rounded,
      badge: 'LOGGING FINDINGS',
      title: 'Capture every observation',
      subtitle: 'One finding card per issue: category, severity, description and photo.',
      progress: 0.66,
      items: const [
        _Item(Icons.flash_on_rounded, 'Quick Add buttons',
            'Tap Disease, Pest, Water Stress - a new finding card opens instantly.'),
        _Item(Icons.mic_rounded, 'Voice input for gloved hands',
            'Tap the mic icon in the observation field and speak. No typing needed.'),
        _Item(Icons.camera_alt_rounded, 'Attach photo evidence',
            'Camera or gallery. Up to 5 photos per finding.'),
      ],
      currentPage: 2,
      onBack: () => _go(1),
      onNext: () => _go(3),
      onSkip: _finish,
    ),
    _StepPage(
      stepNum: 3,
      totalSteps: 3,
      icon: Icons.send_rounded,
      badge: 'SUBMITTING',
      title: 'One tap to submit',
      subtitle: 'Your report including findings, photos and GPS trail goes to your manager instantly.',
      progress: 1.0,
      items: const [
        _Item(Icons.cloud_upload_rounded, 'Offline? It still saves',
            'Reports queue locally and upload automatically when signal returns.'),
        _Item(Icons.sync_rounded, 'Pending count badge',
            'Shows how many reports are waiting to sync so nothing gets lost.'),
      ],
      tip: 'This walkthrough won\'t show again. Replay it anytime from Settings.',
      currentPage: 3,
      onBack: () => _go(2),
      onNext: _finish,
      onSkip: null,
      nextLabel: "Let's go",
    ),
  ];
}

// -- Welcome page --------------------------------------------------------------
class _WelcomePage extends StatelessWidget {
  final VoidCallback onNext;
  const _WelcomePage({required this.onNext});

  @override
  Widget build(BuildContext context) {
    return Column(children: [
      _Hero(
        icon: Icons.eco_rounded,
        badge: 'WELCOME TO FLOWERSCOUT',
        title: 'Your field scouting\ncompanion',
        subtitle: 'Smarter scouting, faster reporting, zero paperwork.',
      ),
      Expanded(
        child: SingleChildScrollView(
          padding: const EdgeInsets.fromLTRB(20, 20, 20, 4),
          child: Column(children: const [
            _Item(Icons.map_rounded, 'GPS trail recording',
                'Your path through every greenhouse row is tracked automatically.'),
            SizedBox(height: 14),
            _Item(Icons.assignment_rounded, 'Fast finding logging',
                'Disease, pest, water stress - log it with voice or one tap.'),
            SizedBox(height: 14),
            _Item(Icons.wifi_off_rounded, 'Works offline',
                'Reports save locally and sync the moment you get signal.'),
          ]),
        ),
      ),
      Padding(
        padding: const EdgeInsets.fromLTRB(20, 8, 20, 24),
        child: Column(children: [
          _BtnPrimary(label: 'Get started', icon: Icons.arrow_forward_rounded, onTap: onNext),
          const SizedBox(height: 10),
          _DotsRow(current: 0, total: 4),
        ]),
      ),
    ]);
  }
}

// -- Step page -----------------------------------------------------------------
class _StepPage extends StatelessWidget {
  final int stepNum;
  final int totalSteps;
  final IconData icon;
  final String badge;
  final String title;
  final String subtitle;
  final double progress;
  final List<_Item> items;
  final String? tip;
  final int currentPage;
  final VoidCallback onBack;
  final VoidCallback onNext;
  final VoidCallback? onSkip;
  final String nextLabel;

  const _StepPage({
    required this.stepNum,
    required this.totalSteps,
    required this.icon,
    required this.badge,
    required this.title,
    required this.subtitle,
    required this.progress,
    required this.items,
    required this.currentPage,
    required this.onBack,
    required this.onNext,
    this.onSkip,
    this.tip,
    this.nextLabel = 'Next',
  });

  @override
  Widget build(BuildContext context) {
    return Column(children: [
      Stack(children: [
        _Hero(icon: icon, badge: badge, title: title, subtitle: subtitle),
        Positioned(top: 14, right: 18,
          child: Text('$stepNum / $totalSteps',
            style: const TextStyle(fontSize: 11, color: Colors.white54))),
      ]),
      _ProgressBar(value: progress),
      Expanded(
        child: SingleChildScrollView(
          padding: const EdgeInsets.fromLTRB(20, 16, 20, 4),
          child: Column(
            children: [
              ...items.map((item) => Padding(
                padding: const EdgeInsets.only(bottom: 14),
                child: item)),
              if (tip != null) ...[
                const SizedBox(height: 4),
                _TipBox(tip!),
              ],
            ],
          ),
        ),
      ),
      Padding(
        padding: const EdgeInsets.fromLTRB(20, 8, 20, 24),
        child: Column(children: [
          Row(children: [
            Expanded(child: _BtnBack(onTap: onBack)),
            const SizedBox(width: 10),
            Expanded(flex: 2, child: _BtnPrimary(
              label: nextLabel,
              icon: Icons.arrow_forward_rounded,
              onTap: onNext,
              color: stepNum == totalSteps ? const Color(0xFF2D6A4F) : const Color(0xFF1B4332),
            )),
          ]),
          const SizedBox(height: 8),
          _DotsRow(current: currentPage, total: 4),
          if (onSkip != null) ...[
            const SizedBox(height: 6),
            GestureDetector(
              onTap: onSkip,
              child: const Text('Skip walkthrough',
                style: TextStyle(fontSize: 11, color: Color(0xFF9EAD9E)))),
          ],
        ]),
      ),
    ]);
  }
}

// -- Shared components ---------------------------------------------------------
class _Hero extends StatelessWidget {
  final IconData icon;
  final String badge;
  final String title;
  final String subtitle;
  const _Hero({required this.icon, required this.badge, required this.title, required this.subtitle});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      color: const Color(0xFF1B4332),
      padding: const EdgeInsets.fromLTRB(24, 28, 24, 24),
      child: Column(children: [
        Container(
          width: 68, height: 68,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: Colors.white.withValues(alpha: 0.12),
            border: Border.all(color: Colors.white.withValues(alpha: 0.2), width: 1.5),
          ),
          child: Icon(icon, color: Colors.white, size: 30),
        ),
        const SizedBox(height: 12),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
          decoration: BoxDecoration(
            color: Colors.white.withValues(alpha: 0.15),
            borderRadius: BorderRadius.circular(20)),
          child: Text(badge, style: const TextStyle(
            fontSize: 10, fontWeight: FontWeight.w600,
            letterSpacing: 1.2, color: Colors.white70)),
        ),
        const SizedBox(height: 10),
        Text(title, textAlign: TextAlign.center,
          style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w600,
              color: Colors.white, height: 1.25)),
        const SizedBox(height: 6),
        Text(subtitle, textAlign: TextAlign.center,
          style: const TextStyle(fontSize: 12, color: Colors.white60, height: 1.6)),
      ]),
    );
  }
}

class _Item extends StatelessWidget {
  final IconData icon;
  final String title;
  final String desc;
  const _Item(this.icon, this.title, this.desc, {super.key});

  @override
  Widget build(BuildContext context) {
    return Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Container(
        width: 34, height: 34,
        decoration: BoxDecoration(
          color: const Color(0xFFEAF3DE),
          borderRadius: BorderRadius.circular(10)),
        child: Icon(icon, color: const Color(0xFF1B4332), size: 16),
      ),
      const SizedBox(width: 12),
      Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(title, style: const TextStyle(
          fontSize: 13, fontWeight: FontWeight.w600, color: Color(0xFF0D1B0F))),
        const SizedBox(height: 2),
        Text(desc, style: const TextStyle(
          fontSize: 11, color: Color(0xFF6B7F6E), height: 1.5)),
      ])),
    ]);
  }
}

class _TipBox extends StatelessWidget {
  final String text;
  const _TipBox(this.text);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: const Color(0xFFF0FBF4),
        border: Border.all(color: const Color(0xFFB7DFC5)),
        borderRadius: BorderRadius.circular(10)),
      child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Icon(Icons.lightbulb_outline_rounded, size: 15, color: Color(0xFF2D6A4F)),
        const SizedBox(width: 8),
        Expanded(child: Text(text,
          style: const TextStyle(fontSize: 11, color: Color(0xFF2D6A4F), height: 1.5))),
      ]),
    );
  }
}

class _ProgressBar extends StatelessWidget {
  final double value;
  const _ProgressBar({required this.value});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 20),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(2),
        child: LinearProgressIndicator(
          value: value,
          minHeight: 3,
          backgroundColor: const Color(0xFFEAF3DE),
          valueColor: const AlwaysStoppedAnimation(Color(0xFF1B4332)),
        ),
      ),
    );
  }
}

class _DotsRow extends StatelessWidget {
  final int current;
  final int total;
  const _DotsRow({required this.current, required this.total});

  @override
  Widget build(BuildContext context) {
    return Row(mainAxisAlignment: MainAxisAlignment.center, children: List.generate(total, (i) {
      final active = i == current;
      return AnimatedContainer(
        duration: const Duration(milliseconds: 250),
        margin: const EdgeInsets.symmetric(horizontal: 3),
        width: active ? 20 : 6,
        height: 6,
        decoration: BoxDecoration(
          color: active ? const Color(0xFF1B4332) : const Color(0xFFDDE5DD),
          borderRadius: BorderRadius.circular(3)),
      );
    }));
  }
}

class _BtnPrimary extends StatelessWidget {
  final String label;
  final IconData icon;
  final VoidCallback onTap;
  final Color color;
  const _BtnPrimary({required this.label, required this.icon,
      required this.onTap, this.color = const Color(0xFF1B4332)});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: double.infinity, height: 48,
      child: ElevatedButton.icon(
        icon: Text(label, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
        label: Icon(icon, size: 16),
        onPressed: onTap,
        style: ElevatedButton.styleFrom(
          backgroundColor: color, foregroundColor: Colors.white,
          elevation: 0, shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
      ),
    );
  }
}

class _BtnBack extends StatelessWidget {
  final VoidCallback onTap;
  const _BtnBack({required this.onTap});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 48,
      child: OutlinedButton.icon(
        icon: const Icon(Icons.arrow_back_rounded, size: 16),
        label: const Text('Back', style: TextStyle(fontSize: 13)),
        onPressed: onTap,
        style: OutlinedButton.styleFrom(
          foregroundColor: const Color(0xFF6B7F6E),
          side: const BorderSide(color: Color(0xFFDDE5DD)),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
      ),
    );
  }
}

