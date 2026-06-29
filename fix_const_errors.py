import pathlib

# Fix maps - remove const where s is used
p = pathlib.Path('lib/features/maps/presentation/maps_screen.dart')
txt = p.read_text(encoding='utf-8')
txt = txt.replace('const Center(child: Text(s.couldNotLoadLive, style: TextStyle(color: _muted)))', 'Center(child: Text(s.couldNotLoadLive, style: const TextStyle(color: _muted)))')
txt = txt.replace('const Center(child: Text(s.couldNotLoadTrail, style: TextStyle(color: _muted)))', 'Center(child: Text(s.couldNotLoadTrail, style: const TextStyle(color: _muted)))')
txt = txt.replace('                Text(s.noScoutsOut,', '                Text(s.noScoutsOut,')
p.write_text(txt, encoding='utf-8')
print('maps done')

# Fix settings - remove const where s is used
p2 = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
txt2 = p2.read_text(encoding='utf-8')
txt2 = txt2.replace('const _LoadingCard(message: s.loadingFarms)', '_LoadingCard(message: s.loadingFarms)')
txt2 = txt2.replace('const _EmptyCard(message: s.noFarmsAssigned)', '_EmptyCard(message: s.noFarmsAssigned)')
txt2 = txt2.replace('const _LoadingCard(message: s.loadingProfile)', '_LoadingCard(message: s.loadingProfile)')
txt2 = txt2.replace('const _LoadingCard(message: s.loadingTeam)', '_LoadingCard(message: s.loadingTeam)')
txt2 = txt2.replace('const _EmptyCard(message: s.noTeamMembers)', '_EmptyCard(message: s.noTeamMembers)')
txt2 = txt2.replace('const Text(s.signOutQ, style: TextStyle(', 'Text(s.signOutQ, style: const TextStyle(')
txt2 = txt2.replace('const Text(s.signOutLabel,', 'Text(s.signOutLabel,')
txt2 = txt2.replace('String _theme      = s.systemDefault;', "String _theme      = 'System default';")
p2.write_text(txt2, encoding='utf-8')
print('settings done')