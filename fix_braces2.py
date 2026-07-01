import pathlib

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
text = p.read_text(encoding='utf-8')

old = """      if (!hasNetwork) {
      try {"""
new = """      if (!hasNetwork) {
        try {"""
if old not in text:
    raise SystemExit("Anchor A not found.")
text = text.replace(old, new, 1)

old2 = """        }
      } else {
        // Genuine error while online — show it instead of masking as offline.
        if (mounted) {
          setState(() { _submitting = false; _submitted = false; });
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            backgroundColor: AppColors.critical,
            behavior: SnackBarBehavior.floating,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            content: Text('Submit failed: \\$e',
                style: const TextStyle(color: Colors.white)),
          ));
        }
      }
      } catch (queueError) {
        if (mounted) {
          setState(() { _submitting = false; _submitted = false; });
          AppErrorHandler.showError(context, queueError, context2: 'submit inspection report');
        }
      }
    }
  }"""

new2 = """        }
        } catch (queueError) {
          if (mounted) {
            setState(() { _submitting = false; _submitted = false; });
            AppErrorHandler.showError(context, queueError, context2: 'submit inspection report');
          }
        }
      } else {
        // Genuine error while online — show it instead of masking as offline.
        if (mounted) {
          setState(() { _submitting = false; _submitted = false; });
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            backgroundColor: AppColors.critical,
            behavior: SnackBarBehavior.floating,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            content: Text('Submit failed: \\$e',
                style: const TextStyle(color: Colors.white)),
          ));
        }
      }
    }
  }"""

if old2 not in text:
    raise SystemExit("Anchor B not found — no changes made, need to inspect further.")
text = text.replace(old2, new2, 1)

p.write_text(text, encoding='utf-8')
print("Brace structure fixed: try/catch closes correctly, if/else attached to connectivity check.")