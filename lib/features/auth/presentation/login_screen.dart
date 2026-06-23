import 'dart:math';
import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import '../../../shared/constants/motivational_messages.dart';
import '../../../shared/widgets/app_shell.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});
  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailCtrl = TextEditingController();
  final _passCtrl  = TextEditingController();
  bool  _obscure   = true;
  bool  _loading   = false;
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

  Future<void> _handleLogin() async {
    final email = _emailCtrl.text.trim();
    final pass  = _passCtrl.text.trim();
    if (email.isEmpty || pass.isEmpty) {
      setState(() => _error = 'Please enter your email and password.');
      return;
    }
    setState(() { _loading = true; _error = null; });
    try {
      final response = await Supabase.instance.client.auth.signInWithPassword(
        email: email, password: pass,
      );
      if (response.user == null) {
        setState(() { _error = 'Login failed. Check your credentials.'; _loading = false; });
        return;
      }
      if (!mounted) return;
      setState(() => _loading = false);
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (_) => const AppShell()),
      );
    } on AuthException catch (e) {
      setState(() { _error = e.message; _loading = false; });
    } catch (_) {
      setState(() { _error = 'An unexpected error occurred.'; _loading = false; });
    }
  }

  @override
  Widget build(BuildContext context) {
    final w = MediaQuery.of(context).size.width;
    final cardWidth = w < 600 ? (w - 48.0).clamp(280.0, 400.0) : 400.0;

    return Scaffold(
      backgroundColor: _bg,
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(vertical: 48),
          child: SizedBox(
            width: cardWidth,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Center(child: Column(children: [
                  Container(
                    width: 96, height: 96,
                    decoration: BoxDecoration(
                      color: _gold.withValues(alpha: 0.15),
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(Icons.local_florist, size: 52, color: _green),
                  ),
                  const SizedBox(height: 16),
                  const Text('Flower Scout', style: TextStyle(
                      fontSize: 30, fontWeight: FontWeight.bold,
                      color: Color(0xFF2C2C2A))),
                  const SizedBox(height: 4),
                  const Text('Kongoni River Farm',
                      style: TextStyle(fontSize: 15, color: Colors.grey)),
                ])),
                const SizedBox(height: 32),
                Container(
                  padding: const EdgeInsets.all(28),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: [BoxShadow(
                        color: Colors.black.withValues(alpha: 0.07),
                        blurRadius: 24, offset: const Offset(0, 8))],
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      const Text('Sign in', style: TextStyle(
                          fontSize: 20, fontWeight: FontWeight.w700,
                          color: Color(0xFF2C2C2A))),
                      const SizedBox(height: 4),
                      const Text('Welcome back to FlowerScout',
                          style: TextStyle(fontSize: 13, color: Colors.grey)),
                      const SizedBox(height: 24),
                      _InputField(controller: _emailCtrl, label: 'Email',
                          icon: Icons.email_outlined,
                          keyboardType: TextInputType.emailAddress),
                      const SizedBox(height: 14),
                      _InputField(
                        controller: _passCtrl, label: 'Password',
                        icon: Icons.lock_outline, obscure: _obscure,
                        suffix: IconButton(
                          icon: Icon(_obscure
                              ? Icons.visibility_off_rounded
                              : Icons.visibility_rounded,
                              size: 18, color: const Color(0xFF888780)),
                          onPressed: () => setState(() => _obscure = !_obscure),
                        ),
                      ),
                      if (_error != null) ...[
                        const SizedBox(height: 12),
                        Container(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 12, vertical: 10),
                          decoration: BoxDecoration(
                            color: const Color(0xFFFEEAEA),
                            borderRadius: BorderRadius.circular(10),
                            border: Border.all(color: const Color(0xFFF7C1C1)),
                          ),
                          child: Text(_error!, style: const TextStyle(
                              fontSize: 13, color: Color(0xFFA32D2D))),
                        ),
                      ],
                      const SizedBox(height: 24),
                      SizedBox(
                        height: 52,
                        child: ElevatedButton.icon(
                          icon: _loading
                              ? const SizedBox(width: 20, height: 20,
                                  child: CircularProgressIndicator(
                                      color: Colors.white, strokeWidth: 2.5))
                              : const Icon(Icons.login),
                          label: Text(_loading ? 'Signing in...' : 'Sign in',
                              style: const TextStyle(
                                  fontSize: 15, fontWeight: FontWeight.w600)),
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
                    ],
                  ),
                ),
                const SizedBox(height: 24),
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: _gold.withValues(alpha: 0.08),
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(
                        color: _gold.withValues(alpha: 0.25), width: 0.8),
                  ),
                  child: Text(_message,
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                        fontSize: 13, color: Color(0xFF5F5E5A),
                        fontStyle: FontStyle.italic, height: 1.5)),
                ),
              ],
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
  final TextInputType keyboardType;
  const _InputField({
    required this.controller, required this.label, required this.icon,
    this.obscure = false, this.suffix,
    this.keyboardType = TextInputType.text,
  });
  @override
  Widget build(BuildContext context) => TextField(
    controller: controller, obscureText: obscure, keyboardType: keyboardType,
    style: const TextStyle(fontSize: 14, color: Color(0xFF2C2C2A)),
    decoration: InputDecoration(
      labelText: label,
      prefixIcon: Icon(icon, color: const Color(0xFF888780)),
      suffixIcon: suffix,
      filled: true, fillColor: const Color(0xFFF9F9F9),
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: Color(0xFFE0E0E0))),
      enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: Color(0xFFE0E0E0))),
      focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: Color(0xFF2E7D32), width: 1.5)),
      contentPadding: const EdgeInsets.symmetric(vertical: 16, horizontal: 12),
    ),
  );
}
