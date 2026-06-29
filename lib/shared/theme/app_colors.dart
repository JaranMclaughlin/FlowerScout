import 'package:flutter/material.dart';

class AppColors {
  // ── Existing (kept exactly as-is so nothing breaks) ─────────────────────────
  static const Color primaryGreen = Color(0xFF2E7D32);
  static const Color premiumGold  = Color(0xFFD4AF37);
  static const Color background   = Color(0xFFF8FAF8);
  static const Color critical     = Color(0xFFD32F2F);
  static const Color warning      = Color(0xFFF57C00);
  static const Color success      = Color(0xFF388E3C);
  static const Color textDark     = Color(0xFF212121);

  // ── New additive tokens (used by redesigned dynamic screens) ────────────────
  // Brand greens (matches scouting/settings screen palette)
  static const Color forest = Color(0xFF1B4332);
  static const Color canopy = Color(0xFF2D6A4F);
  static const Color leaf   = Color(0xFF40916C);
  static const Color mint   = Color(0xFF74C69D);
  static const Color mist   = Color(0xFFD8F3DC);

  // Surfaces / neutrals
  static const Color surface    = Color(0xFFFFFFFF);
  static const Color surfaceAlt = Color(0xFFEAEFEA);
  static const Color divider    = Color(0xFFDDE5DD);
  static const Color border     = Color(0xFFD3D1C7);

  // Text
  static const Color ink      = Color(0xFF0D1B0F);
  static const Color graphite = Color(0xFF3D4F42);
  static const Color slate    = Color(0xFF6B7F6E);
  static const Color muted    = Color(0xFF888780);

  // Severity (high added — critical/warning/success already existed above)
  static const Color high      = Color(0xFFEF6C00);
  static const Color warningBg  = Color(0xFFFFF8ED);
  static const Color info = Color(0xFF185FA5);

  static Color severityColor(String severity) {
    switch (severity.toLowerCase()) {
      case 'critical': return critical;
      case 'high':     return high;
      case 'medium':   return warning;
      case 'low':      return success;
      default:         return muted;
    }
  }

  static Color severityBg(String severity) =>
      severityColor(severity).withValues(alpha: 0.10);

  // Category accents
  static const Color disease       = Color(0xFFD32F2F);
  static const Color diseaseBg     = Color(0xFFFDF0F0);
  static const Color pest          = Color(0xFFE65100);
  static const Color water         = Color(0xFF0277BD);
  static const Color nutrition     = Color(0xFF388E3C);
  static const Color irrigation    = Color(0xFF00838F);
  static const Color environmental = Color(0xFF6A1B9A);
  static const Color other         = Color(0xFF455A64);

  static Color categoryColor(String category) {
    switch (category.toLowerCase()) {
      case 'disease':       return disease;
      case 'pest':          return pest;
      case 'water stress':  return water;
      case 'nutrition':     return nutrition;
      case 'irrigation':    return irrigation;
      case 'environmental': return environmental;
      default:              return other;
    }
  }

  // Nav
  static const Color navActive    = leaf;
  static const Color navInactive  = muted;
  static const Color navIndicator = Color(0x261D9E75); // leaf @ 15%
}
