import pathlib, shutil

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
shutil.copy(p, p.with_suffix('.dart.bak3'))
text = p.read_text(encoding='utf-8')
original = text

# Fix 1: build() - capture s once and pass to layout methods
old_build = """  @override
  Widget build(BuildContext context) {
    // Populate profile fields once loaded
    final profileAsync = ref.watch(profileProvider);
    profileAsync.whenData((profile) {
      if (profile != null && !_profileLoaded) {
        _nameCtrl.text  = profile.fullName;
        _emailCtrl.text = ref.read(supabaseClientProvider).auth.currentUser?.email ?? '';
        _phoneCtrl.text = profile.phone ?? '';
        _profileLoaded  = true;
      }
    });

    return Scaffold(
      backgroundColor: _C.cream,
      body: SafeArea(
        child: LayoutBuilder(builder: (context, constraints) {
          final isWide = constraints.maxWidth >= 900;
          return isWide ? _wideLayout() : _narrowLayout();
        }),
      ),
    );
  }"""

new_build = """  @override
  Widget build(BuildContext context) {
    final s = this.s; // capture once inside build so ref.watch is legal
    // Populate profile fields once loaded
    final profileAsync = ref.watch(profileProvider);
    profileAsync.whenData((profile) {
      if (profile != null && !_profileLoaded) {
        _nameCtrl.text  = profile.fullName;
        _emailCtrl.text = ref.read(supabaseClientProvider).auth.currentUser?.email ?? '';
        _phoneCtrl.text = profile.phone ?? '';
        _profileLoaded  = true;
      }
    });

    return Scaffold(
      backgroundColor: _C.cream,
      body: SafeArea(
        child: LayoutBuilder(builder: (context, constraints) {
          final isWide = constraints.maxWidth >= 900;
          return isWide ? _wideLayout(s) : _narrowLayout(s);
        }),
      ),
    );
  }"""

if old_build in text:
    text = text.replace(old_build, new_build, 1)
    print("Fix 1 applied: s captured in build(), passed to layout methods")
else:
    print("ERROR: build() anchor not found - aborting")
    raise SystemExit(1)

# Fix 2: _wideLayout() signature
old_wide_sig = "  Widget _wideLayout() => Row(children: ["
new_wide_sig = "  Widget _wideLayout(AppStrings s) => Row(children: ["
if old_wide_sig in text:
    text = text.replace(old_wide_sig, new_wide_sig, 1)
    print("Fix 2 applied: _wideLayout now accepts s")
else:
    print("WARNING: _wideLayout() signature not found")

# Fix 3: _narrowLayout() signature
old_narrow_sig = "  Widget _narrowLayout() =>"
new_narrow_sig = "  Widget _narrowLayout(AppStrings s) =>"
if old_narrow_sig in text:
    text = text.replace(old_narrow_sig, new_narrow_sig, 1)
    print("Fix 3 applied: _narrowLayout now accepts s")
else:
    # Try alternate form
    old_narrow_sig2 = "  Widget _narrowLayout() {"
    new_narrow_sig2 = "  Widget _narrowLayout(AppStrings s) {"
    if old_narrow_sig2 in text:
        text = text.replace(old_narrow_sig2, new_narrow_sig2, 1)
        print("Fix 3 applied (alt): _narrowLayout now accepts s")
    else:
        print("WARNING: _narrowLayout() signature not found - check manually")

if text != original:
    p.write_text(text, encoding='utf-8')
    print("\nDone. Now run:")
    print("  flutter analyze lib\\features\\settings\\presentation\\settings_screen.dart")
    print("  flutter run -d chrome --web-port=8080")
else:
    print("\nNo changes written.")