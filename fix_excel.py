import pathlib, sys

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

# 1. Add excel + share_plus imports if missing
if "import 'package:excel/excel.dart';" not in text:
    text = text.replace(
        "import 'package:share_plus/share_plus.dart';",
        "import 'package:share_plus/share_plus.dart';\nimport 'package:excel/excel.dart';"
    )

# 2. Replace "coming soon" with real Excel export
old_excel = """            if(type!='pdf'){
              ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                content:Text('${s.exportExcel} — coming soon'),
                behavior:SnackBarBehavior.floating,
                shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(10))));
              return;
            }"""

new_excel = """            if(type!='pdf'){
              Navigator.pop(ctx);
              try {
                final allRecords = await _fetchAllForExport();
                final filtered  = _applyActiveFilter(allRecords);
                final bytes     = await _generateExcelReport(s, filtered);
                final name      = 'FlowerScout_${DateTime.now().millisecondsSinceEpoch}.xlsx';
                await SharePlus.instance.share(ShareParams(
                  files: [XFile.fromData(bytes, name: name,
                    mimeType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')],
                  subject: name,
                ));
              } catch(e) {
                if(mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                  content: Text('Excel export failed: \$e'),
                  backgroundColor: AppColors.critical,
                  behavior: SnackBarBehavior.floating));
              }
              return;
            }"""

if old_excel not in text:
    sys.exit("Excel anchor not found.")
text = text.replace(old_excel, new_excel)

# 3. Add _generateExcelReport method before _shareWhatsApp
old_share = "  void _shareWhatsApp(AppStrings s) {"
new_excel_method = """  Future<List<int>> _generateExcelReport(AppStrings s, List<_Inspection> rows) async {
    final excel = Excel.createExcel();
    final sheet = excel['Inspections'];

    // Header row
    final headers = ['Date', 'Scout', 'GH', 'Variety', 'Category', 'Severity'];
    for (var i = 0; i < headers.length; i++) {
      final cell = sheet.cell(CellIndex.indexByColumnRow(columnIndex: i, rowIndex: 0));
      cell.value = TextCellValue(headers[i]);
      cell.cellStyle = CellStyle(
        bold: true,
        backgroundColorHex: ExcelColor.fromHexString('#1B4332'),
        fontColorHex: ExcelColor.fromHexString('#FFFFFF'),
      );
    }

    // Data rows
    for (var ri = 0; ri < rows.length; ri++) {
      final r = rows[ri];
      final rowData = [
        r.date,
        r.inspectorName.isNotEmpty ? r.inspectorName : r.inspectorId,
        r.gh,
        r.variety,
        r.category,
        r.severity,
      ];
      for (var ci = 0; ci < rowData.length; ci++) {
        final cell = sheet.cell(CellIndex.indexByColumnRow(columnIndex: ci, rowIndex: ri + 1));
        cell.value = TextCellValue(rowData[ci]);
        if (ri % 2 == 0) {
          cell.cellStyle = CellStyle(backgroundColorHex: ExcelColor.fromHexString('#F5F6F8'));
        }
      }
    }

    // Auto-fit columns
    sheet.setColumnWidth(0, 14);
    sheet.setColumnWidth(1, 20);
    sheet.setColumnWidth(2, 10);
    sheet.setColumnWidth(3, 18);
    sheet.setColumnWidth(4, 16);
    sheet.setColumnWidth(5, 12);

    final encoded = excel.encode();
    if (encoded == null) throw Exception('Failed to encode Excel file');
    return encoded;
  }

  void _shareWhatsApp(AppStrings s) {"""

if old_share not in text:
    sys.exit("shareWhatsApp anchor not found.")
text = text.replace(old_share, new_excel_method)

p.write_text(text, encoding='utf-8')
print("reports_screen.dart: Excel export implemented.")