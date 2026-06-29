import pathlib, sys

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

# 1. Add share_plus import
old_import = "import 'package:printing/printing.dart';"
new_import = "import 'package:printing/printing.dart';\nimport 'package:share_plus/share_plus.dart';"
if old_import not in text:
    sys.exit("Import anchor not found.")
text = text.replace(old_import, new_import, 1)

# 2. Add WhatsApp chip next to Excel chip
old_chips = """          _exportChip(Icons.picture_as_pdf_outlined,'PDF',AppColors.disease,()=>_showExport('pdf',s)),
          const SizedBox(width:8),
          _exportChip(Icons.table_chart_outlined,'Excel',AppColors.leaf,()=>_showExport('excel',s)),"""
new_chips = """          _exportChip(Icons.picture_as_pdf_outlined,'PDF',AppColors.disease,()=>_showExport('pdf',s)),
          const SizedBox(width:8),
          _exportChip(Icons.table_chart_outlined,'Excel',AppColors.leaf,()=>_showExport('excel',s)),
          const SizedBox(width:8),
          _exportChip(Icons.share_rounded,'Share',const Color(0xFF25D366),()=>_shareWhatsApp(s)),"""
if old_chips not in text:
    sys.exit("Chips anchor not found.")
text = text.replace(old_chips, new_chips, 1)

# 3. Add _shareWhatsApp method before _showExport
old_show = "  void _showExport(String type, AppStrings s){"
new_show = """  void _shareWhatsApp(AppStrings s) {
    final stats = _stats;
    final period = {
      'today': s.today, '7days': s.last7Days,
      '30days': s.last30Days, '3months': s.last3Months,
    }[_period] ?? _period;
    final lines = [
      '*FlowerScout Report* — $period',
      '',
      '📊 *Summary*',
      '• Inspections: ${stats.total}',
      '• Disease: ${stats.disease}',
      '• Pests: ${stats.pest}',
      '• Critical: ${stats.critical}',
      '',
      '🏆 *Top Greenhouses*',
      ...stats.topGreenhouses.take(3).map((g) => '• ${g.gh}: ${g.findings} findings (${g.topIssue})'),
      '',
      '📅 Generated: ${DateTime.now().toString().split(' ').first}',
      '_via FlowerScout_',
    ];
    SharePlus.instance.share(ShareParams(text: lines.join('\n')));
  }

  void _showExport(String type, AppStrings s){"""
if old_show not in text:
    sys.exit("showExport anchor not found.")
text = text.replace(old_show, new_show, 1)

p.write_text(text, encoding='utf-8')
print("reports_screen.dart: WhatsApp share added.")