import pathlib, sys

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

# 1. Add findings list to _Inspection model
text = text.replace(
    "  final String id, date, gh, variety, category, severity, inspectorId, inspectorName;\n  final DateTime dateTime;\n  const _Inspection({\n    required this.id, required this.date, required this.gh,",
    "  final String id, date, gh, variety, category, severity, inspectorId, inspectorName;\n  final DateTime dateTime;\n  final List<Map<String,dynamic>> findings;\n  const _Inspection({\n    required this.id, required this.date, required this.gh,"
)
text = text.replace(
    "    this.inspectorName = '',\n    required this.dateTime,\n  });",
    "    this.inspectorName = '',\n    this.findings = const [],\n    required this.dateTime,\n  });"
)

# 2. Wire findings into fromRow
text = text.replace(
    "      inspectorName: r['scout_name'] as String? ?? '',\n    );",
    "      inspectorName: r['scout_name'] as String? ?? '',\n      findings: (r['inspection_findings'] as List? ?? [])\n          .map((f) => Map<String,dynamic>.from(f as Map)).toList(),\n    );"
)

# 3. Replace snackbar tap with detail bottom sheet
text = text.replace(
    "          onTap: () => ScaffoldMessenger.of(context).showSnackBar(SnackBar(\n            content: Text('${r.date} · ${r.gh} · ${r.variety}'),\n            behavior: SnackBarBehavior.floating,\n            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),\n          )),",
    "          onTap: () => _showInspectionDetail(context, r, s),"
)

# 4. Add _showInspectionDetail method before _shareWhatsApp
text = text.replace(
    "  void _shareWhatsApp(AppStrings s) {",
    """  void _showInspectionDetail(BuildContext context, _Inspection r, AppStrings s) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (_) => DraggableScrollableSheet(
        initialChildSize: 0.6,
        maxChildSize: 0.92,
        minChildSize: 0.4,
        builder: (_, ctrl) => Container(
          decoration: const BoxDecoration(
            color: AppColors.surface,
            borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
          ),
          child: Column(children: [
            Container(
              width: 40, height: 4,
              margin: const EdgeInsets.symmetric(vertical: 12),
              decoration: BoxDecoration(color: AppColors.divider, borderRadius: BorderRadius.circular(2)),
            ),
            Expanded(child: ListView(controller: ctrl, padding: const EdgeInsets.fromLTRB(20,0,20,32), children: [
              // Header
              Row(children: [
                Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text('${r.gh} · ${r.variety}', style: const TextStyle(fontSize: 16,
                      fontWeight: FontWeight.w700, color: AppColors.ink)),
                  const SizedBox(height: 4),
                  Text('${r.date}${r.inspectorName.isNotEmpty ? " · ${r.inspectorName}" : ""}',
                      style: const TextStyle(fontSize: 12, color: AppColors.slate)),
                ])),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: AppColors.severityBg(r.severity),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(r.severity, style: TextStyle(fontSize: 11,
                      fontWeight: FontWeight.w600, color: AppColors.severityColor(r.severity))),
                ),
              ]),
              const SizedBox(height: 20),
              const Divider(),
              const SizedBox(height: 12),
              // Findings
              if (r.findings.isEmpty)
                const Text('No findings recorded.', style: TextStyle(color: AppColors.slate))
              else
                ...r.findings.map((f) {
                  final cat = f['category'] as String? ?? '';
                  final sev = f['severity'] as String? ?? '';
                  final issue = f['issue'] as String? ?? '';
                  final photos = (f['photo_urls'] as List? ?? []).cast<String>();
                  return Container(
                    margin: const EdgeInsets.only(bottom: 16),
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: AppColors.background,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: AppColors.divider),
                    ),
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Row(children: [
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                          decoration: BoxDecoration(
                            color: AppColors.categoryColor(cat).withValues(alpha: 0.10),
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Text(cat, style: TextStyle(fontSize: 11,
                              fontWeight: FontWeight.w600, color: AppColors.categoryColor(cat))),
                        ),
                        const SizedBox(width: 8),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                          decoration: BoxDecoration(
                            color: AppColors.severityBg(sev),
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Text(sev, style: TextStyle(fontSize: 11,
                              fontWeight: FontWeight.w600, color: AppColors.severityColor(sev))),
                        ),
                      ]),
                      if (issue.isNotEmpty) ...[
                        const SizedBox(height: 8),
                        Text(issue, style: const TextStyle(fontSize: 13, color: AppColors.graphite, height: 1.4)),
                      ],
                      if (photos.isNotEmpty) ...[
                        const SizedBox(height: 12),
                        SizedBox(
                          height: 90,
                          child: ListView.separated(
                            scrollDirection: Axis.horizontal,
                            itemCount: photos.length,
                            separatorBuilder: (_, _) => const SizedBox(width: 8),
                            itemBuilder: (_, i) => ClipRRect(
                              borderRadius: BorderRadius.circular(8),
                              child: Image.network(photos[i],
                                width: 90, height: 90, fit: BoxFit.cover,
                                errorBuilder: (_, _, _) => Container(
                                  width: 90, height: 90,
                                  color: AppColors.surfaceAlt,
                                  child: const Icon(Icons.broken_image_rounded, color: AppColors.slate),
                                ),
                              ),
                            ),
                          ),
                        ),
                      ],
                    ]),
                  );
                }),
            ])),
          ]),
        ),
      ),
    );
  }

  void _shareWhatsApp(AppStrings s) {"""
)

p.write_text(text, encoding='utf-8')
print("reports_screen.dart: inspection detail bottom sheet with photos added.")