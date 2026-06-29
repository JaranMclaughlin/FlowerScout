import pathlib, sys

p = pathlib.Path('lib/shared/providers/analytics_data.dart')
text = p.read_text(encoding='utf-8')

old = """    final findings = r['inspection_findings'] as List?;
    final topCat = findings != null && findings.isNotEmpty
        ? (findings.first['category'] as String? ?? 'Other') : 'Other';
    final topSev = findings != null && findings.isNotEmpty
        ? (findings.first['severity'] as String? ?? 'Low') : 'Low';"""

new = """    final findings = r['inspection_findings'] as List?;
    // Pick the finding with the highest severity, not just the first one.
    const _sevRank = {'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1};
    String topCat = 'Other';
    String topSev = 'Low';
    if (findings != null && findings.isNotEmpty) {
      Map<String, dynamic> worst = Map<String, dynamic>.from(findings.first as Map);
      for (final f in findings) {
        final fm = f as Map;
        final rank = _sevRank[fm['severity'] as String? ?? 'Low'] ?? 1;
        final worstRank = _sevRank[worst['severity'] as String? ?? 'Low'] ?? 1;
        if (rank > worstRank) worst = Map<String, dynamic>.from(fm);
      }
      topCat = worst['category'] as String? ?? 'Other';
      topSev = worst['severity'] as String? ?? 'Low';
    }"""

if old not in text:
    sys.exit("Anchor not found.")
text = text.replace(old, new)
p.write_text(text, encoding='utf-8')
print("analytics_data.dart: severity aggregation fixed.")