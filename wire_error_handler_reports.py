import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

# 1. Add the import
old_import = "import 'package:supabase_flutter/supabase_flutter.dart';"
new_import = "import 'package:supabase_flutter/supabase_flutter.dart';\nimport '../../../shared/error/app_error_handler.dart';"
if old_import not in text:
    raise SystemExit("Import anchor not found - aborting, no changes made.")
text = text.replace(old_import, new_import, 1)

# 2. Excel export error - also fixes the literal '\$e' bug (was showing
#    the text "$e" instead of the actual exception, due to an escaped dollar sign)
old_excel = """              } catch(e) {
                if(mounted) {ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                  content: Text('Excel export failed: \\$e'),
                  backgroundColor: AppColors.critical,
                  behavior: SnackBarBehavior.floating)); }
              }"""
new_excel = """              } catch(e) {
                if(mounted) AppErrorHandler.showError(context, e, context2: 'excel export');
              }"""
if old_excel not in text:
    raise SystemExit("Excel export catch block anchor not found - aborting, no changes made.")
text = text.replace(old_excel, new_excel, 1)

# 3. PDF export error
old_pdf = """              if(mounted) Navigator.pop(context);
              if(mounted) {ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                content:Text('PDF export failed: $e'),
                behavior:SnackBarBehavior.floating,
                shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(10)))); }
            }"""
new_pdf = """              if(mounted) Navigator.pop(context);
              if(mounted) AppErrorHandler.showError(context, e, context2: 'pdf export');
            }"""
if old_pdf not in text:
    raise SystemExit("PDF export catch block anchor not found - aborting, no changes made.")
text = text.replace(old_pdf, new_pdf, 1)

p.write_text(text, encoding='utf-8')
print("reports_screen.dart updated: PDF/Excel export errors now use AppErrorHandler (friendly messages, real exception logged).")