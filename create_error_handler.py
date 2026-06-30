import pathlib

p = pathlib.Path('lib/shared/error/app_error_handler.dart')
p.parent.mkdir(parents=True, exist_ok=True)

content = """import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:postgrest/postgrest.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

/// Centralized error handling: turns raw exceptions into clean,
/// user-facing messages while logging full detail for debugging.
/// This never exposes internal schema/query details to the user.
class AppErrorHandler {
  /// Maps any caught exception to a short, friendly message.
  /// Always logs the real exception via debugPrint for diagnosis.
  static String describe(Object error, {String context = 'operation'}) {
    debugPrint('[error][\$context] \${error.runtimeType}: \$error');

    if (error is AuthException) {
      return 'Authentication issue. Please sign in again.';
    }
    if (error is PostgrestException) {
      // RLS denial surfaces as a Postgrest error with no matching rows/permission.
      if (error.code == '42501' || error.message.toLowerCase().contains('permission')) {
        return 'You don\\'t have permission to do that.';
      }
      return 'Something went wrong loading or saving data. Please try again.';
    }
    if (error is TimeoutException || error.toString().contains('TimeoutException')) {
      return 'This is taking longer than expected. Check your connection and try again.';
    }
    if (error.toString().toLowerCase().contains('socketexception') ||
        error.toString().toLowerCase().contains('network')) {
      return 'No internet connection. Please check your network and try again.';
    }

    // Fallback: generic, never leak raw exception text to the user.
    return 'Something went wrong. Please try again.';
  }

  /// Shows a consistent, branded error snackbar - matches the app's
  /// existing floating/colored snackbar style used throughout.
  static void showError(
    BuildContext context,
    Object error, {
    String context2 = 'operation',
    Color backgroundColor = const Color(0xFFB53030),
  }) {
    final message = describe(error, context: context2);
    if (!context.mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content: Text(message),
      backgroundColor: backgroundColor,
      behavior: SnackBarBehavior.floating,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
    ));
  }
}

class TimeoutException implements Exception {
  final String message;
  TimeoutException(this.message);
  @override
  String toString() => 'TimeoutException: \$message';
}
"""

p.write_text(content, encoding='utf-8')
print(f"Created {p} ({len(content)} chars)")