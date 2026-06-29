import pathlib, re

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

# 1. Hide Border from excel import to avoid clash with Flutter's Border
text = text.replace(
    "import 'package:excel/excel.dart';",
    "import 'package:excel/excel.dart' hide Border;"
)

# 2. Fix List<int> → Uint8List for XFile.fromData
text = text.replace(
    "  Future<List<int>> _generateExcelReport(AppStrings s, List<_Inspection> rows) async {",
    "  Future<Uint8List> _generateExcelReport(AppStrings s, List<_Inspection> rows) async {"
)
text = text.replace(
    "    if (encoded == null) throw Exception('Failed to encode Excel file');\n    return encoded;",
    "    if (encoded == null) throw Exception('Failed to encode Excel file');\n    return Uint8List.fromList(encoded);"
)

# 3. Add Uint8List import if missing
if "import 'dart:typed_data';" not in text:
    text = text.replace(
        "import 'dart:async';",
        "import 'dart:async';\nimport 'dart:typed_data';"
    )

# 4. Fix curly_braces
text = re.sub(
    r'(?m)\b((?:else\s+)?if)\s*(\([^)]*\))\s*\r?\n(\s+[^\n{][^\n]*;)',
    lambda m: f"{m.group(1)}{m.group(2)} {{\n{m.group(3)}\n}}",
    text
)

p.write_text(text, encoding='utf-8')
print("Fixed: Border clash, Uint8List, curly braces.")