import pathlib

p = pathlib.Path('lib/main.dart')
t = p.read_text(encoding='utf-8')

# Check import
if 'onboarding_screen' in t:
    print("Import: present")
else:
    print("Import: MISSING - adding now")
    t = t.replace(
        "import 'features/auth/presentation/login_screen.dart';",
        "import 'features/auth/presentation/login_screen.dart';\nimport 'features/onboarding/presentation/onboarding_screen.dart';", 1)

# Check initState wiring
if 'hasSeenOnboarding' in t:
    print("initState: present")
else:
    print("initState: MISSING - adding now")
    t = t.replace(
        "_loggedIn = Supabase.instance.client.auth.currentSession != null;",
        "_loggedIn = Supabase.instance.client.auth.currentSession != null;\n    hasSeenOnboarding().then((seen) {\n      if (mounted) setState(() => _seenOnboarding = seen);\n    });", 1)

p.write_text(t, encoding='utf-8')
print("Saved.")