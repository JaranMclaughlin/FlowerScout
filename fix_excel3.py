import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

text = text.replace(
    "                if(mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(\n                  content: Text('Excel export failed: \\$e'),\n                  backgroundColor: AppColors.critical,\n                  behavior: SnackBarBehavior.floating));",
    "                if(mounted) { ScaffoldMessenger.of(context).showSnackBar(SnackBar(\n                  content: Text('Excel export failed: \\$e'),\n                  backgroundColor: AppColors.critical,\n                  behavior: SnackBarBehavior.floating)); }"
)

p.write_text(text, encoding='utf-8')
print("Done.")