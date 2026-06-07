import 'package:flutter/material.dart';

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
  );
}