import pathlib

p = pathlib.Path('lib/features/dashboard/presentation/dashboard_screen.dart')
text = p.read_text(encoding='utf-8')

# Remove BOM
text = text.lstrip('\ufeff')

# Remove duplicate locale_provider import (keep the first one on line 3)
text = text.replace(
    "import '../../../shared/providers/analytics_data.dart';\nimport '../../../shared/providers/locale_provider.dart';",
    "import '../../../shared/providers/analytics_data.dart';"
)

p.write_text(text, encoding='utf-8')
print("Done.")