import pathlib, re

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
text = p.read_text(encoding='utf-8')

# 1. Add AppColors import
text = text.replace(
    "import '../../../core/offline/offline_sync_service.dart';",
    "import '../../../core/offline/offline_sync_service.dart';\nimport '../../../shared/theme/app_colors.dart';"
)

# 2. Remove the _C class entirely
text = re.sub(
    r'\nclass _C \{.*?\}\n',
    '\n',
    text,
    count=1,
    flags=re.DOTALL
)

# 3. Replace all _C.x references with AppColors equivalents
replacements = [
    ('_C.forest',    'AppColors.forest'),
    ('_C.canopy',    'AppColors.canopy'),
    ('_C.leaf',      'AppColors.leaf'),
    ('_C.mint',      'AppColors.mint'),
    ('_C.mist',      'AppColors.mist'),
    ('_C.cream',     'AppColors.background'),
    ('_C.paper',     'AppColors.surface'),
    ('_C.ink',       'AppColors.ink'),
    ('_C.graphite',  'AppColors.graphite'),
    ('_C.slate',     'AppColors.slate'),
    ('_C.fog',       'AppColors.surfaceAlt'),
    ('_C.divider',   'AppColors.divider'),
    ('_C.disease',   'AppColors.disease'),
    ('_C.pest',      'AppColors.pest'),
    ('_C.water',     'AppColors.water'),
    ('_C.nutrition', 'AppColors.nutrition'),
    ('_C.irrigation','AppColors.irrigation'),
    ('_C.other',     'AppColors.other'),
    ('_C.high',      'AppColors.high'),
    ('_C.critical',  'AppColors.critical'),
]
for old, new in replacements:
    text = text.replace(old, new)

# 4. Replace remaining hardcoded hex that match AppColors tokens
# _FindingCard uses raw hex — replace with AppColors
text = text.replace("const Color(0xFF6B7F6E)", "AppColors.slate")
text = text.replace("const Color(0xFF2D6A4F)", "AppColors.canopy")
text = text.replace("const Color(0xFFDDE5DD)", "AppColors.divider")
text = text.replace("const Color(0xFFEAEFEA)", "AppColors.surfaceAlt")
text = text.replace("const Color(0xFF3D4F42)", "AppColors.graphite")
text = text.replace("const Color(0xFF0D1B0F)", "AppColors.ink")
text = text.replace("const Color(0xFFF8FAF8)", "AppColors.background")
text = text.replace("const Color(0xFFD32F2F)", "AppColors.disease")
text = text.replace("const Color(0xFFE65100)", "AppColors.pest")
text = text.replace("const Color(0xFF0277BD)", "AppColors.water")
text = text.replace("const Color(0xFF388E3C)", "AppColors.nutrition")
text = text.replace("const Color(0xFF00838F)", "AppColors.irrigation")
text = text.replace("const Color(0xFF455A64)", "AppColors.other")

p.write_text(text, encoding='utf-8')
print("scouting_screen.dart: _C eliminated, AppColors wired.")