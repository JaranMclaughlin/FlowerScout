import pathlib, sys

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

# 1. Add scout_name + full findings fields to query
text = text.replace(
    "    id, submitted_at, started_at, variety_name, greenhouse_id, scout_id,\n    greenhouses!inner(code),\n    inspection_findings(category, severity)",
    "    id, submitted_at, started_at, variety_name, greenhouse_id, scout_id, scout_name,\n    greenhouses!inner(code),\n    inspection_findings(category, severity, issue, photo_urls)"
)

# 2. Fix chart x-axis labels — use short week labels
# The reports screen _buildChartCard uses _stats.chartLabels
# _ReportStats.chartLabels is set in _fetchReportStatsRpc or fromRpcJson
# Find where chartLabels is used in the chart renderer and cap label length
text = text.replace(
    "return Padding(padding:const EdgeInsets.only(top:4),child:Text(labels[i],style:const TextStyle(fontSize:9,color:AppColors.slate)));",
    "final short=labels[i].length>3?labels[i].substring(0,3):labels[i];\n          return Padding(padding:const EdgeInsets.only(top:4),child:Text(short,style:const TextStyle(fontSize:9,color:AppColors.slate)));"
)

if text.count("final short=labels[i].length>3") == 0:
    sys.exit("Chart label anchor not found.")

p.write_text(text, encoding='utf-8')
print("Fixed: scout_name in query, findings fields, chart labels shortened.")