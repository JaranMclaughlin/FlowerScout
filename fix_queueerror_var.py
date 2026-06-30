import pathlib

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
text = p.read_text(encoding='utf-8')

old = """      } catch (queueError) {
        if (mounted) {
          setState(() { _submitting = false; _submitted = false; });
          AppErrorHandler.showError(context, e, context2: 'submit inspection report');
        }"""
new = """      } catch (queueError) {
        if (mounted) {
          setState(() { _submitting = false; _submitted = false; });
          AppErrorHandler.showError(context, queueError, context2: 'submit inspection report');
        }"""
if old not in text:
    raise SystemExit("Anchor not found - aborting, no changes made.")
text = text.replace(old, new, 1)

p.write_text(text, encoding='utf-8')
print("scouting_screen.dart fixed: error handler now references the correct exception variable (queueError, not the outer e).")