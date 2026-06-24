import pathlib, os

files = {}

# ── 1. app_strings.dart ────────────────────────────────────────────────────
files['lib/shared/l10n/app_strings.dart'] = r"""
class AppStrings {
  final String languageCode;
  const AppStrings._(this.languageCode);

  static const en = AppStrings._('en');
  static const sw = AppStrings._('sw');

  static AppStrings of(String code) => code == 'sw' ? sw : en;

  // ── Auth ──────────────────────────────────────────────────────────────────
  String get appName            => _t('Flower Scout',            'Flower Scout');
  String get farmName           => _t('Kongoni River Farm',      'Shamba la Kongoni River');
  String get signIn             => _t('Sign in',                 'Ingia');
  String get welcomeBack        => _t('Welcome back to FlowerScout', 'Karibu tena FlowerScout');
  String get email              => _t('Email',                   'Barua pepe');
  String get password           => _t('Password',                'Nenosiri');
  String get signingIn          => _t('Signing in...',           'Inaingia...');
  String get errorEmptyFields   => _t('Please enter your email and password.', 'Tafadhali ingiza barua pepe na nenosiri.');
  String get errorLoginFailed   => _t('Login failed. Check your credentials.', 'Kuingia kumeshindwa. Angalia taarifa zako.');
  String get errorUnexpected    => _t('An unexpected error occurred.',         'Hitilafu isiyotarajiwa imetokea.');

  // ── Shell / Nav ───────────────────────────────────────────────────────────
  String get navDashboard   => _t('Dashboard',  'Dashibodi');
  String get navScouting    => _t('Scouting',   'Ukaguzi');
  String get navMaps        => _t('Maps',       'Ramani');
  String get navReports     => _t('Reports',    'Ripoti');
  String get navSettings    => _t('Settings',   'Mipangilio');
  String get signOut        => _t('Sign out',   'Toka');
  String get signOutConfirm => _t('Sign out?',  'Toka?');
  String get signOutMsg     => _t('You will need to log in again to access FlowerScout.', 'Utahitaji kuingia tena ili kufikia FlowerScout.');
  String get cancel         => _t('Cancel',     'Ghairi');

  // ── Dashboard ─────────────────────────────────────────────────────────────
  String get goodMorning    => _t('Good morning',   'Habari za asubuhi');
  String get goodAfternoon  => _t('Good afternoon', 'Habari za mchana');
  String get goodEvening    => _t('Good evening',   'Habari za jioni');
  String get farmOverview   => _t('Farm Overview',  'Muhtasari wa Shamba');
  String get quickActions   => _t('Quick Actions',  'Vitendo vya Haraka');
  String get reportSummary  => _t('Report Summary', 'Muhtasari wa Ripoti');
  String get farms          => _t('Farms',          'Mashamba');
  String get newReport      => _t('New Report',     'Ripoti Mpya');
  String get openMaps       => _t('Open Maps',      'Fungua Ramani');
  String get settings       => _t('Settings',       'Mipangilio');
  String get viewFullReports=> _t('View full reports', 'Angalia ripoti zote');
  String get noFarmsYet     => _t('No farms yet',   'Hakuna mashamba bado');
  String get noFarmsDesc    => _t('Farms you have access to will appear here.', 'Mashamba unayoweza kufikia yataonekana hapa.');
  String get couldNotLoad   => _t('Could not load dashboard', 'Dashibodi haijapakia');
  String get ghActivation   => _t('Greenhouse Activation', 'Uanzishaji wa Chafu');
  String get greenhouses    => _t('Greenhouses',    'Vyumba vya Mimea');
  String get plantings      => _t('Plantings',      'Upandaji');
  String get varieties      => _t('Varieties',      'Aina');
  String get active         => _t('Active',         'Hai');
  String get check          => _t('Check',          'Angalia');
  String get inactive       => _t('inactive',       'haifanyi kazi');
  String get totalPlants    => _t('Total plants',   'Jumla ya mimea');
  String get varietiesInUse => _t('Varieties in use','Aina zinazotumiwa');
  String get activeGh       => _t('Active greenhouses', 'Vyumba hai');
  String get inactiveLabel  => _t('Inactive',       'Isiyofanya kazi');
  String get totalArea      => _t('Total area',     'Eneo lote');
  String get excellentCond  => _t('Excellent condition',       'Hali nzuri sana');
  String get goodCond       => _t('Good condition',            'Hali nzuri');
  String get needsAttention => _t('Needs attention',           'Inahitaji umakini');
  String get criticalAction => _t('Critical — action required','Muhimu — hatua inahitajika');

  // ── Scouting ──────────────────────────────────────────────────────────────
  String get scoutingInspection => _t('SCOUTING INSPECTION',     'UKAGUZI WA SHAMBA');
  String get inspectionInProgress=>_t('Inspection In\nProgress', 'Ukaguzi\nUnafanyika');
  String get newInspectionReport=> _t('New Inspection\nReport',  'Ripoti Mpya\nya Ukaguzi');
  String get readyToScout       => _t('Ready to Scout?',         'Uko Tayari Kukagua?');
  String get startScouting      => _t('Start Scouting',          'Anza Ukaguzi');
  String get startScoutingDesc  => _t('Tap Start Scouting to begin your inspection.\nYour location will be captured to geo-tag findings.',
                                      'Gonga Anza Ukaguzi kuanza ukaguzi wako.\nEneo lako litanaswa kutambua matokeo.');
  String get inspectionProgress => _t('Inspection Progress',     'Maendeleo ya Ukaguzi');
  String get farm               => _t('Farm',     'Shamba');
  String get greenhouse         => _t('Greenhouse','Chafu');
  String get variety            => _t('Variety',   'Aina');
  String get findings           => _t('Findings',  'Matokeo');
  String get quickAdd           => _t('QUICK ADD', 'ONGEZA HARAKA');
  String get addFinding         => _t('Add finding','Ongeza tokeo');
  String get submitReport       => _t('Submit Report', 'Wasilisha Ripoti');
  String get submitting         => _t('Submitting...', 'Inawasilisha...');
  String get selectFarm         => _t('Select farm',       'Chagua shamba');
  String get selectFarmFirst    => _t('Select farm first', 'Chagua shamba kwanza');
  String get selectGreenhouse   => _t('Select greenhouse', 'Chagua chafu');
  String get selectGhFirst      => _t('Select GH first',   'Chagua chafu kwanza');
  String get selectVariety      => _t('Select variety',    'Chagua aina');
  String get pleaseSelectAll    => _t('Please select Farm, Greenhouse and Variety', 'Tafadhali chagua Shamba, Chafu na Aina');
  String get pleaseAddFinding   => _t('Please add at least one finding', 'Tafadhali ongeza tokeo moja angalau');
  String get reportSubmitted    => _t('Report submitted successfully!', 'Ripoti imewasilishwa!');
  String get failedToSubmit     => _t('Failed to submit: ', 'Imeshindwa kuwasilisha: ');
  String get couldNotLoadFarm   => _t('Could not load farm data', 'Data ya shamba haijapakia');
  String get locationServicesOff=> _t('Location services off', 'Huduma za eneo zimezimwa');
  String get locationServicesMsg=> _t('Please enable location services to geo-tag your inspections.',
                                      'Tafadhali wezesha huduma za eneo ili kutambua ukaguzi wako.');
  String get locationPermReq    => _t('Location permission required', 'Ruhusa ya eneo inahitajika');
  String get locationPermMsg    => _t('Location access is denied. Findings will not be geo-tagged. You can enable it in app settings.',
                                      'Ufikiaji wa eneo umekataliwa. Matokeo hayatatambuliwa kwa eneo. Unaweza kuiwezesha katika mipangilio.');
  String get continueAnyway     => _t('Continue anyway', 'Endelea hata hivyo');
  String get openAppSettings    => _t('Open settings',   'Fungua mipangilio');
  String get findingLabel       => _t('Finding',         'Tokeo');
  String get category           => _t('CATEGORY',        'KATEGORIA');
  String get severity           => _t('SEVERITY',        'UKALI');
  String get issueObservation   => _t('ISSUE / OBSERVATION', 'TATIZO / UCHUNGUZI');
  String get describeObserved   => _t('Describe what you observed...', 'Elezea ulichoona...');
  String get disease            => _t('Disease',      'Ugonjwa');
  String get pest               => _t('Pest',         'Wadudu');
  String get waterStress        => _t('Water Stress', 'Msongo wa Maji');
  String get nutrition          => _t('Nutrition',    'Lishe');
  String get irrigation         => _t('Irrigation',   'Umwagiliaji');
  String get other              => _t('Other',        'Nyingine');
  String get low                => _t('Low',          'Chini');
  String get medium             => _t('Medium',       'Wastani');
  String get high               => _t('High',         'Juu');
  String get critical           => _t('Critical',     'Muhimu');

  // ── Maps ──────────────────────────────────────────────────────────────────
  String get scoutTrailMap      => _t('Scout Trail Map',  'Ramani ya Njia ya Ukaguzi');
  String get trailManagerOnly   => _t('Trail tracking and playback are available to farm managers and admins.',
                                      'Ufuatiliaji wa njia unapatikana kwa wasimamizi na wasimamizi wakuu.');
  String get liveNow            => _t('Live Now',         'Moja kwa Moja');
  String get history            => _t('History',          'Historia');
  String get noScoutsOut        => _t('No scouts are currently out scouting', 'Hakuna wakaguzi wanaokagua sasa hivi');
  String get couldNotLoadLive   => _t('Could not load live scouts',   'Wakaguzi wa moja kwa moja hawajapakia');
  String get couldNotLoadHistory=> _t('Could not load trail history', 'Historia ya njia haijapakia');
  String get noCompletedTrails  => _t('No completed trails yet',      'Hakuna njia zilizokamilika bado');
  String get deleteTrail        => _t('Delete trail?',    'Futa njia?');
  String get deleteTrailMsg     => _t('This will permanently delete the trail and all its GPS points.',
                                      'Hii itafuta njia na pointi zote za GPS kabisa.');
  String get delete             => _t('Delete',           'Futa');
  String get liveTrail          => _t('Live trail',       'Njia ya moja kwa moja');
  String get trailPlayback      => _t('Trail playback',   'Uchezaji wa njia');
  String get couldNotLoadTrail  => _t('Could not load trail', 'Njia haijapakia');
  String get noGpsPoints        => _t('No GPS points recorded for this trail', 'Hakuna pointi za GPS zilizorekodiwa');
  String get unknownScout       => _t('Unknown scout',    'Mkaguzi asiyejulikana');

  // ── Reports ───────────────────────────────────────────────────────────────
  String get reportsAnalytics   => _t('Reports & Analytics',    'Ripoti na Uchambuzi');
  String get reportsSubtitle    => _t('Inspection trends, findings and performance', 'Mwenendo wa ukaguzi, matokeo na utendaji');
  String get exportPdf          => _t('Export PDF',   'Hamisha PDF');
  String get exportExcel        => _t('Export Excel', 'Hamisha Excel');
  String get aiInsight          => _t('AI Insight',   'Ufahamu wa AI');
  String get dateRange          => _t('Date Range',   'Muda');
  String get allFarms           => _t('All Farms',    'Mashamba Yote');
  String get allLabel           => _t('All',          'Yote');
  String get inspections        => _t('Inspections',  'Ukaguzi');
  String get pests              => _t('Pests',        'Wadudu');
  String get findingsTrend      => _t('Findings Trend','Mwenendo wa Matokeo');
  String get severityBreakdown  => _t('Severity Breakdown',     'Mgawanyo wa Ukali');
  String get topProblemCats     => _t('Top Problem Categories', 'Makundi Makuu ya Matatizo');
  String get topGhByFindings    => _t('Top Greenhouses by Findings', 'Vyumba vya Juu kwa Matokeo');
  String get recentInspections  => _t('Recent Inspections',     'Ukaguzi wa Hivi Karibuni');
  String get noMatchFilter      => _t('No inspections match this filter.', 'Hakuna ukaguzi unaolingana na kichujio hiki.');
  String get bar                => _t('Bar',  'Mstari');
  String get line               => _t('Line', 'Mstari');
  String get download           => _t('Download', 'Pakua');

  // ── Settings ──────────────────────────────────────────────────────────────
  String get settingsTitle      => _t('Settings',     'Mipangilio');
  String get tabFarms           => _t('Farm config',  'Usanidi wa Shamba');
  String get tabProfile         => _t('Profile',      'Wasifu');
  String get tabTeam            => _t('Team',         'Timu');
  String get tabNotifications   => _t('Notifications','Arifa');
  String get tabPreferences     => _t('Preferences',  'Mapendeleo');
  String get farmGhConfig       => _t('Farm & greenhouse config', 'Usanidi wa Shamba na Chafu');
  String get farmGhConfigDesc   => _t('Manage your farms and growing locations.', 'Simamia mashamba na maeneo ya ukuaji.');
  String get loadingFarms       => _t('Loading farms...','Inapakia mashamba...');
  String get noFarmsAssigned    => _t('No farms assigned to your account.', 'Hakuna mashamba yaliyokabidhiwa akaunti yako.');
  String get inspectionDefaults => _t('INSPECTION DEFAULTS', 'MIPANGILIO YA UKAGUZI');
  String get inspectionInterval => _t('Inspection interval', 'Muda wa ukaguzi');
  String get inspectionIntervalDesc=> _t('Days between required greenhouse checks', 'Siku kati ya ukaguzi wa chafu unaohitajika');
  String get refreshData        => _t('Refresh data',  'Onyesha upya data');
  String get refreshDataDesc    => _t('Pull latest farm data from server', 'Pata data mpya ya shamba kutoka seva');
  String get refresh            => _t('Refresh',       'Onyesha upya');
  String get yourProfile        => _t('Your profile',  'Wasifu wako');
  String get yourProfileDesc    => _t('Update your personal details.', 'Sasisha maelezo yako ya kibinafsi.');
  String get loadingProfile     => _t('Loading profile...', 'Inapakia wasifu...');
  String get personalInfo       => _t('PERSONAL INFO', 'TAARIFA ZA KIBINAFSI');
  String get fullName           => _t('FULL NAME',     'JINA KAMILI');
  String get emailLabel         => _t('EMAIL',         'BARUA PEPE');
  String get phone              => _t('PHONE',         'SIMU');
  String get saveProfile        => _t('Save profile',  'Hifadhi wasifu');
  String get teamManagement     => _t('Team management',    'Usimamizi wa Timu');
  String get teamManagementDesc => _t('View and manage team access.', 'Angalia na simamia ufikiaji wa timu.');
  String get loadingTeam        => _t('Loading team...','Inapakia timu...');
  String get noTeamMembers      => _t('No team members found.', 'Hakuna wanachama wa timu walioopatikana.');
  String get inviteNewMember    => _t('INVITE A NEW MEMBER', 'ALIKA MWANACHAMA MPYA');
  String get roleLabel          => _t('ROLE',          'WADHIFU');
  String get sendInvite         => _t('Send invite',   'Tuma mwaliko');
  String get notificationsAlerts=> _t('Notifications & alerts',  'Arifa na Tahadhari');
  String get notificationsDesc  => _t('Control when and how FlowerScout notifies you.', 'Dhibiti wakati na jinsi FlowerScout inavyokutaarifu.');
  String get inspectionAlerts   => _t('INSPECTION ALERTS',    'TAHADHARI ZA UKAGUZI');
  String get overdueReminder    => _t('Overdue inspection reminder', 'Ukumbusho wa ukaguzi uliochelewa');
  String get overdueDesc        => _t('Notify when a greenhouse passes its inspection date', 'Taarifu wakati chafu kinapopita tarehe yake ya ukaguzi');
  String get criticalAlert      => _t('Critical pest / disease alert', 'Tahadhari ya wadudu/ugonjwa muhimu');
  String get criticalAlertDesc  => _t('Immediate push when health score drops below threshold', 'Msukumo wa haraka wakati alama ya afya inashuka chini ya kiwango');
  String get weeklySummary      => _t('Weekly summary report', 'Ripoti ya muhtasari wa kila wiki');
  String get weeklyDesc         => _t('Every Monday 7 AM — farm health digest', 'Kila Jumatatu saa 1 asubuhi — muhtasari wa afya ya shamba');
  String get deliveryChannels   => _t('DELIVERY CHANNELS',   'NJIA ZA UTOAJI');
  String get pushNotifications  => _t('Push notifications',  'Arifa za msukumo');
  String get pushDesc           => _t('Mobile and desktop',  'Simu na kompyuta');
  String get notSet             => _t('Not set',             'Haijawekwa');
  String get addPhoneForSms     => _t('Add phone number in Profile', 'Ongeza nambari ya simu kwenye Wasifu');
  String get saveNotifSettings  => _t('Save notification settings', 'Hifadhi mipangilio ya arifa');
  String get appPreferences     => _t('App preferences',    'Mapendeleo ya Programu');
  String get appPreferencesDesc => _t('Personalise how FlowerScout looks and behaves.', 'Personalisha jinsi FlowerScout inavyoonekana na kutenda.');
  String get appearance         => _t('APPEARANCE',         'MUONEKANO');
  String get theme              => _t('THEME',              'MANDHARI');
  String get dateFormat         => _t('DATE FORMAT',        'MUUNDO WA TAREHE');
  String get mapDefaults        => _t('MAP DEFAULTS',       'MIPANGILIO YA RAMANI');
  String get defaultView        => _t('DEFAULT VIEW',       'MTAZAMO WA CHAGUO-MSINGI');
  String get showHeatmap        => _t('Show heatmap on load','Onyesha ramani ya joto wakati wa kupakia');
  String get heatmapDesc        => _t('Auto-display scouting heatmap when opening Maps', 'Onyesha ramani ya ukaguzi moja kwa moja unapofungua Ramani');
  String get about              => _t('ABOUT',              'KUHUSU');
  String get signOutLabel       => _t('Sign out',           'Toka');
  String get signOutSettingsDesc=> _t('Log out of FlowerScout', 'Toka kwenye FlowerScout');
  String get savePreferences    => _t('Save preferences',   'Hifadhi mapendeleo');
  String get saved              => _t('saved',              'imehifadhiwa');
  String get language           => _t('LANGUAGE',           'LUGHA');
  String get english            => _t('English',            'Kiingereza');
  String get swahili            => _t('Swahili',            'Kiswahili');
  String get systemDefault      => _t('System default',     'Chaguo-msingi la mfumo');
  String get lightTheme         => _t('Light',              'Mwanga');
  String get darkTheme          => _t('Dark',               'Giza');
  String get satellite          => _t('Satellite',          'Setilaiti');
  String get terrain            => _t('Terrain',            'Ardhi');
  String get street             => _t('Street',             'Mtaa');
  String get latest             => _t('Latest',             'Mpya');
  String get scout              => _t('Scout',              'Mkaguzi');
  String get manager            => _t('Manager',            'Msimamizi');
  String get viewer             => _t('Viewer',             'Mtazamaji');
  String get systemAdmin        => _t('System Admin',       'Msimamizi Mkuu');

  String _t(String en, String sw) => languageCode == 'sw' ? sw : en;
}
""".lstrip()

# ── 2. locale_provider.dart ───────────────────────────────────────────────
files['lib/shared/providers/locale_provider.dart'] = r"""
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../l10n/app_strings.dart';

const _kLangKey = 'app_language';

class LocaleNotifier extends Notifier<String> {
  @override
  String build() {
    // Load persisted value; default to English
    final prefs = ref.watch(sharedPrefsProvider).value;
    return prefs?.getString(_kLangKey) ?? 'en';
  }

  Future<void> setLanguage(String code) async {
    state = code;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_kLangKey, code);
  }
}

final localeProvider = NotifierProvider<LocaleNotifier, String>(
  LocaleNotifier.new,
);

/// Convenience: get the AppStrings object for the current language
final stringsProvider = Provider<AppStrings>((ref) {
  final code = ref.watch(localeProvider);
  return AppStrings.of(code);
});
""".lstrip()

for path, content in files.items():
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Written:', path)

print('All done.')