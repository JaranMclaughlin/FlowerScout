import 'package:flutter/material.dart';

import 'core/theme/app_theme.dart';
import 'features/auth/presentation/login_screen.dart';

void main() {
  runApp(const FlowerScoutApp());
}

class FlowerScoutApp extends StatelessWidget {
  const FlowerScoutApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Flower Scout',
      theme: AppTheme.lightTheme,
      home: LoginScreen(),
    );
  }
}