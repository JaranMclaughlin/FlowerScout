import pathlib

p = pathlib.Path('lib/main.dart')
t = p.read_text(encoding='utf-8')

t = t.replace(
    "[startup] dotenv loaded at \${sw.elapsedMilliseconds}ms",
    "[startup] dotenv loaded")
t = t.replace(
    "[startup] Supabase initialized at \${sw.elapsedMilliseconds}ms",
    "[startup] Supabase initialized")
t = t.replace(
    "[startup] locale ready at \${sw.elapsedMilliseconds}ms",
    "[startup] locale ready")
t = t.replace(
    "[startup] init failed after \${sw.elapsedMilliseconds}ms: \$e",
    "[startup] init failed: \$e")

p.write_text(t, encoding='utf-8')
print("Fixed: startup log strings cleaned")