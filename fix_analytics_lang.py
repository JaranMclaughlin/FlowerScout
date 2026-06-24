import pathlib, re

p = pathlib.Path('lib/shared/providers/analytics_data.dart')
txt = p.read_text(encoding='utf-8')

# Fix 1: InspectionRecord.fromRow - add lang param
txt = txt.replace(
    'factory InspectionRecord.fromRow(Map<String, dynamic> r) {',
    'factory InspectionRecord.fromRow(Map<String, dynamic> r, String lang) {'
)

# Fix 2: ReportStats.empty() - drop const, add lang param
txt = txt.replace(
    'static ReportStats empty() => const ReportStats(',
    'static ReportStats empty(String lang) => ReportStats('
)

# Fix 3: ReportStats.fromInspections - add lang param
txt = txt.replace(
    'factory ReportStats.fromInspections(\n    List<InspectionRecord> ins, String period, DateTime since,\n  ) {',
    'factory ReportStats.fromInspections(\n    List<InspectionRecord> ins, String period, DateTime since, String lang,\n  ) {'
)

# Fix 4: _buildTrend call site - pass lang through
txt = txt.replace(
    'final buckets = _buildTrend(ins, period, since);',
    'final buckets = _buildTrend(ins, period, since, lang);'
)

# Fix 5: _buildTrend signature - add lang param
txt = txt.replace(
    'static Map<String, List<dynamic>> _buildTrend(\n    List<InspectionRecord> ins, String period, DateTime since,\n  ) {',
    'static Map<String, List<dynamic>> _buildTrend(\n    List<InspectionRecord> ins, String period, DateTime since, String lang,\n  ) {'
)

p.write_text(txt, encoding='utf-8')
print('done')