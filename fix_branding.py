import pathlib, sys

# ── 1. Login screen ───────────────────────────────────────────────────
p = pathlib.Path('lib/features/auth/presentation/login_screen.dart')
text = p.read_text(encoding='utf-8')

# Replace flower icon with VP Group logo
text = text.replace(
    "const Icon(Icons.local_florist, size: 52, color: Color(0xFF2E7D32))",
    "Image.asset('assets/images/vp_group_logo.png', height: 80)"
)
# Also replace any Container wrapping the icon if needed
text = text.replace(
    "Container(\n              width: 96, height: 96,\n              decoration: BoxDecoration(\n                color: const Color(0xFFD4AF37).withValues(alpha: 0.15),\n                shape: BoxShape.circle,\n              ),\n              child: const Icon(Icons.local_florist, size: 52, color: Color(0xFF2E7D32)),\n            ),",
    "Image.asset('assets/images/vp_group_logo.png', height: 100),"
)

p.write_text(text, encoding='utf-8')
print("login_screen.dart: logo wired.")

# ── 2. Splash screen in main.dart ────────────────────────────────────
p2 = pathlib.Path('lib/main.dart')
text2 = p2.read_text(encoding='utf-8')

text2 = text2.replace(
    "Container(\n              width: 96, height: 96,\n              decoration: BoxDecoration(\n                color: const Color(0xFFD4AF37).withValues(alpha: 0.15),\n                shape: BoxShape.circle,\n              ),\n              child: const Icon(Icons.local_florist, size: 52, color: Color(0xFF2E7D32)),\n            ),",
    "Image.asset('assets/images/vp_group_logo.png', height: 100),"
)

p2.write_text(text2, encoding='utf-8')
print("main.dart: splash logo wired.")

# ── 3. PDF header — replace text logo with image ──────────────────────
p3 = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text3 = p3.read_text(encoding='utf-8')

# Update PDF header text to show VP Group branding
text3 = text3.replace(
    "                pw.Text('Flower Scout', style: pw.TextStyle(fontSize: 20, fontWeight: pw.FontWeight.bold, color: PdfColors.white)),\n                pw.Text('Inspection Report', style: pw.TextStyle(fontSize: 12, color: mist)),",
    "                pw.Text('VP GROUP', style: pw.TextStyle(fontSize: 20, fontWeight: pw.FontWeight.bold, color: PdfColors.white)),\n                pw.Text('FlowerScout · Inspection Report', style: pw.TextStyle(fontSize: 11, color: mist)),"
)

p3.write_text(text3, encoding='utf-8')
print("reports_screen.dart: PDF header branded.")