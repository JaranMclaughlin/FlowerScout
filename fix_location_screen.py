import pathlib

p = pathlib.Path('lib/features/auth/presentation/location_permission_screen.dart')
text = p.read_text(encoding='utf-8')

old_class = """class _LocationPermissionScreenState
    extends State<LocationPermissionScreen> {
  bool _checking = false;"""
new_class = """class _LocationPermissionScreenState
    extends ConsumerState<LocationPermissionScreen> {
  bool _checking = false;

  AppStrings get s => AppStrings.of(ref.watch(localeProvider));"""
if old_class not in text:
    raise SystemExit("Class anchor not found - aborting.")
text = text.replace(old_class, new_class, 1)

old_build = """  Widget build(BuildContext context) {
    final s = AppStrings.of(ref.watch(localeProvider));
    final isTablet = MediaQuery.of(context).size.shortestSide >= 600;"""
new_build = """  Widget build(BuildContext context) {
    final isTablet = MediaQuery.of(context).size.shortestSide >= 600;"""
if old_build not in text:
    raise SystemExit("build() anchor not found - aborting.")
text = text.replace(old_build, new_build, 1)

old_dialog = """        title: const Text(s.locationBlocked,
            style: TextStyle(
                fontSize: 16, fontWeight: FontWeight.w600)),"""
new_dialog = """        title: Text(s.locationBlocked,
            style: const TextStyle(
                fontSize: 16, fontWeight: FontWeight.w600)),"""
if old_dialog not in text:
    raise SystemExit("Dialog title anchor not found - aborting.")
text = text.replace(old_dialog, new_dialog, 1)

old_btn1 = """            child: const Text(s.continueAnyway,
                style: TextStyle(color: Color(0xFF888780))),"""
new_btn1 = """            child: Text(s.continueAnyway,
                style: const TextStyle(color: Color(0xFF888780))),"""
if old_btn1 not in text:
    raise SystemExit("continueAnyway anchor not found - aborting.")
text = text.replace(old_btn1, new_btn1, 1)

old_btn2 = """            child: const Text(s.openAppSettings,
                style: TextStyle(color: Color(0xFF1D9E75))),"""
new_btn2 = """            child: Text(s.openAppSettings,
                style: const TextStyle(color: Color(0xFF1D9E75))),"""
if old_btn2 not in text:
    raise SystemExit("openAppSettings anchor not found - aborting.")
text = text.replace(old_btn2, new_btn2, 1)

p.write_text(text, encoding='utf-8')
print("location_permission_screen.dart fixed: ConsumerState, AppStrings getter, removed invalid const.")