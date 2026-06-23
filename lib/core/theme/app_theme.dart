import 'package:flutter/material.dart';
import '../../shared/theme/app_colors.dart';

class AppTheme {
  static ThemeData lightTheme = ThemeData(
    useMaterial3: true,
    colorSchemeSeed: Colors.green,
    scaffoldBackgroundColor: const Color(0xFFF8FAF8),

    appBarTheme: const AppBarTheme(
      centerTitle: false,
      elevation: 0,
    ),

    inputDecorationTheme: const InputDecorationTheme(
      border: OutlineInputBorder(),
    ),

    // ── Additive: card + divider defaults for the redesign ──────────────────
    cardTheme: CardThemeData(
      color: AppColors.surface,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppSizes.radiusLg),
        side: const BorderSide(color: AppColors.divider, width: 0.5),
      ),
      margin: EdgeInsets.zero,
    ),
    dividerTheme: const DividerThemeData(
      color: AppColors.divider,
      thickness: 0.5,
      space: 0.5,
    ),
  );
}

/// ── Responsive sizing helpers ────────────────────────────────────────────────
/// New, additive utility class — does not replace anything existing.
/// Use these in new/refactored screens for consistent, smaller, responsive sizing.
class AppSizes {
  AppSizes._();

  // Border radius
  static const double radiusSm = 8;
  static const double radiusMd = 12;
  static const double radiusLg = 16;
  static const double radiusXl = 20;
  static const double radiusPill = 50;

  // Spacing
  static const double spaceXs  = 4;
  static const double spaceSm  = 8;
  static const double spaceMd  = 12;
  static const double spaceLg  = 16;
  static const double spaceXl  = 20;
  static const double space2xl = 24;
  static const double space3xl = 32;

  // Icon sizes
  static const double iconSm = 16;
  static const double iconMd = 20;
  static const double iconLg = 24;

  // Card padding
  static const EdgeInsets cardPadding   = EdgeInsets.all(14);
  static const EdgeInsets cardPaddingLg = EdgeInsets.all(18);

  // Breakpoints
  static const double tabletMin  = 600;
  static const double desktopMin = 900;

  static bool isPhone(BuildContext ctx) =>
      MediaQuery.of(ctx).size.shortestSide < tabletMin;
  static bool isTablet(BuildContext ctx) =>
      MediaQuery.of(ctx).size.shortestSide >= tabletMin &&
      MediaQuery.of(ctx).size.width < desktopMin;
  static bool isDesktop(BuildContext ctx) =>
      MediaQuery.of(ctx).size.width >= desktopMin;

  /// Horizontal page padding — tighter on phone, roomier on tablet/web
  static double pagePadding(BuildContext ctx) =>
      isPhone(ctx) ? 16 : isTablet(ctx) ? 20 : 28;

  /// Max content width for web/large tablet — keeps cards from stretching too wide
  static const double maxContentWidth = 1100;
}

/// ── Shared text styles (additive) ────────────────────────────────────────────
class AppTextStyles {
  AppTextStyles._();

  static const TextStyle displayLarge = TextStyle(
    fontSize: 24, fontWeight: FontWeight.w700,
    color: AppColors.ink, letterSpacing: -0.5, height: 1.2,
  );
  static const TextStyle heading = TextStyle(
    fontSize: 17, fontWeight: FontWeight.w600, color: AppColors.ink,
  );
  static const TextStyle title = TextStyle(
    fontSize: 14, fontWeight: FontWeight.w600, color: AppColors.ink,
  );
  static const TextStyle body = TextStyle(
    fontSize: 13, color: AppColors.graphite, height: 1.5,
  );
  static const TextStyle caption = TextStyle(
    fontSize: 11, color: AppColors.slate,
  );
  static const TextStyle label = TextStyle(
    fontSize: 11, fontWeight: FontWeight.w600,
    color: AppColors.slate, letterSpacing: 0.8,
  );
}
