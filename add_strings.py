import pathlib

p = pathlib.Path('lib/shared/l10n/app_strings.dart')
txt = p.read_text(encoding='utf-8')

# Add missing strings before the closing }
new_strings = """
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
  String get noData             => _t('No data',                'Hakuna data');

  // -- Chart labels full --
  List<String> get chartLabels30DaysFull => languageCode=='sw'
    ? ['Wiki 1','Wiki 2','Wiki 3','Wiki 4','Wiki 5']
    : ['Week 1','Week 2','Week 3','Week 4','Week 5'];
"""

txt = txt.replace('\n}', new_strings + '\n}', 1)
p.write_text(txt, encoding='utf-8')
print('done')