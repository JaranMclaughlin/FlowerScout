import pathlib

p = pathlib.Path('lib/shared/error/app_error_handler.dart')
text = p.read_text(encoding='utf-8')

old = """import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
/// Centralized error handling: turns raw exceptions into clean,
/// user-facing messages while logging full detail for debugging.
/// This never exposes internal schema/query details to the user.
class AppErrorHandler {
  /// Maps any caught exception to a short, friendly message.
  /// Always logs the real exception via debugPrint for diagnosis.
  static String describe(Object error, {String context = 'operation'}) {
    debugPrint('[error][$context] ${error.runtimeType}: $error');
    if (error is AuthException) {"""

new = """import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:sentry_flutter/sentry_flutter.dart';
/// Centralized error handling: turns raw exceptions into clean,
/// user-facing messages while logging full detail for debugging.
/// This never exposes internal schema/query details to the user.
class AppErrorHandler {
  /// Maps any caught exception to a short, friendly message.
  /// Always logs the real exception via debugPrint, and reports it
  /// to Sentry for production diagnosis, while the return value stays
  /// safe to show directly to the user.
  static String describe(Object error, {String context = 'operation', StackTrace? stackTrace}) {
    debugPrint('[error][$context] ${error.runtimeType}: $error');
    Sentry.captureException(error, stackTrace: stackTrace, hint: Hint.withMap({'context': context}));
    if (error is AuthException) {"""

if old not in text:
    raise SystemExit("Anchor 1 not found - aborting, no changes made.")
text = text.replace(old, new, 1)

old2 = """  static void showError(
    BuildContext context,
    Object error, {
    String context2 = 'operation',
    Color backgroundColor = const Color(0xFFB53030),
  }) {
    final message = describe(error, context: context2);"""

new2 = """  static void showError(
    BuildContext context,
    Object error, {
    String context2 = 'operation',
    Color backgroundColor = const Color(0xFFB53030),
    StackTrace? stackTrace,
  }) {
    final message = describe(error, context: context2, stackTrace: stackTrace);"""

if old2 not in text:
    raise SystemExit("Anchor 2 not found - aborting, no changes made.")
text = text.replace(old2, new2, 1)

p.write_text(text, encoding='utf-8')
print("app_error_handler.dart updated: errors now reported to Sentry with optional stack trace, in addition to local debugPrint logging.")