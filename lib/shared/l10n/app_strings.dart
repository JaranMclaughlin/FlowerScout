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


  // ── Months ────────────────────────────────────────────────────────────────
  List<String> get monthsShort => languageCode=='sw'
    ? ['Jan','Feb','Mac','Apr','Mei','Jun','Jul','Ago','Sep','Okt','Nov','Des']
    : ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

  // ── Chart labels ──────────────────────────────────────────────────────────
  List<String> get chartLabelsToday   => languageCode=='sw'
    ? ['6as','8as','10as','12ch','2mch','4jio','6jio']
    : ['6am','8am','10am','12pm','2pm','4pm','6pm'];
  List<String> get chartLabels30Days  => ['W1','W2','W3','W4','W5'];
  List<String> get chartLabels3Months => languageCode=='sw'
    ? ['M1','M2','M3'] : ['M1','M2','M3'];
  List<String> get chartLabelsWeek    => languageCode=='sw'
    ? ['Jumatatu','Jumanne','Jumatano','Alhamisi','Ijumaa','Jumamosi','Jumapili']
    : ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];

  List<String> get chartLabelsWeekShort => languageCode=='sw'
    ? ['Jum','Jum','Jua','Alh','Iju','Jums','Jmap']
    : ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];

  // Full day names
  List<String> get weekdaysFull => languageCode=='sw'
    ? ['Jumatatu','Jumanne','Jumatano','Alhamisi','Ijumaa','Jumamosi','Jumapili']
    : ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];

  // Full month names
  List<String> get monthsFull => languageCode=='sw'
    ? ['Januari','Februari','Machi','Aprili','Mei','Juni','Julai','Agosti','Septemba','Oktoba','Novemba','Desemba']
    : ['January','February','March','April','May','June','July','August','September','October','November','December'];

  // ── Table headers ─────────────────────────────────────────────────────────
  String get colDate      => _t('Date',     'Tarehe');
  String get colGh        => _t('GH',       'Chafu');
  String get colVariety   => _t('Variety',  'Aina');
  String get colCategory  => _t('Category', 'Kategoria');
  String get colSeverity  => _t('Severity', 'Ukali');

  // ── UI actions ────────────────────────────────────────────────────────────
  String get showAll      => _t('Show all', 'Onyesha yote');
  String get showLess     => _t('Show less','Onyesha kidogo');
  String get loadMore     => _t('Load more','Pakia zaidi');
  String get noData       => _t('No data',  'Hakuna data');

  // ── Analytics screen ──────────────────────────────────────────────────────
  String get analytics         => _t('Analytics',                    'Uchambuzi');
  String get analyticsSubtitle => _t('Farm-wide performance and trends','Utendaji na mwenendo wa shamba');
  String get period            => _t('Period',                       'Kipindi');
  String get farmFilter        => _t('Farm',                         'Shamba');
  String get findingsTrendSub  => _t('By category over period',      'Kwa kategoria kwa kipindi');
  String get diseaseLegend     => _t('Disease',  'Ugonjwa');
  String get pestsLegend       => _t('Pests',    'Wadudu');
  String get waterLegend       => _t('Water',    'Maji');
  String get criticalLabel     => _t('Critical', 'Muhimu');
  String get highLabel         => _t('High',     'Juu');
  String get mediumLabel       => _t('Medium',   'Wastani');
  String get lowLabel          => _t('Low',      'Chini');
  String get barLabel          => _t('Bar',      'Mhimili');
  String get lineLabel         => _t('Line',     'Mstari');
  String get topGreenhouses    => _t('Top Greenhouses',      'Vyumba vya Juu');
  String get findingsByCategory=> _t('Findings by Category', 'Matokeo kwa Kategoria');

  // ── Settings hardcoded ────────────────────────────────────────────────────
  String get farmGhConfigTitle => _t('Farm & greenhouse config',  'Usanidi wa Shamba na Chafu');
  String get controlNotif      => _t('Control when and how FlowerScout notifies you.', 'Dhibiti wakati na jinsi FlowerScout inavyokutaarifu.');
  String get personaliseDesc   => _t('Personalise how FlowerScout looks and behaves.', 'Personalisha jinsi FlowerScout inavyoonekana na kutenda.');
  String get versionLabel      => _t('Version 1.0.0 · Flutter',   'Toleo 1.0.0 · Flutter');
  String get logOut            => _t('Log out of FlowerScout',     'Toka kwenye FlowerScout');
  String get themeSystem       => _t('System default', 'Chaguo-msingi la mfumo');
  String get themeLight        => _t('Light',  'Mwanga');
  String get themeDark         => _t('Dark',   'Giza');
  String get mapSatellite      => _t('Satellite', 'Setilaiti');
  String get mapTerrain        => _t('Terrain',   'Ardhi');
  String get mapStreet         => _t('Street',    'Mtaa');
  String get dateFmtDMY        => _t('DD/MM/YYYY',      'DD/MM/YYYY');
  String get dateFmtMDY        => _t('MM/DD/YYYY',      'MM/DD/YYYY');
  String get dateFmtISO        => _t('YYYY-MM-DD (ISO)','YYYY-MM-DD (ISO)');
  String get roleScout         => _t('Scout',   'Mkaguzi');
  String get roleViewer        => _t('Viewer',  'Mtazamaji');
  String get roleManager       => _t('Manager', 'Msimamizi');
  String get weeklyDescFull    => _t('Every Monday 7 AM – farm health digest', 'Kila Jumatatu saa 1 asubuhi – muhtasari wa afya ya shamba');
  String get showHeatmapDesc   => _t('Auto-display scouting heatmap when opening Maps', 'Onyesha ramani ya ukaguzi moja kwa moja unapofungua Ramani');

  // -- Offline sync --
  String get offlineQueuedSingle  => _t('Report saved locally — will sync when online', 'Ripoti imehifadhiwa — itasawazishwa mtandaoni');
  String get offlineQueuedPlural  => _t('reports queued — will sync when online', 'ripoti zimehifadhiwa — zitasawazishwa mtandaoni');
  String get offlineSyncedSingle  => _t('queued report synced', 'ripoti iliyohifadhiwa imesawazishwa');
  String get offlineSyncedPlural  => _t('queued reports synced', 'ripoti zilizohifadhiwa zimesawazishwa');
  String get offlineDeadLetter    => _t('could not sync — contact admin', 'haikuweza kusawazishwa — wasiliana na msimamizi');
  String get offlineNoConn        => _t('No connection', 'Hakuna mtandao');

  String _t(String en, String sw) => languageCode == 'sw' ? sw : en;

  // ── Reports extra ────────────────────────────────────────────────────────
  String get today           => _t('Today',          'Leo');
  String get last7Days       => _t('Last 7 Days',    'Siku 7 Zilizopita');
  String get last30Days      => _t('Last 30 Days',   'Siku 30 Zilizopita');
  String get last3Months     => _t('Last 3 Months',  'Miezi 3 Iliyopita');
  String get allGreenhouses  => _t('All Greenhouses','Vyumba Vyote');
  String get allVarieties    => _t('All Varieties',  'Aina Zote');
  String get loadingReports  => _t('Loading reports...','Inapakia ripoti...');
  String get noReportsYet    => _t('No inspections found for this period.','Hakuna ukaguzi kwa kipindi hiki.');
  String get errorLoadReports=> _t('Could not load reports','Ripoti hazijapakia');
  String get exportPdfDesc   => _t('A PDF report will be generated for the current filters.','Ripoti ya PDF itatengenezwa kwa vichujio vya sasa.');
  String get exportExcelDesc => _t('An Excel file with all inspection data will be saved.','Faili la Excel lenye data yote litahifadhiwa.');
  String get waterStressShort=> _t('Water Stress','Msongo wa Maji');
  String get openingInspect  => _t('Opening inspection...','Inafungua ukaguzi...');
  String get signOutQ        => _t('Sign out?','Toka?');

  // -- Location permission --
  String get locationBlocked    => _t('Location blocked',       'Eneo limezuiwa');
  String get allowLocationAccess=> _t('Allow location access',  'Ruhusu ufikiaji wa eneo');
  String get recordsTrail       => _t('Records your walking trail across the farm', 'Inarekodia njia yako ya kutembea shambani');
  String get tracksZones        => _t('Tracks which farm zones are covered or missed', 'Inafuatilia maeneo ya shamba yaliyofunikwa au kukosekana');
  String get powersAnalytics    => _t('Powers distance and coverage analytics', 'Inasaidia uchambuzi wa umbali na ufunikaji');
  String get allowWhileUsing    => _t('Allow while using app',  'Ruhusu wakati wa kutumia programu');
  String get notNow             => _t('Not now',                'Si sasa');

  // -- Topbar / notifications --
  String get justNow            => _t('Just now',               'Sasa hivi');
  String get partlyCloudy       => _t('Partly Cloudy',          'Mawingu kidogo');
  String get feelsLike          => _t('Feels like',             'Inahisi kama');
  String get highSeverityAlert  => _t('High Severity Alert',    'Tahadhari ya Ukali Mkubwa');
  String get pestOutbreak       => _t('Potential pest outbreak detected', 'Mlipuko wa wadudu unaowezekana umegunduliwa');
  String get inspectionDue      => _t('Inspection Due',         'Ukaguzi Unastahili');
  String get reportReady        => _t('Report Ready',           'Ripoti Iko Tayari');
  String get weeklySummaryReady => _t('Weekly scouting summary is ready to view', 'Muhtasari wa ukaguzi wa kila wiki uko tayari kutazamwa');
  String get irrigationAlert    => _t('Irrigation Alert',       'Tahadhari ya Umwagiliaji');
  String get markAllRead        => _t('Mark all read',          'Weka yote kama imesomwa');
  String get allCaughtUp        => _t('All caught up!',         'Umesoma yote!');
  String get noNewNotifications => _t('No new notifications',   'Hakuna arifa mpya');

  // -- Chart labels full --
  List<String> get chartLabels30DaysFull => languageCode=='sw'
    ? ['Wiki 1','Wiki 2','Wiki 3','Wiki 4','Wiki 5']
    : ['Week 1','Week 2','Week 3','Week 4','Week 5'];

}