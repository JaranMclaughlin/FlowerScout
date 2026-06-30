import pathlib

p = pathlib.Path('lib/main.dart')
text = p.read_text(encoding='utf-8')
text = text.replace(
    "        publishableKey: dotenv.env['SUPABASE_ANON_KEY']!,",
    "        anonKey: dotenv.env['SUPABASE_ANON_KEY']!,"
)
p.write_text(text, encoding='utf-8')
print("main.dart: anonKey restored.")