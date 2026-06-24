import pathlib

p = pathlib.Path('lib/shared/l10n/app_strings.dart')
t = p.read_text(encoding='utf-8')

new_strings = """
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
    ? ['Jtt','Jmo','Jtn','Alh','Ijm','Jum','Jps']
    : ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];

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
"""

anchor = "  String _t(String en, String sw) => languageCode == 'sw' ? sw : en;"
if anchor not in t:
    raise SystemExit('anchor not found')
t = t.replace(anchor, new_strings + '\n  ' + anchor.strip())
p.write_text(t, encoding='utf-8')
print('app_strings.dart updated.')