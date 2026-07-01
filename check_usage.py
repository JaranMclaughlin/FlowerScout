import pathlib
p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
text = p.read_text(encoding='utf-8')
print("Supabase usages:", text.count('Supabase.'))
print("LoginScreen usages:", text.count('LoginScreen'))