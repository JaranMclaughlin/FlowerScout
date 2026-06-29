import pathlib

# ── 1. Add short week labels to app_strings.dart ─────────────────────
p = pathlib.Path('lib/shared/l10n/app_strings.dart')
text = p.read_text(encoding='utf-8')

text = text.replace(
    "  List<String> get chartLabelsWeek    => languageCode=='sw'\n    ? ['Jumatatu','Jumanne','Jumatano','Alhamisi','Ijumaa','Jumamosi','Jumapili']\n    : ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];",
    "  List<String> get chartLabelsWeek    => languageCode=='sw'\n    ? ['Jumatatu','Jumanne','Jumatano','Alhamisi','Ijumaa','Jumamosi','Jumapili']\n    : ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];\n\n  List<String> get chartLabelsWeekShort => languageCode=='sw'\n    ? ['Jum','Jum','Jua','Alh','Iju','Jums','Jmap']\n    : ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];"
)

# ── 2. Add offline/sync strings ───────────────────────────────────────
text = text.replace(
    "  String _t(String en, String sw) => languageCode == 'sw' ? sw : en;",
    """  // -- Offline sync --
  String get offlineQueuedSingle  => _t('Report saved locally — will sync when online', 'Ripoti imehifadhiwa — itasawazishwa mtandaoni');
  String get offlineQueuedPlural  => _t('reports queued — will sync when online', 'ripoti zimehifadhiwa — zitasawazishwa mtandaoni');
  String get offlineSyncedSingle  => _t('queued report synced', 'ripoti iliyohifadhiwa imesawazishwa');
  String get offlineSyncedPlural  => _t('queued reports synced', 'ripoti zilizohifadhiwa zimesawazishwa');
  String get offlineDeadLetter    => _t('could not sync — contact admin', 'haikuweza kusawazishwa — wasiliana na msimamizi');
  String get offlineNoConn        => _t('No connection', 'Hakuna mtandao');

  String _t(String en, String sw) => languageCode == 'sw' ? sw : en;"""
)

p.write_text(text, encoding='utf-8')
print("app_strings.dart: short week labels + offline strings added.")