import pathlib

p = pathlib.Path('lib/shared/theme/app_colors.dart')
text = p.read_text(encoding='utf-8')

text = text.replace(
    "  static const Color disease       = Color(0xFFD32F2F);",
    "  static const Color disease       = Color(0xFFD32F2F);\n  static const Color diseaseBg     = Color(0xFFFDF0F0);"
)
text = text.replace(
    "  static const Color high = Color(0xFFEF6C00);",
    "  static const Color high      = Color(0xFFEF6C00);\n  static const Color warningBg  = Color(0xFFFFF8ED);"
)

p.write_text(text, encoding='utf-8')
print("AppColors: diseaseBg + warningBg added.")