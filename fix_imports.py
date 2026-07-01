import pathlib

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
text = p.read_text(encoding='utf-8')

text = text.replace("import '../../auth/presentation/login_screen.dart';\n", "")
text = text.replace("import 'package:supabase_flutter/supabase_flutter.dart';\n", "")

p.write_text(text, encoding='utf-8')
print("settings_screen.dart: unused imports removed.")