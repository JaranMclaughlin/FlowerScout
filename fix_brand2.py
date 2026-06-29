import pathlib

# ── Excel export — add VP Group branding to sheet ────────────────────
p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

# Add a title row above headers in Excel
text = text.replace(
    "    // Header row\n    final headers = ['Date', 'Scout', 'GH', 'Variety', 'Category', 'Severity'];",
    """    // Title row
    final titleCell = sheet.cell(CellIndex.indexByColumnRow(columnIndex: 0, rowIndex: 0));
    titleCell.value = TextCellValue('VP GROUP — FlowerScout Inspection Report');
    titleCell.cellStyle = CellStyle(
      bold: true,
      fontSize: 14,
      fontColorHex: ExcelColor.fromHexString('#1B4332'),
    );
    sheet.merge(CellIndex.indexByColumnRow(columnIndex: 0, rowIndex: 0),
                CellIndex.indexByColumnRow(columnIndex: 5, rowIndex: 0));

    final dateCell = sheet.cell(CellIndex.indexByColumnRow(columnIndex: 0, rowIndex: 1));
    dateCell.value = TextCellValue('Generated: \${DateTime.now().toString().split(\\' \\').first}');
    dateCell.cellStyle = CellStyle(fontColorHex: ExcelColor.fromHexString('#6B7F6E'));
    sheet.merge(CellIndex.indexByColumnRow(columnIndex: 0, rowIndex: 1),
                CellIndex.indexByColumnRow(columnIndex: 5, rowIndex: 1));

    // Header row
    final headers = ['Date', 'Scout', 'GH', 'Variety', 'Category', 'Severity'];"""
)

# Shift data rows down by 2 (title + date rows)
text = text.replace(
    "      final cell = sheet.cell(CellIndex.indexByColumnRow(columnIndex: i, rowIndex: 0));",
    "      final cell = sheet.cell(CellIndex.indexByColumnRow(columnIndex: i, rowIndex: 2));"
)
text = text.replace(
    "        final cell = sheet.cell(CellIndex.indexByColumnRow(columnIndex: ci, rowIndex: ri + 1));",
    "        final cell = sheet.cell(CellIndex.indexByColumnRow(columnIndex: ci, rowIndex: ri + 3));"
)

p.write_text(text, encoding='utf-8')
print("Excel: VP Group branding added.")

# ── App shell nav — replace flower icon with VP Group initials ────────
p2 = pathlib.Path('lib/shared/widgets/app_shell.dart')
text2 = p2.read_text(encoding='utf-8')

text2 = text2.replace(
    "                  child: const Icon(Icons.local_florist,\n                      color: AppColors.leaf, size: 18),",
    "                  child: Image.asset('assets/images/vp_group_logo.png', height: 22, fit: BoxFit.contain),"
)

p2.write_text(text2, encoding='utf-8')
print("app_shell.dart: nav logo branded.")