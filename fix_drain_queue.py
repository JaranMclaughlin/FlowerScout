import pathlib, shutil

p = pathlib.Path('lib/main.dart')
shutil.copy(p, p.with_suffix('.dart.bak'))
text = p.read_text(encoding='utf-8')
original = text

# Step 1: Add scouting_screen import for ScoutingScreenState.drainQueue
old_import_anchor = "import 'shared/widgets/app_shell.dart';"
new_import = """import 'shared/widgets/app_shell.dart';
import 'features/scouting/presentation/scouting_screen.dart';"""
if old_import_anchor in text and 'scouting_screen.dart' not in text:
    text = text.replace(old_import_anchor, new_import, 1)
    print("Step 1: added scouting_screen import")
else:
    print("Step 1: import already present or anchor not found")

# Step 2: Add WidgetsBindingObserver mixin to _AuthGateState
old_class = "class _AuthGateState extends ConsumerState<_AuthGate> {"
new_class  = "class _AuthGateState extends ConsumerState<_AuthGate> with WidgetsBindingObserver {"
if old_class in text:
    text = text.replace(old_class, new_class, 1)
    print("Step 2: added WidgetsBindingObserver mixin")
else:
    print("ERROR: _AuthGateState class not found"); raise SystemExit(1)

# Step 3: Register/unregister observer in initState/dispose
old_initstate = """  @override
  void initState() {
    super.initState();
    _loggedIn = Supabase.instance.client.auth.currentSession != null;"""
new_initstate = """  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _loggedIn = Supabase.instance.client.auth.currentSession != null;"""
if old_initstate in text:
    text = text.replace(old_initstate, new_initstate, 1)
    print("Step 3a: registered observer in initState")
else:
    print("ERROR: initState anchor not found"); raise SystemExit(1)

# Step 4: Add dispose method before _loadProfileForCurrentUser
old_load = "  Future<void> _loadProfileForCurrentUser() async {"
new_dispose_plus_load = """  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed && _loggedIn) {
      ScoutingScreenState.drainQueue(context);
    }
  }

  Future<void> _loadProfileForCurrentUser() async {"""
if old_load in text:
    text = text.replace(old_load, new_dispose_plus_load, 1)
    print("Step 4: added dispose + didChangeAppLifecycleState")
else:
    print("ERROR: _loadProfileForCurrentUser anchor not found"); raise SystemExit(1)

# Step 5: Drain queue on successful login (after setState loggedIn = true)
old_login = """        if (!mounted) return;
        setState(() => _loggedIn = true);"""
new_login = """        if (!mounted) return;
        setState(() => _loggedIn = true);
        // Drain any queued reports from when the scout was offline
        ScoutingScreenState.drainQueue(context);"""
if old_login in text:
    text = text.replace(old_login, new_login, 1)
    print("Step 5: drain queue wired to login event")
else:
    print("ERROR: login setState anchor not found"); raise SystemExit(1)

if text != original:
    p.write_text(text, encoding='utf-8')
    print("\nDone. Now wiring the pending badge UI...")
else:
    print("No changes written.")