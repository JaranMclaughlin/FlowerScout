import pathlib

p = pathlib.Path('lib/features/auth/presentation/location_permission_screen.dart')
text = p.read_text(encoding='utf-8')

old = """  @override
  State<LocationPermissionScreen> createState() =>
      _LocationPermissionScreenState();"""
new = """  @override
  ConsumerState<LocationPermissionScreen> createState() =>
      _LocationPermissionScreenState();"""
if old not in text:
    raise SystemExit("Anchor not found - aborting.")
text = text.replace(old, new, 1)
p.write_text(text, encoding='utf-8')
print("Fixed createState() return type.")