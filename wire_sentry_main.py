import pathlib

p = pathlib.Path('lib/main.dart')
text = p.read_text(encoding='utf-8')

# 1. Add the Sentry import
old_imports = "import 'package:supabase_flutter/supabase_flutter.dart';"
new_imports = old_imports + "\nimport 'package:sentry_flutter/sentry_flutter.dart';"
if old_imports not in text:
    raise SystemExit("Imports anchor not found - aborting, no changes made.")
text = text.replace(old_imports, new_imports, 1)

# 2. Wrap runApp() with SentryFlutter.init() in main()
old_main = """void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const _Bootstrap());
}"""
new_main = """Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Load just enough of .env early to get the Sentry DSN before full
  // startup begins, so crashes during _Bootstrap's own init are also captured.
  await dotenv.load(fileName: '.env');
  final sentryDsn = dotenv.env['SENTRY_DSN'];

  await SentryFlutter.init(
    (options) {
      options.dsn = sentryDsn;
      options.tracesSampleRate = 0.2;
      options.environment = kDebugMode ? 'debug' : 'production';
      // Don't double-report: AppErrorHandler already logs locally via debugPrint;
      // Sentry capture is wired in there explicitly, not via global error hooks,
      // to avoid duplicate/noisy reports for errors we already handle gracefully.
    },
    appRunner: () => runApp(const _Bootstrap()),
  );
}"""
if old_main not in text:
    raise SystemExit("main() anchor not found - aborting, no changes made.")
text = text.replace(old_main, new_main, 1)

# 3. Fix the pre-existing escaped-dollar bug in the startup failure log
old_log = "      debugPrint('[startup] init failed: \\$e');"
new_log = "      debugPrint('[startup] init failed: $e');"
if old_log not in text:
    raise SystemExit("Startup log anchor not found - aborting, no changes made.")
text = text.replace(old_log, new_log, 1)

p.write_text(text, encoding='utf-8')
print("main.dart updated: Sentry initialized, wraps runApp(); fixed startup log interpolation bug.")