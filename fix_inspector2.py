import pathlib, sys

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

# 1. Add inspectorName to _Inspection model
text = text.replace(
    "  final String id, date, gh, variety, category, severity, inspectorId;",
    "  final String id, date, gh, variety, category, severity, inspectorId, inspectorName;"
)
text = text.replace(
    "    required this.severity, required this.inspectorId,\n    required this.dateTime,\n  });",
    "    required this.severity, required this.inspectorId,\n    this.inspectorName = '',\n    required this.dateTime,\n  });"
)

# 2. Wire inspectorName from the RPC/fetch result
text = text.replace(
    "      inspectorId: scoutId.length >= 8 ? scoutId.substring(0, 8) : scoutId,\n    );",
    "      inspectorId: scoutId.length >= 8 ? scoutId.substring(0, 8) : scoutId,\n      inspectorName: r['scout_name'] as String? ?? '',\n    );"
)

# 3. Add Scout column to table header
text = text.replace(
    "    final header = Padding(\n      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),\n      child: Row(children: [",
    "    final header = Padding(\n      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),\n      child: Row(children: [\n              Expanded(flex: 2, child: Text('Scout',\n                style: const TextStyle(fontSize: 10, fontWeight: FontWeight.w700,\n                    letterSpacing: 0.5, color: AppColors.slate))),"
)

# 4. Add scout name to each table row
text = text.replace(
    "              Expanded(flex: 2, child: Text(r.date,\n                style: const TextStyle(fontSize: 12, color: AppColors.graphite))),",
    "              Expanded(flex: 2, child: Text(\n                r.inspectorName.isNotEmpty ? r.inspectorName : r.inspectorId,\n                style: const TextStyle(fontSize: 11, color: AppColors.forest,\n                    fontWeight: FontWeight.w600),\n                overflow: TextOverflow.ellipsis)),\n              Expanded(flex: 2, child: Text(r.date,\n                style: const TextStyle(fontSize: 12, color: AppColors.graphite))),"
)

# 5. Add Scout column to PDF export
text = text.replace(
    "          headers: ['Date', 'GH', 'Variety', 'Category', 'Severity'],",
    "          headers: ['Scout', 'Date', 'GH', 'Variety', 'Category', 'Severity'],"
)
text = text.replace(
    "          data: rows.map((r) => [r.date, r.gh, r.variety, r.category, r.severity]).toList(),",
    "          data: rows.map((r) => [r.inspectorName.isNotEmpty ? r.inspectorName : r.inspectorId, r.date, r.gh, r.variety, r.category, r.severity]).toList(),"
)

p.write_text(text, encoding='utf-8')
print("reports_screen.dart: inspector name wired into table + PDF.")