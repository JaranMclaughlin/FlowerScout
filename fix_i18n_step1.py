import pathlib, re

# ── Step 1: Add missing keys to app_strings.dart ─────────────────────────────
p = pathlib.Path('lib/shared/l10n/app_strings.dart')
s = p.read_text(encoding='utf-8')

# Add retry + export error keys near errorUnexpected
old_anchor = "  String get errorUnexpected    => _t('An unexpected error occurred.',         'Hitilafu isiyotarajiwa imetokea.');"
new_anchor  = """  String get errorUnexpected    => _t('An unexpected error occurred.',         'Hitilafu isiyotarajiwa imetokea.');
  String get retry              => _t('Retry',                                  'Jaribu tena');
  String get exportFailed       => _t('Export failed',                          'Usafirishaji umeshindwa');
  String get excelExportFailed  => _t('Excel export failed',                    'Usafirishaji wa Excel umeshindwa');
  String get pdfExportFailed    => _t('PDF export failed',                      'Usafirishaji wa PDF umeshindwa');"""

if old_anchor in s:
    s = s.replace(old_anchor, new_anchor, 1)
    p.write_text(s, encoding='utf-8')
    print("Step 1: added retry + export error keys")
else:
    print("ERROR: app_strings anchor not found"); raise SystemExit(1)

# ── Step 2: Fix maps_screen.dart - hardcoded 'Cancel' ────────────────────────
p2 = pathlib.Path('lib/features/maps/presentation/maps_screen.dart')
t2 = p2.read_text(encoding='utf-8')

# Need to know what s reference is in maps_screen
# Check if it uses AppStrings
has_strings = 'AppStrings' in t2 or 'stringsProvider' in t2 or 'localeProvider' in t2
print(f"Step 2: maps_screen has strings: {has_strings}")

# Show the Cancel context
lines2 = t2.split('\n')
for i, l in enumerate(lines2, 1):
    if 'Cancel' in l:
        print(f"  {i}: {l}")