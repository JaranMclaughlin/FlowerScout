import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

# Replace raw hex with named tokens now that they exist
text = text.replace("const Color(0xFFFDF0F0)", "AppColors.diseaseBg")
text = text.replace("const Color(0xFFFFF8ED)", "AppColors.warningBg")

p.write_text(text, encoding='utf-8')
print("reports_screen.dart: diseaseBg + warningBg wired.")