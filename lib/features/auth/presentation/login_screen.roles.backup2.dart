import 'dart:math';
import 'package:flutter/material.dart';
import '../../../shared/constants/motivational_messages.dart';
import '../../../shared/widgets/app_shell.dart';
import 'location_permission_screen.dart';
import '../../../core/session/user_session.dart';

enum LoginRole {
  scout,
  manager,
  systemAdmin,
}

enum ManagerType {
  productionManager,
  sprayCoordinator,
  regionalManager,
  system,
}

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});
  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailCtrl = TextEditingController();
  final _passCtrl  = TextEditingController();
  LoginRole _role = LoginRole.scout;
ManagerType? _managerType;
  bool _obscure    = true;
  bool _loading    = false;
  String? _error;

  final String _message =
      motivationalMessages[Random().nextInt(motivationalMessages.length)];

  static const _green = Color(0xFF2E7D32);
  static const _gold  = Color(0xFFD4AF37);
  static const _bg    = Color(0xFFF5F4EF);

  @override
  void dispose() {
    _emailCtrl.dispose();
    _passCtrl.dispose();
    super.dispose();
  }

  void _goToApp() {
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(builder: (_) => const AppShell()),
    );
  }

  Future<void> _handleLogin() async {
    final email = _emailCtrl.text.trim();
    final pass  = _passCtrl.text;

    if (email.isEmpty || pass.isEmpty) {
      setState(() => _error = 'Please enter your username and password.');
      return;
    }

    setState(() { _loading = true; _error = null; });
    await Future.delayed(const Duration(milliseconds: 900));
    if (!mounted) return;
    setState(() => _loading = false);

    if (_role == ScoutRole.scout) {
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (_) => LocationPermissionScreen(scoutName: email.split('@').first)),
      );
    } else {
      _goToApp();
    }
  }

  @override
  Widget build(BuildContext context) {
    final isTablet = MediaQuery.of(context).size.shortestSide >= 600;
    final maxWidth = isTablet ? 480.0 : double.infinity;

    return Scaffold(
      backgroundColor: _bg,
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: EdgeInsets.symmetric(
              horizontal: isTablet ? 0 : 24,
              vertical: 32,
            ),
            child: ConstrainedBox(
              constraints: BoxConstraints(maxWidth: maxWidth),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [

                  // Logo
                  Center(
                    child: Column(children: [
                      Container(
                        padding: const EdgeInsets.all(20),
                        decoration: BoxDecoration(
                          color: _gold.withValues(alpha: 0.15),
                          shape: BoxShape.circle,
                        ),
                        child: Icon(Icons.local_florist,
                            size: isTablet ? 90 : 72,
                            color: _green),
                      ),
                      SizedBox(height: isTablet ? 20 : 16),
                      Text('Flower Scout',
                          style: TextStyle(
                            fontSize: isTablet ? 40 : 34,
                            fontWeight: FontWeight.bold,
                            color: const Color(0xFF2C2C2A),
                          )),
                      const SizedBox(height: 6),
                      Text('Kongoni River Farm',
                          style: TextStyle(
                            fontSize: isTablet ? 18 : 16,
                            color: Colors.grey,
                          )),
                    ]),
                  ),

                  SizedBox(height: isTablet ? 40 : 32),

                  // Role selector
                  Text('Sign in as',
                      style: TextStyle(
                        fontSize: isTablet ? 13 : 12,
                        color: const Color(0xFF888780),
                        fontWeight: FontWeight.w500,
                      )),
                  const SizedBox(height: 8),
                  Row(children: [
                    Expanded(child: _RoleChip(
                      label: 'Scout',
                      icon: Icons.person_rounded,
                      selected: _role == ScoutRole.scout,
                      onTap: () => setState(() => _role = ScoutRole.scout),
                      isTablet: isTablet,
                    )),
                    const SizedBox(width: 10),
                    Expanded(child: _RoleChip(
                      label: 'Manager',
                      icon: Icons.shield_rounded,
                      selected: _role == ScoutRole.manager,
                      onTap: () => setState(() => _role = ScoutRole.manager),
                      isTablet: isTablet,
                    )),
                  ]),

                  SizedBox(height: isTablet ? 24 : 20),

                  // Username
                  _InputField(
                    controller: _emailCtrl,
                    label: 'Username',
                    icon: Icons.person_outline,
                    isTablet: isTablet,
                  ),

                  SizedBox(height: isTablet ? 16 : 14),

                  // Password
                  _InputField(
                    controller: _passCtrl,
                    label: 'Password',
                    icon: Icons.lock_outline,
                    obscure: _obscure,
                    isTablet: isTablet,
                    suffix: IconButton(
                      icon: Icon(
                        _obscure
                            ? Icons.visibility_off_rounded
                            : Icons.visibility_rounded,
                        size: 18,
                        color: const Color(0xFF888780),
                      ),
                      onPressed: () =>
                          setState(() => _obscure = !_obscure),
                    ),
                  ),

                  // Error
                  if (_error != null) ...[
                    const SizedBox(height: 10),
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 12, vertical: 8),
                      decoration: BoxDecoration(
                        color: const Color(0xFFFEEAEA),
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(
                            color: const Color(0xFFF7C1C1)),
                      ),
                      child: Text(_error!,
                          style: TextStyle(
                              fontSize: isTablet ? 13 : 12,
                              color: const Color(0xFFA32D2D))),
                    ),
                  ],

                  SizedBox(height: isTablet ? 28 : 24),

                  // Login button
                  SizedBox(
                    width: double.infinity,
                    height: isTablet ? 58 : 52,
                    child: ElevatedButton.icon(
                      icon: _loading
                          ? const SizedBox(
                              width: 20, height: 20,
                              child: CircularProgressIndicator(
                                  color: Colors.white,
                                  strokeWidth: 2.5))
                          : const Icon(Icons.login),
                      label: Text(
                        _loading ? 'Signing in...' : 'Login',
                        style: TextStyle(
                            fontSize: isTablet ? 17 : 15,
                            fontWeight: FontWeight.w600),
                      ),
                      onPressed: _loading ? null : _handleLogin,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: _green,
                        foregroundColor: Colors.white,
                        elevation: 0,
                        shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12)),
                      ),
                    ),
                  ),

                  // Motivational message
                  SizedBox(height: isTablet ? 36 : 28),
                  Container(
                    padding: EdgeInsets.all(isTablet ? 20 : 16),
                    decoration: BoxDecoration(
                      color: _gold.withValues(alpha: 0.08),
                      borderRadius: BorderRadius.circular(14),
                      border: Border.all(
                          color: _gold.withValues(alpha: 0.25),
                          width: 0.8),
                    ),
                    child: Text(
                      _message,
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: isTablet ? 15 : 13,
                        color: const Color(0xFF5F5E5A),
                        fontStyle: FontStyle.italic,
                        height: 1.5,
                      ),
                    ),
                  ),

                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _InputField extends StatelessWidget {
  final TextEditingController controller;
  final String label;
  final IconData icon;
  final bool obscure;
  final Widget? suffix;
  final bool isTablet;

  const _InputField({
    required this.controller,
    required this.label,
    required this.icon,
    required this.isTablet,
    this.obscure = false,
    this.suffix,
  });

  @override
  Widget build(BuildContext context) => TextField(
    controller: controller,
    obscureText: obscure,
    style: TextStyle(
        fontSize: isTablet ? 15 : 14,
        color: const Color(0xFF2C2C2A)),
    decoration: InputDecoration(
      labelText: label,
      prefixIcon: Icon(icon, color: const Color(0xFF888780)),
      suffixIcon: suffix,
      border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12)),
      contentPadding: EdgeInsets.symmetric(
          vertical: isTablet ? 18 : 14, horizontal: 12),
    ),
  );
}

class _RoleChip extends StatelessWidget {
  final String label;
  final IconData icon;
  final bool selected;
  final VoidCallback onTap;
  final bool isTablet;

  const _RoleChip({
    required this.label,
    required this.icon,
    required this.selected,
    required this.onTap,
    required this.isTablet,
  });

  @override
  Widget build(BuildContext context) => GestureDetector(
    onTap: onTap,
    child: AnimatedContainer(
      duration: const Duration(milliseconds: 180),
      padding: EdgeInsets.symmetric(
          vertical: isTablet ? 14 : 11),
      decoration: BoxDecoration(
        color: selected
            ? const Color(0xFF2E7D32).withValues(alpha: 0.08)
            : Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: selected
              ? const Color(0xFF2E7D32)
              : const Color(0xFFD3D1C7),
          width: selected ? 1.5 : 0.5,
        ),
      ),
      child: Column(children: [
        Icon(icon,
            color: selected
                ? const Color(0xFF2E7D32)
                : const Color(0xFF888780),
            size: isTablet ? 24 : 20),
        const SizedBox(height: 4),
        Text(label,
            style: TextStyle(
                fontSize: isTablet ? 13 : 11,
                fontWeight: FontWeight.w500,
                color: selected
                    ? const Color(0xFF2E7D32)
                    : const Color(0xFF888780))),
      ]),
    ),
  );
}




//test

