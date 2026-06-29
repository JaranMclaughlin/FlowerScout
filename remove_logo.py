import pathlib

# 1. Login screen — restore flower icon
p = pathlib.Path('lib/features/auth/presentation/login_screen.dart')
text = p.read_text(encoding='utf-8')
text = text.replace(
    "Image.asset('assets/images/vp_group_logo.png', height: 100),",
    "Container(\n              width: 96, height: 96,\n              decoration: BoxDecoration(\n                color: const Color(0xFFD4AF37).withValues(alpha: 0.15),\n                shape: BoxShape.circle,\n              ),\n              child: const Icon(Icons.local_florist, size: 52, color: Color(0xFF2E7D32)),\n            ),"
)
text = text.replace(
    "Image.asset('assets/images/vp_group_logo.png', height: 80)",
    "const Icon(Icons.local_florist, size: 52, color: Color(0xFF2E7D32))"
)
p.write_text(text, encoding='utf-8')
print("login_screen.dart: restored.")

# 2. Splash screen — restore flower icon
p2 = pathlib.Path('lib/main.dart')
text2 = p2.read_text(encoding='utf-8')
text2 = text2.replace(
    "Image.asset('assets/images/vp_group_logo.png', height: 100),",
    "Container(\n              width: 96, height: 96,\n              decoration: BoxDecoration(\n                color: const Color(0xFFD4AF37).withValues(alpha: 0.15),\n                shape: BoxShape.circle,\n              ),\n              child: const Icon(Icons.local_florist, size: 52, color: Color(0xFF2E7D32)),\n            ),"
)
p2.write_text(text2, encoding='utf-8')
print("main.dart: restored.")

# 3. App shell — restore flower icon
p3 = pathlib.Path('lib/shared/widgets/app_shell.dart')
text3 = p3.read_text(encoding='utf-8')
text3 = text3.replace(
    "                  child: Image.asset('assets/images/vp_group_logo.png', height: 22, fit: BoxFit.contain),",
    "                  child: const Icon(Icons.local_florist,\n                      color: AppColors.leaf, size: 18),"
)
p3.write_text(text3, encoding='utf-8')
print("app_shell.dart: restored.")

# 4. PDF header — restore FlowerScout branding
p4 = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text4 = p4.read_text(encoding='utf-8')
text4 = text4.replace(
    "                pw.Text('VP GROUP', style: pw.TextStyle(fontSize: 20, fontWeight: pw.FontWeight.bold, color: PdfColors.white)),\n                pw.Text('FlowerScout · Inspection Report', style: pw.TextStyle(fontSize: 11, color: mist)),",
    "                pw.Text('Flower Scout', style: pw.TextStyle(fontSize: 20, fontWeight: pw.FontWeight.bold, color: PdfColors.white)),\n                pw.Text('Inspection Report', style: pw.TextStyle(fontSize: 12, color: mist)),"
)
p4.write_text(text4, encoding='utf-8')
print("reports_screen.dart: PDF restored.")