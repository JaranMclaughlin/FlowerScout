import pathlib
import re

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

# 1. Add imports for PDF generation
old_imports = "import 'package:supabase_flutter/supabase_flutter.dart';"
new_imports = """import 'package:supabase_flutter/supabase_flutter.dart';
import 'dart:typed_data';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;
import 'package:printing/printing.dart';"""
if old_imports not in text:
    raise SystemExit("Imports anchor not found - aborting, no changes made.")
text = text.replace(old_imports, new_imports, 1)

# 2. Refactor _filtered into a reusable helper
old_filtered = """  List<_Inspection> get _filtered {
    if (_activeFilter=='all') return _inspections;
    if (_activeFilter=='critical') return _inspections.where((r)=>r.severity.toLowerCase()=='critical').toList();
    return _inspections.where((r)=>r.category.toLowerCase().contains(_activeFilter)).toList();
  }"""
new_filtered = """  List<_Inspection> _applyActiveFilter(List<_Inspection> source) {
    if (_activeFilter=='all') return source;
    if (_activeFilter=='critical') return source.where((r)=>r.severity.toLowerCase()=='critical').toList();
    return source.where((r)=>r.category.toLowerCase().contains(_activeFilter)).toList();
  }
  List<_Inspection> get _filtered => _applyActiveFilter(_inspections);"""
if old_filtered not in text:
    raise SystemExit("_filtered anchor not found - aborting, no changes made.")
text = text.replace(old_filtered, new_filtered, 1)

# 3. Add a full (unpaginated) fetch for export, right after _loadMore()
old_loadmore = """  Future<void> _loadMore() async {
    if(_loadingMore || !_hasMore) return;
    setState(()=>_loadingMore=true);
    try {
      final more=await _fetchInspections(_period,
        farmId:_farmId,greenhouseId:_greenhouseId,variety:_variety,
        offset:_inspections.length,limit:_pageSize,lang:ref.read(localeProvider));
      if(mounted) setState((){
        _inspections=[..._inspections,...more];
        _hasMore=more.length==_pageSize;
        _loadingMore=false;
      });
    } catch(e){ if(mounted) setState(()=>_loadingMore=false); }
  }"""
new_loadmore = old_loadmore + """

  // Export needs every matching record, not just whatever page is loaded
  // on screen - fetch fresh, independent of the table's pagination state.
  Future<List<_Inspection>> _fetchAllForExport() async {
    const cap=2000, batch=200;
    final all=<_Inspection>[];
    int offset=0;
    while(true){
      final page=await _fetchInspections(_period,
          farmId:_farmId,greenhouseId:_greenhouseId,variety:_variety,
          offset:offset,limit:batch,lang:ref.read(localeProvider));
      all.addAll(page);
      if(page.length<batch || all.length>=cap) break;
      offset+=batch;
    }
    return all;
  }"""
if old_loadmore not in text:
    raise SystemExit("_loadMore anchor not found - aborting, no changes made.")
text = text.replace(old_loadmore, new_loadmore, 1)

# 4. Replace _showExport: real PDF generation + wiring instead of a stub.
#    Tolerate any amount of blank-line whitespace before BoxDecoration _card().
pattern = re.compile(
    r"  void _showExport\(String type, AppStrings s\)\{.*?\n  \}\n\s*\n*(?=  BoxDecoration _card\(\)=>BoxDecoration\()",
    re.DOTALL,
)

pdf_helpers = """  // \u2500\u2500 PDF generation \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
  pw.Widget _pdfKpi(String label, String value) => pw.Expanded(
        child: pw.Container(
          margin: const pw.EdgeInsets.only(right: 8),
          padding: const pw.EdgeInsets.all(8),
          decoration: pw.BoxDecoration(
            border: pw.Border.all(color: PdfColors.grey300),
            borderRadius: pw.BorderRadius.circular(6),
          ),
          child: pw.Column(
            crossAxisAlignment: pw.CrossAxisAlignment.start,
            children: [
              pw.Text(value, style: pw.TextStyle(fontSize: 18, fontWeight: pw.FontWeight.bold)),
              pw.Text(label, style: const pw.TextStyle(fontSize: 9, color: PdfColors.grey700)),
            ],
          ),
        ),
      );

  Future<Uint8List> _generatePdfReport(AppStrings s, List<_Inspection> rows) async {
    final doc=pw.Document();
    final stats=_stats;

    doc.addPage(pw.MultiPage(
      pageFormat: PdfPageFormat.a4,
      margin: const pw.EdgeInsets.all(32),
      header: (context) => pw.Column(
        crossAxisAlignment: pw.CrossAxisAlignment.start,
        children: [
          pw.Text('Flower Scout \u2014 Inspection Report',
              style: pw.TextStyle(fontSize: 20, fontWeight: pw.FontWeight.bold)),
          pw.SizedBox(height: 4),
          pw.Text('Generated ${DateTime.now().toString().split(\".\").first}',
              style: const pw.TextStyle(fontSize: 9, color: PdfColors.grey700)),
          pw.Divider(),
        ],
      ),
      build: (context) => [
        pw.SizedBox(height: 8),
        pw.Text('Summary', style: pw.TextStyle(fontSize: 14, fontWeight: pw.FontWeight.bold)),
        pw.SizedBox(height: 8),
        pw.Row(children: [
          _pdfKpi('Inspections', '${stats.total}'),
          _pdfKpi('Disease', '${stats.disease}'),
          _pdfKpi('Pests', '${stats.pest}'),
          _pdfKpi('Critical', '${stats.critical}'),
        ]),
        pw.SizedBox(height: 16),
        pw.Text('Severity Breakdown', style: pw.TextStyle(fontSize: 14, fontWeight: pw.FontWeight.bold)),
        pw.SizedBox(height: 8),
        ...stats.bySeverity.entries.map((e) => pw.Padding(
              padding: const pw.EdgeInsets.symmetric(vertical: 2),
              child: pw.Row(mainAxisAlignment: pw.MainAxisAlignment.spaceBetween,
                  children: [pw.Text(e.key), pw.Text('${e.value}')]),
            )),
        pw.SizedBox(height: 16),
        pw.Text('Findings by Category', style: pw.TextStyle(fontSize: 14, fontWeight: pw.FontWeight.bold)),
        pw.SizedBox(height: 8),
        ...stats.byCategory.entries.map((e) => pw.Padding(
              padding: const pw.EdgeInsets.symmetric(vertical: 2),
              child: pw.Row(mainAxisAlignment: pw.MainAxisAlignment.spaceBetween,
                  children: [pw.Text(e.key), pw.Text('${e.value}')]),
            )),
        pw.SizedBox(height: 16),
        pw.Text('Top Greenhouses', style: pw.TextStyle(fontSize: 14, fontWeight: pw.FontWeight.bold)),
        pw.SizedBox(height: 8),
        ...stats.topGreenhouses.map((g) => pw.Padding(
              padding: const pw.EdgeInsets.symmetric(vertical: 2),
              child: pw.Row(mainAxisAlignment: pw.MainAxisAlignment.spaceBetween,
                  children: [pw.Text('${g.gh} \u2014 ${g.topIssue}'), pw.Text('${g.findings}')]),
            )),
        pw.SizedBox(height: 20),
        pw.Text('Inspection Records (${rows.length})', style: pw.TextStyle(fontSize: 14, fontWeight: pw.FontWeight.bold)),
        pw.SizedBox(height: 8),
        pw.TableHelper.fromTextArray(
          headers: ['Date', 'GH', 'Variety', 'Category', 'Severity'],
          data: rows.map((r) => [r.date, r.gh, r.variety, r.category, r.severity]).toList(),
          headerStyle: pw.TextStyle(fontWeight: pw.FontWeight.bold, fontSize: 9),
          cellStyle: const pw.TextStyle(fontSize: 9),
          headerDecoration: const pw.BoxDecoration(color: PdfColors.green100),
          cellHeight: 22,
        ),
      ],
    ));

    return doc.save();
  }

"""

new_show_export = """  void _showExport(String type, AppStrings s){
    showDialog(context:context,builder:(ctx)=>AlertDialog(
      shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(16)),
      title:Text(type=='pdf'?s.exportPdf:s.exportExcel,
        style:const TextStyle(fontFamily:'Georgia',fontSize:18)),
      content:Text(type=='pdf'?s.exportPdfDesc:s.exportExcelDesc),
      actions:[
        TextButton(onPressed:()=>Navigator.pop(ctx),child:Text(s.cancel)),
        ElevatedButton(
          onPressed:() async {
            Navigator.pop(ctx);
            if(type!='pdf'){
              ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                content:Text('${s.exportExcel} \u2014 coming soon'),
                behavior:SnackBarBehavior.floating,
                shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(10))));
              return;
            }
            showDialog(context:context,barrierDismissible:false,
              builder:(_)=>const Center(child:CircularProgressIndicator(color:_P.forest)));
            try {
              final allRecords=await _fetchAllForExport();
              final filtered=_applyActiveFilter(allRecords);
              final bytes=await _generatePdfReport(s,filtered);
              if(mounted) Navigator.pop(context);
              await Printing.layoutPdf(onLayout:(_) async => bytes,
                  name:'FlowerScout_Report_${DateTime.now().millisecondsSinceEpoch}.pdf');
            } catch(e){
              if(mounted) Navigator.pop(context);
              if(mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                content:Text('PDF export failed: $e'),
                behavior:SnackBarBehavior.floating,
                shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(10))));
            }
          },
          style:ElevatedButton.styleFrom(backgroundColor:_P.forest,foregroundColor:Colors.white,
            elevation:0,shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(8))),
          child:Text(s.download)),
      ]));
  }

"""

replacement = pdf_helpers + new_show_export
new_text, count = pattern.subn(replacement, text, count=1)
if count == 0:
    raise SystemExit("_showExport pattern not found - aborting, no changes made.")
text = new_text

p.write_text(text, encoding='utf-8')
print("reports_screen.dart updated: real PDF export wired (full-dataset fetch, KPI/severity/category/top-GH summary, inspection table).")