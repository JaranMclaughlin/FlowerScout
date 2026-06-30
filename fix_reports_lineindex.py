import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines(keepends=True)

# Sanity-check we're targeting the right lines before touching anything
assert "catch(e) {" in lines[1404], f"Line 1405 mismatch: {lines[1404]!r}"
assert "Excel export failed" in lines[1406], f"Line 1407 mismatch: {lines[1406]!r}"
assert lines[1409] == '              }\n', f"Line 1410 mismatch: {lines[1409]!r}"

assert "catch(e){" in lines[1421], f"Line 1422 mismatch: {lines[1421]!r}"
assert "PDF export failed" in lines[1424], f"Line 1425 mismatch: {lines[1424]!r}"
assert lines[1427] == '            }\n', f"Line 1428 mismatch: {lines[1427]!r}"

# Replace Excel block: lines 1405-1410 (0-indexed 1404-1409)
excel_replacement = [
    "              } catch(e) {\n",
    "                if(mounted) AppErrorHandler.showError(context, e, context2: 'excel export');\n",
    "              }\n",
]
new_lines = lines[:1404] + excel_replacement + lines[1410:]

# Recompute PDF block offset: original PDF block was lines 1422-1428 (0-indexed 1421-1427),
# but it shifted because the Excel block changed from 6 lines to 3 lines (shrank by 3).
offset = 1421 - 3
assert "catch(e){" in new_lines[offset], f"Shifted PDF anchor mismatch: {new_lines[offset]!r}"

pdf_replacement = [
    "            } catch(e){\n",
    "              if(mounted) Navigator.pop(context);\n",
    "              if(mounted) AppErrorHandler.showError(context, e, context2: 'pdf export');\n",
    "            }\n",
]
pdf_end = offset + (1428 - 1421)  # original block length
new_lines = new_lines[:offset] + pdf_replacement + new_lines[pdf_end:]

# Add the import
for i, line in enumerate(new_lines):
    if "import 'package:supabase_flutter/supabase_flutter.dart';" in line:
        new_lines.insert(i + 1, "import '../../../shared/error/app_error_handler.dart';\n")
        break
else:
    raise SystemExit("Could not find import anchor line - aborting, no changes made.")

p.write_text(''.join(new_lines), encoding='utf-8')
print("reports_screen.dart updated via line-index replacement (bypassing whitespace-matching issues).")