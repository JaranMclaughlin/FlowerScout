import pathlib

# ── Fix maps_screen.dart ──────────────────────────────────────────────────────
p = pathlib.Path('lib/features/maps/presentation/maps_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')

for i, l in enumerate(lines, 1):
    if "child: const Text('Cancel')" in l:
        lines[i-1] = l.replace("child: const Text('Cancel')", "child: Text(AppStrings.of(ref.watch(localeProvider)).cancel)")
        print(f"Fixed maps_screen line {i}")

p.write_text('\n'.join(lines), encoding='utf-8')

# ── Fix reports_screen.dart ───────────────────────────────────────────────────
p2 = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
lines2 = p2.read_text(encoding='utf-8').split('\n')

for i, l in enumerate(lines2, 1):
    if "Text('Error: \$e')" in l:
        lines2[i-1] = l.replace("Text('Error: \$e')", "Text(AppStrings.of(ref.watch(localeProvider)).errorUnexpected)")
        print(f"Fixed reports_screen line {i}: Error text")
    if "child: const Text('Retry')" in l or "child: Text('Retry')" in l:
        lines2[i-1] = l.replace("const Text('Retry')", "Text(AppStrings.of(ref.watch(localeProvider)).retry)")
        lines2[i-1] = lines2[i-1].replace("Text('Retry')", "Text(AppStrings.of(ref.watch(localeProvider)).retry)")
        print(f"Fixed reports_screen line {i}: Retry text")
    if "Excel export failed:" in l:
        lines2[i-1] = re.sub(
            r"'Excel export failed: \\?\\\$e'",
            "'\${AppStrings.of(ref.watch(localeProvider)).excelExportFailed}: \$e'",
            lines2[i-1])
        print(f"Fixed reports_screen line {i}: Excel export failed")
    if "PDF export failed:" in l:
        lines2[i-1] = re.sub(
            r"'PDF export failed: \\\$e'",
            "'\${AppStrings.of(ref.watch(localeProvider)).pdfExportFailed}: \$e'",
            lines2[i-1])
        print(f"Fixed reports_screen line {i}: PDF export failed")

p2.write_text('\n'.join(lines2), encoding='utf-8')

import re
print("Done.")