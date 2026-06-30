import 'package:flutter_test/flutter_test.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:mobile/shared/error/app_error_handler.dart';

void main() {
  group('AppErrorHandler.describe', () {
    test('AuthException returns a friendly auth message', () {
      final error = AuthException('Invalid login credentials');
      final result = AppErrorHandler.describe(error);
      expect(result, 'Authentication issue. Please sign in again.');
    });

    test('PostgrestException with permission code returns permission message', () {
      final error = PostgrestException(message: 'permission denied for table farms', code: '42501');
      final result = AppErrorHandler.describe(error);
      expect(result, contains('permission'));
    });

    test('PostgrestException with permission wording (no code) still detected', () {
      final error = PostgrestException(message: 'insufficient permission to access this resource');
      final result = AppErrorHandler.describe(error);
      expect(result, contains('permission'));
    });

    test('PostgrestException with unrelated error returns generic data message', () {
      final error = PostgrestException(message: 'relation "foo" does not exist', code: '42P01');
      final result = AppErrorHandler.describe(error);
      expect(result, 'Something went wrong loading or saving data. Please try again.');
      // Critically: the raw schema-leaking message must never appear in what the user sees.
      expect(result, isNot(contains('relation')));
      expect(result, isNot(contains('foo')));
    });

    test('TimeoutException returns a connection-related message', () {
      final error = TimeoutException('request timed out');
      final result = AppErrorHandler.describe(error);
      expect(result, contains('longer than expected'));
    });

    test('network/socket errors return offline-friendly message', () {
      final error = Exception('SocketException: Failed host lookup');
      final result = AppErrorHandler.describe(error);
      expect(result, contains('internet connection'));
    });

    test('unknown error type falls back to generic safe message', () {
      final error = Exception('some totally unexpected internal detail');
      final result = AppErrorHandler.describe(error);
      expect(result, 'Something went wrong. Please try again.');
      // The raw exception text must never leak through on the fallback path either.
      expect(result, isNot(contains('totally unexpected internal detail')));
    });

    test('never returns an empty string regardless of input', () {
      final inputs = [
        Exception(''),
        AuthException(''),
        PostgrestException(message: ''),
        'a raw string, not even an Exception',
        42,
      ];
      for (final input in inputs) {
        final result = AppErrorHandler.describe(input);
        expect(result.isNotEmpty, isTrue, reason: 'Failed for input: \$input');
      }
    });
  });
}
