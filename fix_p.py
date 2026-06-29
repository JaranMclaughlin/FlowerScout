import pathlib, re

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

# 1. Add AppColors import after the last existing import
text = text.replace(
    "import '../../../shared/theme/app_colors.dart';",
    "import '../../../shared/theme/app_colors.dart';"
)
# In case it is not already imported
if "shared/theme/app_colors.dart" not in text:
    text = re.sub(
        r"(import '[^']+app_strings\.dart';)",
        r"\1\nimport '../../../shared/theme/app_colors.dart';",
        text, count=1
    )

# 2. Remove _P class
text = re.sub(
    r'\nclass _P \{.*?\}\n',
    '\n',
    text, count=1, flags=re.DOTALL
)

# 3. Replace all _P.x with AppColors equivalents
replacements = [
    ('_P.bg',       'AppColors.background'),
    ('_P.surface',  'AppColors.surface'),
    ('_P.border',   'AppColors.border'),
    ('_P.ink',      'AppColors.ink'),
    ('_P.graphite', 'AppColors.graphite'),
    ('_P.slate',    'AppColors.slate'),
    ('_P.forest',   'AppColors.forest'),
    ('_P.canopy',   'AppColors.canopy'),
    ('_P.leaf',     'AppColors.leaf'),
    ('_P.mint',     'AppColors.mint'),
    ('_P.mist',     'AppColors.mist'),
    ('_P.red',      'AppColors.disease'),
    ('_P.redBg',    'const Color(0xFFFDF0F0)'),
    ('_P.amber',    'AppColors.warning'),
    ('_P.amberBg',  'const Color(0xFFFFF8ED)'),
    ('_P.blue',     'AppColors.info'),
    ('_P.blueBg',   'const Color(0xFFEEF4FF)'),
    ('_P.divider',  'AppColors.divider'),
]
for old, new in replacements:
    text = text.replace(old, new)

p.write_text(text, encoding='utf-8')
print("reports_screen.dart: _P eliminated, AppColors wired.")