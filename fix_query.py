import pathlib

# Fix the query — remove the bad FK hint, use separate profile lookup
rp = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
rc = rp.read_text(encoding='utf-8')

old_select = """      .select(\'\'\'
        id, submitted_at, started_at, variety_name, greenhouse_id,
        greenhouses!inner(code),
        user_profiles!scout_id(full_name),
        inspection_findings(category, severity)
      \'\'\')"""

new_select = """      .select(\'\'\'
        id, submitted_at, started_at, variety_name, greenhouse_id, scout_id,
        greenhouses!inner(code),
        inspection_findings(category, severity)
      \'\'\')"""

rc = rc.replace(old_select, new_select)

# Fix fromRow — profile no longer joined, use scout_id directly
old_from_row = """    final profile = r['user_profiles'] as Map<String, dynamic>?;
    return _Inspection(
      id: r['id']?.toString() ?? '',
      date: date,
      gh: r['greenhouse_code'] as String? ?? r['greenhouse_id']?.toString() ?? '—',
      variety: r['variety_name'] as String? ?? '—',
      category: topCat,
      severity: topSev,
      inspectorName: profile?['full_name'] as String? ?? 'Unknown',
    );"""

new_from_row = """    return _Inspection(
      id: r['id']?.toString() ?? '',
      date: date,
      gh: r['greenhouse_code'] as String? ?? r['greenhouse_id']?.toString() ?? '—',
      variety: r['variety_name'] as String? ?? '—',
      category: topCat,
      severity: topSev,
      inspectorName: r['scout_id']?.toString().substring(0, 8) ?? 'Unknown',
    );"""

rc = rc.replace(old_from_row, new_from_row)

# Remove profile hydration from factory
old_hydrate = """    final profile = row['user_profiles'];
    if (profile is Map) row['user_profiles'] = Map<String, dynamic>.from(profile);"""
new_hydrate = ""
rc = rc.replace(old_hydrate, new_hydrate)

rp.write_text(rc, encoding='utf-8')
print('query fixed')