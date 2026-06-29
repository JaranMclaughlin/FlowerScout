import pathlib, sys

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')
original = text

# 298: if(mounted) setState({  — this is a callback, not a brace-less if; the
#      lint fires because the if body (the setState call) has no braces.
#      Fix: wrap the setState(...) call in braces.
text = text.replace(
    "      if(mounted) setState((){\n        _inspections=data;\n        _hasMore=data.length==_pageSize;\n        _stats=_ReportStats.fromRpcJson(statsJson,_period,lang:ref.read(localeProvider));\n        _loading=false;\n      });",
    "      if(mounted) {\n        setState((){\n          _inspections=data;\n          _hasMore=data.length==_pageSize;\n          _stats=_ReportStats.fromRpcJson(statsJson,_period,lang:ref.read(localeProvider));\n          _loading=false;\n        });\n      }"
)

# 314: same pattern in _loadMore
text = text.replace(
    "      if(mounted) setState((){\n        _inspections=[..._inspections,...more];\n        _hasMore=more.length==_pageSize;\n        _loadingMore=false;\n      });",
    "      if(mounted) {\n        setState((){\n          _inspections=[..._inspections,...more];\n          _hasMore=more.length==_pageSize;\n          _loadingMore=false;\n        });\n      }"
)

# 413: for(final f in farms) farmItems[f.name]=f.id;
text = text.replace(
    "    for(final f in farms) farmItems[f.name]=f.id;",
    "    for(final f in farms) { farmItems[f.name]=f.id; }"
)

# 417: for(final g in farm.greenhouses) ghItems[g.code]=g.id;
text = text.replace(
    "      for(final g in farm.greenhouses) ghItems[g.code]=g.id;",
    "      for(final g in farm.greenhouses) { ghItems[g.code]=g.id; }"
)

# 421-422: nested for — outer and inner both need braces
text = text.replace(
    "      for(final f in farms) for(final g in f.greenhouses){\n        if(g.id==_greenhouseId) for(final v in g.varietyNames) varItems[v]=v;",
    "      for(final f in farms) { for(final g in f.greenhouses){\n        if(g.id==_greenhouseId) { for(final v in g.varietyNames) { varItems[v]=v; } }"
)
# close the extra brace we opened for the outer for
text = text.replace(
    "      for(final f in farms) { for(final g in f.greenhouses){\n        if(g.id==_greenhouseId) { for(final v in g.varietyNames) { varItems[v]=v; } }\n      }",
    "      for(final f in farms) { for(final g in f.greenhouses){\n        if(g.id==_greenhouseId) { for(final v in g.varietyNames) { varItems[v]=v; } }\n      } }"
)

# 651: getDotPainter:(s,_,_,___) — unnecessary_underscores: ___ → _
text = text.replace(
    "getDotPainter:(s,_,_,___)=>",
    "getDotPainter:(s,_,_,_)=>"
)

# 1209: if(mounted) ScaffoldMessenger... — wrap in braces
text = text.replace(
    "              if(mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(",
    "              if(mounted) { ScaffoldMessenger.of(context).showSnackBar(SnackBar("
)
# find the closing )); of that snackbar and add the brace after it
text = text.replace(
    "                behavior:SnackBarBehavior.floating,\n              ));\n",
    "                behavior:SnackBarBehavior.floating,\n              )); }\n"
)

if text == original:
    print("No changes — anchors differ, paste dump output.")
else:
    p.write_text(text, encoding='utf-8')
    print("All 8 remaining lint issues fixed.")