import pathlib
import re

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

old_block_start = "  pw.Widget _pdfKpi(String label, String value) => pw.Expanded("
old_block_end_marker = "  void _showExport(String type, AppStrings s){"

start_idx = text.find(old_block_start)
end_idx = text.find(old_block_end_marker)
if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
    raise SystemExit("Could not locate PDF generation block - aborting, no changes made.")

new_block = """  pw.Widget _pdfKpi(String label, String value, PdfColor accent, PdfColor bg) => pw.Expanded(
        child: pw.Container(
          margin: const pw.EdgeInsets.only(right: 8),
          padding: const pw.EdgeInsets.all(10),
          decoration: pw.BoxDecoration(
            color: bg,
            borderRadius: pw.BorderRadius.circular(8),
            border: pw.Border.all(color: accent, width: 0.5),
          ),
          child: pw.Column(
            crossAxisAlignment: pw.CrossAxisAlignment.start,
            children: [
              pw.Text(value, style: pw.TextStyle(fontSize: 20, fontWeight: pw.FontWeight.bold, color: accent)),
              pw.SizedBox(height: 2),
              pw.Text(label, style: pw.TextStyle(fontSize: 9, color: PdfColors.grey700)),
            ],
          ),
        ),
      );

  PdfColor _pdfSeverityColor(String severity) {
    switch (severity.toLowerCase()) {
      case 'critical': return PdfColor.fromInt(0xFF7A1F1F);
      case 'high':      return PdfColor.fromInt(0xFFB53030);
      case 'medium':    return PdfColor.fromInt(0xFF9A5C00);
      default:          return PdfColor.fromInt(0xFF40916C);
    }
  }

  PdfColor _pdfCategoryColor(String category) {
    final c = category.toLowerCase();
    if (c.contains('disease')) return PdfColor.fromInt(0xFFB53030);
    if (c.contains('pest'))    return PdfColor.fromInt(0xFF9A5C00);
    if (c.contains('water'))   return PdfColor.fromInt(0xFF1565C0);
    return PdfColor.fromInt(0xFF40916C);
  }

  pw.Widget _pdfSeverityRow(String label, int value, int maxValue) {
    final color = _pdfSeverityColor(label);
    final pct = maxValue == 0 ? 0.0 : value / maxValue;
    return pw.Padding(
      padding: const pw.EdgeInsets.symmetric(vertical: 4),
      child: pw.Row(children: [
        pw.Container(width: 8, height: 8, decoration: pw.BoxDecoration(color: color, shape: pw.BoxShape.circle)),
        pw.SizedBox(width: 8),
        pw.SizedBox(width: 70, child: pw.Text(label, style: const pw.TextStyle(fontSize: 10))),
        pw.Expanded(
          child: pw.Stack(children: [
            pw.Container(height: 8, decoration: pw.BoxDecoration(color: PdfColors.grey200, borderRadius: pw.BorderRadius.circular(4))),
            pw.FractionallySizedBox(
              widthFactor: pct.clamp(0.02, 1.0),
              child: pw.Container(height: 8, decoration: pw.BoxDecoration(color: color, borderRadius: pw.BorderRadius.circular(4))),
            ),
          ]),
        ),
        pw.SizedBox(width: 8),
        pw.SizedBox(width: 24, child: pw.Text('$value', textAlign: pw.TextAlign.right,
            style: pw.TextStyle(fontSize: 10, fontWeight: pw.FontWeight.bold))),
      ]),
    );
  }

  pw.Widget _pdfCategoryRow(String label, int value, int maxValue) {
    final color = _pdfCategoryColor(label);
    final pct = maxValue == 0 ? 0.0 : value / maxValue;
    return pw.Padding(
      padding: const pw.EdgeInsets.symmetric(vertical: 4),
      child: pw.Row(children: [
        pw.SizedBox(width: 90, child: pw.Text(label, style: const pw.TextStyle(fontSize: 10))),
        pw.Expanded(
          child: pw.Stack(children: [
            pw.Container(height: 8, decoration: pw.BoxDecoration(color: PdfColors.grey200, borderRadius: pw.BorderRadius.circular(4))),
            pw.FractionallySizedBox(
              widthFactor: pct.clamp(0.02, 1.0),
              child: pw.Container(height: 8, decoration: pw.BoxDecoration(color: color, borderRadius: pw.BorderRadius.circular(4))),
            ),
          ]),
        ),
        pw.SizedBox(width: 8),
        pw.SizedBox(width: 24, child: pw.Text('$value', textAlign: pw.TextAlign.right,
            style: pw.TextStyle(fontSize: 10, fontWeight: pw.FontWeight.bold))),
      ]),
    );
  }

  Future<Uint8List> _generatePdfReport(AppStrings s, List<_Inspection> rows) async {
    final doc=pw.Document();
    final stats=_stats;
    const forest = PdfColor.fromInt(0xFF1B4332);
    const leaf = PdfColor.fromInt(0xFF40916C);
    const mist = PdfColor.fromInt(0xFFD8F3DC);
    const redAccent = PdfColor.fromInt(0xFFB53030);
    const redBg = PdfColor.fromInt(0xFFFDF0F0);
    const amberAccent = PdfColor.fromInt(0xFF9A5C00);
    const amberBg = PdfColor.fromInt(0xFFFFF8ED);
    const criticalAccent = PdfColor.fromInt(0xFF7A1F1F);
    const criticalBg = PdfColor.fromInt(0xFFFDE8E8);

    final maxSev = stats.bySeverity.values.isEmpty ? 1 : stats.bySeverity.values.reduce((a,b)=>a>b?a:b);
    final maxCat = stats.byCategory.values.isEmpty ? 1 : stats.byCategory.values.reduce((a,b)=>a>b?a:b);

    doc.addPage(pw.MultiPage(
      pageFormat: PdfPageFormat.a4,
      margin: const pw.EdgeInsets.all(28),
      header: (context) => pw.Container(
        padding: const pw.EdgeInsets.fromLTRB(20, 16, 20, 16),
        margin: const pw.EdgeInsets.only(bottom: 16),
        decoration: pw.BoxDecoration(
          color: forest,
          borderRadius: pw.BorderRadius.circular(10),
        ),
        child: pw.Row(
          mainAxisAlignment: pw.MainAxisAlignment.spaceBetween,
          children: [
            pw.Column(
              crossAxisAlignment: pw.CrossAxisAlignment.start,
              children: [
                pw.Text('Flower Scout', style: pw.TextStyle(fontSize: 20, fontWeight: pw.FontWeight.bold, color: PdfColors.white)),
                pw.Text('Inspection Report', style: pw.TextStyle(fontSize: 12, color: mist)),
              ],
            ),
            pw.Text('Generated \${DateTime.now().toString().split(\".\").first}',
                style: pw.TextStyle(fontSize: 9, color: mist)),
          ],
        ),
      ),
      build: (context) => [
        pw.Text('Summary', style: pw.TextStyle(fontSize: 14, fontWeight: pw.FontWeight.bold, color: forest)),
        pw.SizedBox(height: 8),
        pw.Row(children: [
          _pdfKpi('Inspections', '\${stats.total}', forest, mist),
          _pdfKpi('Disease', '\${stats.disease}', redAccent, redBg),
          _pdfKpi('Pests', '\${stats.pest}', amberAccent, amberBg),
          _pdfKpi('Critical', '\${stats.critical}', criticalAccent, criticalBg),
        ]),
        pw.SizedBox(height: 18),
        pw.Text('Severity Breakdown', style: pw.TextStyle(fontSize: 13, fontWeight: pw.FontWeight.bold, color: forest)),
        pw.SizedBox(height: 8),
        ...stats.bySeverity.entries.map((e) => _pdfSeverityRow(e.key, e.value, maxSev)),
        pw.SizedBox(height: 18),
        pw.Text('Findings by Category', style: pw.TextStyle(fontSize: 13, fontWeight: pw.FontWeight.bold, color: forest)),
        pw.SizedBox(height: 8),
        ...stats.byCategory.entries.map((e) => _pdfCategoryRow(e.key, e.value, maxCat)),
        pw.SizedBox(height: 18),
        pw.Text('Top Greenhouses', style: pw.TextStyle(fontSize: 13, fontWeight: pw.FontWeight.bold, color: forest)),
        pw.SizedBox(height: 8),
        pw.Table(
          columnWidths: const {0: pw.FlexColumnWidth(1), 1: pw.FlexColumnWidth(2), 2: pw.FlexColumnWidth(1)},
          children: stats.topGreenhouses.map((g) => pw.TableRow(children: [
            pw.Padding(padding: const pw.EdgeInsets.symmetric(vertical: 4),
                child: pw.Container(
                  padding: const pw.EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                  decoration: pw.BoxDecoration(color: mist, borderRadius: pw.BorderRadius.circular(4)),
                  child: pw.Text(g.gh, style: pw.TextStyle(fontSize: 9, fontWeight: pw.FontWeight.bold, color: forest)))),
            pw.Padding(padding: const pw.EdgeInsets.symmetric(vertical: 4),
                child: pw.Text(g.topIssue, style: const pw.TextStyle(fontSize: 10))),
            pw.Padding(padding: const pw.EdgeInsets.symmetric(vertical: 4),
                child: pw.Text('\${g.findings} findings', style: pw.TextStyle(fontSize: 10, fontWeight: pw.FontWeight.bold), textAlign: pw.TextAlign.right)),
          ])).toList(),
        ),
        pw.SizedBox(height: 20),
        pw.Text('Inspection Records (\${rows.length})', style: pw.TextStyle(fontSize: 13, fontWeight: pw.FontWeight.bold, color: forest)),
        pw.SizedBox(height: 8),
        pw.TableHelper.fromTextArray(
          headers: ['Date', 'GH', 'Variety', 'Category', 'Severity'],
          data: rows.map((r) => [r.date, r.gh, r.variety, r.category, r.severity]).toList(),
          headerStyle: pw.TextStyle(fontWeight: pw.FontWeight.bold, fontSize: 9, color: PdfColors.white),
          cellStyle: const pw.TextStyle(fontSize: 9),
          headerDecoration: pw.BoxDecoration(color: forest),
          cellHeight: 22,
          rowDecoration: const pw.BoxDecoration(border: pw.Border(bottom: pw.BorderSide(color: PdfColors.grey300, width: 0.5))),
          oddRowDecoration: pw.BoxDecoration(color: PdfColor.fromInt(0xFFF5F6F8)),
          cellAlignments: const {0: pw.Alignment.centerLeft, 1: pw.Alignment.center, 2: pw.Alignment.centerLeft,
              3: pw.Alignment.centerLeft, 4: pw.Alignment.centerLeft},
        ),
      ],
    ));

    return doc.save();
  }

"""

text = text[:start_idx] + new_block + text[end_idx:]
p.write_text(text, encoding='utf-8')
print("reports_screen.dart updated: PDF now uses branded colors, severity/category bars, colored greenhouse table, fixed missing em-dash glyphs.")