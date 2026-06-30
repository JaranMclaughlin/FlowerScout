import pathlib, shutil

# ── Step 1: Add onboarding strings to app_strings.dart ───────────────────────
ap = pathlib.Path('lib/shared/l10n/app_strings.dart')
s = ap.read_text(encoding='utf-8')

onboard_strings = """
  // ── Onboarding ────────────────────────────────────────────────────────────
  String get obWelcomeBadge    => _t('WELCOME TO FLOWERSCOUT',        'KARIBU FLOWERSCOUT');
  String get obWelcomeTitle    => _t('Your field scouting\\ncompanion','Msaidizi wako\\nwa ukaguzi wa shamba');
  String get obWelcomeSub      => _t('Smarter scouting, faster reporting, zero paperwork.', 'Ukaguzi bora, ripoti haraka, bila karatasi.');
  String get obGetStarted      => _t('Get started',                   'Anza');
  String get obNext            => _t('Next',                          'Ifuatayo');
  String get obBack            => _t('Back',                          'Rudi');
  String get obSkip            => _t('Skip walkthrough',              'Ruka mwongozo');
  String get obLetsGo          => _t("Let's go",                      'Twende');
  String get obTipReplay       => _t('This walkthrough won\\'t show again. Replay it anytime from Settings.', 'Mwongozo huu hautaonekana tena. Urudishe wakati wowote kutoka Mipangilio.');

  String get obStep1Badge      => _t('STARTING A SESSION',            'KUANZA KIPINDI');
  String get obStep1Title      => _t('Tap, select, scout',            'Gonga, chagua, kagua');
  String get obStep1Sub        => _t('From the Scouting tab, tap Start scouting to begin your inspection.', 'Kutoka kichupo cha Ukaguzi, gonga Anza Ukaguzi kuanza ukaguzi wako.');
  String get obStep1I1Title    => _t('Select farm, greenhouse and variety', 'Chagua shamba, chafu na aina');
  String get obStep1I1Desc     => _t('These three dropdowns lock in context for every finding you log.', 'Madropdown haya matatu yanafunga muktadha kwa kila ugunduzi unaoingia.');
  String get obStep1I2Title    => _t('Timer tracks your session',     'Saa inafuatilia kipindi chako');
  String get obStep1I2Desc     => _t('Starts automatically, stops when you submit the report.', 'Inaanza kiotomatiki, inasimama unapotuma ripoti.');
  String get obStep1I3Title    => _t('GPS records your trail',        'GPS inarekodia njia yako');
  String get obStep1I3Desc     => _t('Managers watch it live on the Maps screen as you move.', 'Wasimamizi wanaiona moja kwa moja kwenye skrini ya Ramani unapotembea.');

  String get obStep2Badge      => _t('LOGGING FINDINGS',              'KUREKODI MATOKEO');
  String get obStep2Title      => _t('Capture every observation',     'Nasa kila uchunguzi');
  String get obStep2Sub        => _t('One finding card per issue: category, severity, description and photo.', 'Kadi moja ya ugunduzi kwa tatizo: kategoria, ukali, maelezo na picha.');
  String get obStep2I1Title    => _t('Quick Add buttons',             'Vitufe vya Kuongeza Haraka');
  String get obStep2I1Desc     => _t('Tap Disease, Pest, Water Stress - a new finding card opens instantly.', 'Gonga Ugonjwa, Wadudu, Msongo wa Maji - kadi mpya ya ugunduzi inafunguka mara moja.');
  String get obStep2I2Title    => _t('Voice input for gloved hands',  'Ingizo la sauti kwa mikono yenye glavu');
  String get obStep2I2Desc     => _t('Tap the mic icon in the observation field and speak. No typing needed.', 'Gonga aikoni ya maikrofoni katika sehemu ya uchunguzi na uzungumze. Huhitaji kuandika.');
  String get obStep2I3Title    => _t('Attach photo evidence',         'Ambatisha ushahidi wa picha');
  String get obStep2I3Desc     => _t('Camera or gallery. Up to 5 photos per finding.', 'Kamera au matunzio. Hadi picha 5 kwa kila ugunduzi.');

  String get obStep3Badge      => _t('SUBMITTING',                    'KUTUMA');
  String get obStep3Title      => _t('One tap to submit',             'Gonga mara moja kutuma');
  String get obStep3Sub        => _t('Your report including findings, photos and GPS trail goes to your manager instantly.', 'Ripoti yako ikijumuisha matokeo, picha na njia ya GPS inaenda kwa msimamizi wako mara moja.');
  String get obStep3I1Title    => _t('Offline? It still saves',       'Nje ya mtandao? Bado inahifadhi');
  String get obStep3I1Desc     => _t('Reports queue locally and upload automatically when signal returns.', 'Ripoti zinasubiri ndani na kupakia kiotomatiki ishara inaporejesha.');
  String get obStep3I2Title    => _t('Pending count badge',           'Beji ya idadi inayosubiri');
  String get obStep3I2Desc     => _t('Shows how many reports are waiting to sync so nothing gets lost.', 'Inaonyesha ripoti ngapi zinasubiri kusawazishwa ili hakuna kinachopotea.');

  String get obGpsTrail        => _t('GPS trail recording',           'Kurekodi njia ya GPS');
  String get obGpsTrailDesc    => _t('Your path through every greenhouse row is tracked automatically.', 'Njia yako kupitia kila safu ya chafu inafuatiliwa kiotomatiki.');
  String get obFastLog         => _t('Fast finding logging',          'Kuingia matokeo haraka');
  String get obFastLogDesc     => _t('Disease, pest, water stress - log it with voice or one tap.', 'Ugonjwa, wadudu, msongo wa maji - ingiza kwa sauti au gonga moja.');
  String get obOffline         => _t('Works offline',                 'Inafanya kazi bila mtandao');
  String get obOfflineDesc     => _t('Reports save locally and sync the moment you get signal.', 'Ripoti zinahifadhiwa ndani na kusawazishwa ishara inapopatikana.');"""

# Insert before the closing _t helper
old_anchor = "\n  String _t(String en, String sw) =>"
if old_anchor in s:
    s = s.replace(old_anchor, onboard_strings + "\n\n  String _t(String en, String sw) =>", 1)
    ap.write_text(s, encoding='utf-8')
    print("Step 1: onboarding strings added to AppStrings")
else:
    print("ERROR: _t anchor not found"); raise SystemExit(1)

# ── Step 2: Rewrite onboarding_screen.dart ───────────────────────────────────
op = pathlib.Path('lib/features/onboarding/presentation/onboarding_screen.dart')
shutil.copy(op, op.with_suffix('.dart.bak'))

new_screen = r"""import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../../shared/widgets/app_shell.dart';
import '../../../shared/l10n/app_strings.dart';
import '../../../shared/providers/locale_provider.dart';

const _kOnboardingKey = 'onboarding_seen_v1';

Future<bool> hasSeenOnboarding() async {
  final prefs = await SharedPreferences.getInstance();
  return prefs.getBool(_kOnboardingKey) ?? false;
}

Future<void> markOnboardingSeen() async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.setBool(_kOnboardingKey, true);
}

class OnboardingScreen extends ConsumerStatefulWidget {
  const OnboardingScreen({super.key});
  @override
  ConsumerState<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends ConsumerState<OnboardingScreen> {
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
    final s = AppStrings.of(ref.watch(localeProvider));
    final pages = [
      _WelcomePage(s: s, onNext: () => _go(1)),
      _StepPage(
        s: s,
        stepNum: 1, totalSteps: 3,
        icon: Icons.play_arrow_rounded,
        badge: s.obStep1Badge, title: s.obStep1Title, subtitle: s.obStep1Sub,
        progress: 0.33,
        items: [
          _Item(Icons.business_rounded,   s.obStep1I1Title, s.obStep1I1Desc),
          _Item(Icons.timer_rounded,      s.obStep1I2Title, s.obStep1I2Desc),
          _Item(Icons.my_location_rounded,s.obStep1I3Title, s.obStep1I3Desc),
        ],
        currentPage: 1, onBack: () => _go(0), onNext: () => _go(2), onSkip: _finish,
      ),
      _StepPage(
        s: s,
        stepNum: 2, totalSteps: 3,
        icon: Icons.assignment_rounded,
        badge: s.obStep2Badge, title: s.obStep2Title, subtitle: s.obStep2Sub,
        progress: 0.66,
        items: [
          _Item(Icons.flash_on_rounded,   s.obStep2I1Title, s.obStep2I1Desc),
          _Item(Icons.mic_rounded,        s.obStep2I2Title, s.obStep2I2Desc),
          _Item(Icons.camera_alt_rounded, s.obStep2I3Title, s.obStep2I3Desc),
        ],
        currentPage: 2, onBack: () => _go(1), onNext: () => _go(3), onSkip: _finish,
      ),
      _StepPage(
        s: s,
        stepNum: 3, totalSteps: 3,
        icon: Icons.send_rounded,
        badge: s.obStep3Badge, title: s.obStep3Title, subtitle: s.obStep3Sub,
        progress: 1.0,
        items: [
          _Item(Icons.cloud_upload_rounded, s.obStep3I1Title, s.obStep3I1Desc),
          _Item(Icons.sync_rounded,         s.obStep3I2Title, s.obStep3I2Desc),
        ],
        tip: s.obTipReplay,
        currentPage: 3, onBack: () => _go(2), onNext: _finish, onSkip: null,
        nextLabel: s.obLetsGo,
      ),
    ];

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
            child: pages[_page],
          ),
        ),
      ),
    );
  }
}

// -- Welcome page --------------------------------------------------------------
class _WelcomePage extends StatelessWidget {
  final AppStrings s;
  final VoidCallback onNext;
  const _WelcomePage({required this.s, required this.onNext});

  @override
  Widget build(BuildContext context) {
    return Column(children: [
      _Hero(
        icon: Icons.eco_rounded,
        badge: s.obWelcomeBadge,
        title: s.obWelcomeTitle,
        subtitle: s.obWelcomeSub,
      ),
      Expanded(
        child: SingleChildScrollView(
          padding: const EdgeInsets.fromLTRB(20, 20, 20, 4),
          child: Column(children: [
            _Item(Icons.map_rounded,        s.obGpsTrail,  s.obGpsTrailDesc),
            const SizedBox(height: 14),
            _Item(Icons.assignment_rounded, s.obFastLog,   s.obFastLogDesc),
            const SizedBox(height: 14),
            _Item(Icons.wifi_off_rounded,   s.obOffline,   s.obOfflineDesc),
          ]),
        ),
      ),
      Padding(
        padding: const EdgeInsets.fromLTRB(20, 8, 20, 24),
        child: Column(children: [
          _BtnPrimary(label: s.obGetStarted, icon: Icons.arrow_forward_rounded, onTap: onNext),
          const SizedBox(height: 10),
          const _DotsRow(current: 0, total: 4),
        ]),
      ),
    ]);
  }
}

// -- Step page -----------------------------------------------------------------
class _StepPage extends StatelessWidget {
  final AppStrings s;
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
  final String? nextLabel;

  const _StepPage({
    required this.s,
    required this.stepNum, required this.totalSteps,
    required this.icon, required this.badge,
    required this.title, required this.subtitle,
    required this.progress, required this.items,
    required this.currentPage, required this.onBack, required this.onNext,
    this.onSkip, this.tip, this.nextLabel,
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
          child: Column(children: [
            ...items.map((item) => Padding(
              padding: const EdgeInsets.only(bottom: 14),
              child: item)),
            if (tip != null) ...[
              const SizedBox(height: 4),
              _TipBox(tip!),
            ],
          ]),
        ),
      ),
      Padding(
        padding: const EdgeInsets.fromLTRB(20, 8, 20, 24),
        child: Column(children: [
          Row(children: [
            Expanded(child: _BtnBack(label: s.obBack, onTap: onBack)),
            const SizedBox(width: 10),
            Expanded(flex: 2, child: _BtnPrimary(
              label: nextLabel ?? s.obNext,
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
              child: Text(s.obSkip,
                style: const TextStyle(fontSize: 11, color: Color(0xFF9EAD9E)))),
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
  const _Item(this.icon, this.title, this.desc);

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
  final String label;
  final VoidCallback onTap;
  const _BtnBack({required this.label, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 48,
      child: OutlinedButton.icon(
        icon: const Icon(Icons.arrow_back_rounded, size: 16),
        label: Text(label, style: const TextStyle(fontSize: 13)),
        onPressed: onTap,
        style: OutlinedButton.styleFrom(
          foregroundColor: const Color(0xFF6B7F6E),
          side: const BorderSide(color: Color(0xFFDDE5DD)),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
      ),
    );
  }
}
"""

op.write_text(new_screen, encoding='utf-8')
print("Step 2: onboarding_screen.dart fully rewritten with i18n")