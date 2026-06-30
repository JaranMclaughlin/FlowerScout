import pathlib

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
text = p.read_text(encoding='utf-8')

# Check if the import already exists (it may already be imported via a shared path)
import_check = "import '../../../shared/error/app_error_handler.dart';"
if import_check not in text:
    old_import = "import 'package:supabase_flutter/supabase_flutter.dart';"
    if old_import not in text:
        raise SystemExit("Import anchor not found - aborting, no changes made.")
    new_import = old_import + "\nimport '../../../shared/error/app_error_handler.dart';"
    text = text.replace(old_import, new_import, 1)
    print("Added AppErrorHandler import.")
else:
    print("AppErrorHandler import already present, skipping.")

old_block = """        if (mounted) {
          setState(() { _submitting = false; _submitted = false; });
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            content: Text('${ref.read(stringsProvider).failedToSubmit}$e'),
            backgroundColor: AppColors.critical,
          ));
        }"""
new_block = """        if (mounted) {
          setState(() { _submitting = false; _submitted = false; });
          AppErrorHandler.showError(context, e, context2: 'submit inspection report');
        }"""
if old_block not in text:
    raise SystemExit("Submit error block anchor not found - aborting, no changes made.")
text = text.replace(old_block, new_block, 1)

p.write_text(text, encoding='utf-8')
print("scouting_screen.dart updated: report submission error now uses AppErrorHandler.")