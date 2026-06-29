import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

old_sev_stack = """        pw.Expanded(
          child: pw.Stack(children: [
            pw.Container(height: 8, decoration: pw.BoxDecoration(color: PdfColors.grey200, borderRadius: pw.BorderRadius.circular(4))),
            pw.FractionallySizedBox(
              widthFactor: pct.clamp(0.02, 1.0),
              child: pw.Container(height: 8, decoration: pw.BoxDecoration(color: color, borderRadius: pw.BorderRadius.circular(4))),
            ),
          ]),
        ),"""
new_sev_stack = """        pw.Expanded(
          child: pw.Container(
            height: 8,
            decoration: pw.BoxDecoration(color: PdfColors.grey200, borderRadius: pw.BorderRadius.circular(4)),
            child: pw.Row(children: [
              pw.Expanded(
                flex: (pct.clamp(0.02, 1.0) * 1000).round(),
                child: pw.Container(decoration: pw.BoxDecoration(color: color, borderRadius: pw.BorderRadius.circular(4))),
              ),
              pw.Expanded(
                flex: ((1 - pct.clamp(0.02, 1.0)) * 1000).round().clamp(1, 1000),
                child: pw.Container(),
              ),
            ]),
          ),
        ),"""
count = text.count(old_sev_stack)
if count == 0:
    raise SystemExit("FractionallySizedBox block anchor not found - aborting, no changes made.")
text = text.replace(old_sev_stack, new_sev_stack)
print(f"Replaced {count} occurrence(s) of FractionallySizedBox with flex-based bar.")

old_leaf = "    const leaf = PdfColor.fromInt(0xFF40916C);\n"
if old_leaf not in text:
    raise SystemExit("Unused 'leaf' variable anchor not found - aborting, no changes made.")
text = text.replace(old_leaf, "", 1)

p.write_text(text, encoding='utf-8')
print("reports_screen.dart fixed: flex-based progress bars instead of FractionallySizedBox, removed unused variable.")