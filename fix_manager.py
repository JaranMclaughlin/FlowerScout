import pathlib

p = pathlib.Path('lib/shared/providers/farm_providers.dart')
txt = p.read_text(encoding='utf-8')

if 'isManagerProvider' not in txt:
    addition = """
// -- Role helpers ---------------------------------------------------------

final isManagerProvider = Provider<bool>((ref) {
  ref.watch(authStateProvider); // rebuild on auth change
  final profile = UserSession.currentProfile;
  return profile == UserProfile.manager || profile == UserProfile.systemAdmin;
});
"""
    # Add after the last import line
    lines = txt.splitlines()
    last_import = max(i for i, l in enumerate(lines) if l.startswith('import '))
    lines.insert(last_import + 1, "import '../../../core/session/user_session.dart';")
    txt = '\n'.join(lines) + addition
    p.write_text(txt, encoding='utf-8')
    print('Added isManagerProvider to farm_providers.dart')
else:
    print('Already present')