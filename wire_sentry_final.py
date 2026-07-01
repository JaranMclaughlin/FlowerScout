import pathlib

p = pathlib.Path('lib/shared/error/app_error_handler.dart')
lines = p.read_text(encoding='utf-8').splitlines(keepends=True)

# Sanity checks before touching anything
assert "supabase_flutter" in lines[1], f"Line 1 unexpected: {lines[1]!r}"
assert "describe(Object error, {String context = 'operation'}) {" in lines[9], f"Line 9 unexpected: {lines[9]!r}"
assert "debugPrint" in lines[10], f"Line 10 unexpected: {lines[10]!r}"
assert "Color backgroundColor" in lines[40], f"Line 40 unexpected: {lines[40]!r}"
assert "describe(error, context: context2)" in lines[42], f"Line 42 unexpected: {lines[42]!r}"

# 1. Insert Sentry import after line 1
lines.insert(2, "import 'package:sentry_flutter/sentry_flutter.dart';\n")

# All subsequent line numbers shift by +1 after the insert
# 2. Update describe() signature (was line 9, now line 10)
lines[10] = "  static String describe(Object error, {String context = 'operation', StackTrace? stackTrace}) {\n"

# 3. Insert Sentry capture after debugPrint (was line 10, now line 11)
lines.insert(12, "    Sentry.captureException(error, stackTrace: stackTrace);\n")

# All subsequent line numbers shift by +1 again
# 4. Add StackTrace param to showError() (was line 40, now line 42)
lines[42] = '    Color backgroundColor = const Color(0xFFB53030),\n    StackTrace? stackTrace,\n'

# 5. Pass stackTrace through in describe() call (was line 42, now line 44)
lines[44] = '    final message = describe(error, context: context2, stackTrace: stackTrace);\n'

p.write_text(''.join(lines), encoding='utf-8')
print("Done: Sentry wired into AppErrorHandler via safe line-index replacement.")