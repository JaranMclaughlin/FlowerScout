import pathlib, re

screens = [
    'lib/features/scouting/presentation/scouting_screen.dart',
    'lib/features/dashboard/presentation/dashboard_screen.dart',
    'lib/features/maps/presentation/maps_screen.dart',
    'lib/features/reports/presentation/reports_screen.dart',
]

# Known non-UI strings to ignore
ignore = ['debugPrint', 'supabase', 'http', 'font', 'json', 
          'cache', 'queue', 'trail', 'image/', 'finding-photos',
          'inspection_', 'scout_', 'user_', 'farm_', 'greenhouse',
          'submitted', 'queued', 'started', '.dart', 'package:',
          'DD/MM', 'YYYY', 'v1_', '.toIso', 'rgba', '0xFF']

for screen in screens:
    p = pathlib.Path(screen)
    lines = p.read_text(encoding='utf-8').split('\n')
    hits = []
    for i, line in enumerate(lines, 1):
        # Find Text() widgets with hardcoded strings
        matches = re.findall(r"Text\('([^']{3,})'\)", line)
        for m in matches:
            if not any(ig.lower() in m.lower() for ig in ignore):
                hits.append(f"  {i}: {m!r}")
        # Find hardcoded label: or hint: strings
        matches2 = re.findall(r"(?:label|hint|title|message|content):\s*'([^']{3,})'", line)
        for m in matches2:
            if not any(ig.lower() in m.lower() for ig in ignore):
                hits.append(f"  {i}: [label/hint] {m!r}")
    if hits:
        print(f"\n=== {p.name} ===")
        for h in hits[:20]:
            print(h)