import pathlib, shutil

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
shutil.copy(p, p.with_suffix('.dart.bak8'))
text = p.read_text(encoding='utf-8')
original = text

# Fix 1: Add a bytes cache map to _FindingCardState
old_state_fields = """  final _picker = ImagePicker();
  bool _pickingPhoto = false;"""
new_state_fields = """  final _picker = ImagePicker();
  bool _pickingPhoto = false;
  final Map<String, Uint8List> _bytesCache = {}; // prevents FutureBuilder blink"""
if old_state_fields in text:
    text = text.replace(old_state_fields, new_state_fields, 1)
    print("Fix 1: added _bytesCache field")
else:
    print("ERROR: state fields anchor not found"); raise SystemExit(1)

# Fix 2: Cache bytes after picking
old_pick_add = """      if (file != null) {
        setState(() => widget.data.photoFiles.add(file));
        widget.onChanged();
      }"""
new_pick_add = """      if (file != null) {
        final bytes = await file.readAsBytes();
        _bytesCache[file.name] = bytes;
        setState(() => widget.data.photoFiles.add(file));
        widget.onChanged();
      }"""
if old_pick_add in text:
    text = text.replace(old_pick_add, new_pick_add, 1)
    print("Fix 2: bytes cached immediately after pick")
else:
    print("ERROR: pick add anchor not found"); raise SystemExit(1)

# Fix 3: Also clear cache on remove
old_remove = """  void _removePhoto(int index) {
    setState(() => widget.data.photoFiles.removeAt(index));
    widget.onChanged();
  }"""
new_remove = """  void _removePhoto(int index) {
    final file = widget.data.photoFiles[index];
    _bytesCache.remove(file.name);
    setState(() => widget.data.photoFiles.removeAt(index));
    widget.onChanged();
  }"""
if old_remove in text:
    text = text.replace(old_remove, new_remove, 1)
    print("Fix 3: cache cleared on remove")
else:
    print("ERROR: _removePhoto anchor not found"); raise SystemExit(1)

# Fix 4: Replace FutureBuilder with direct cache lookup (no more async on every build)
old_future_builder = """              ClipRRect(
                borderRadius: BorderRadius.circular(8),
                child: FutureBuilder<Uint8List>(
                  future: photos[i].readAsBytes(),
                  builder: (context, snap) {
                    if (!snap.hasData) return Container(
                      width: 80, height: 80,
                      decoration: BoxDecoration(
                        color: const Color(0xFFEAEFEA),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: const Icon(Icons.image_rounded, color: Color(0xFF6B7F6E)),
                    );
                    return Image.memory(snap.data!,
                        width: 80, height: 80, fit: BoxFit.cover);
                  },
                ),
              ),"""
new_future_builder = """              ClipRRect(
                borderRadius: BorderRadius.circular(8),
                child: Builder(builder: (context) {
                  final bytes = _bytesCache[photos[i].name];
                  if (bytes == null) return Container(
                    width: 80, height: 80,
                    decoration: BoxDecoration(
                      color: const Color(0xFFEAEFEA),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Icon(Icons.image_rounded, color: Color(0xFF6B7F6E)),
                  );
                  return Image.memory(bytes,
                      width: 80, height: 80, fit: BoxFit.cover);
                }),
              ),"""
if old_future_builder in text:
    text = text.replace(old_future_builder, new_future_builder, 1)
    print("Fix 4: replaced FutureBuilder with cache lookup - no more blinking")
else:
    print("ERROR: FutureBuilder anchor not found"); raise SystemExit(1)

# Fix 5: Enable camera on web - remove kIsWeb guards
# Browser supports camera via image_picker_for_web
old_camera_guard = """          // Camera button - not available on web
          if (!kIsWeb)
            GestureDetector(
              onTap: () => _pickPhoto(ImageSource.camera),
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                decoration: BoxDecoration(
                  color: const Color(0xFF2D6A4F).withValues(alpha: 0.08),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: const Color(0xFF2D6A4F).withValues(alpha: 0.2)),
                ),
                child: Row(mainAxisSize: MainAxisSize.min, children: [
                  const Icon(Icons.camera_alt_rounded, size: 14, color: Color(0xFF2D6A4F)),
                  const SizedBox(width: 4),
                  const Text('Camera', style: TextStyle(fontSize: 11,
                      color: Color(0xFF2D6A4F), fontWeight: FontWeight.w600)),
                ]),
              ),
            ),
          if (!kIsWeb) const SizedBox(width: 8),"""
new_camera_guard = """          GestureDetector(
              onTap: () => _pickPhoto(ImageSource.camera),
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                decoration: BoxDecoration(
                  color: const Color(0xFF2D6A4F).withValues(alpha: 0.08),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: const Color(0xFF2D6A4F).withValues(alpha: 0.2)),
                ),
                child: Row(mainAxisSize: MainAxisSize.min, children: [
                  const Icon(Icons.camera_alt_rounded, size: 14, color: Color(0xFF2D6A4F)),
                  const SizedBox(width: 4),
                  const Text('Camera', style: TextStyle(fontSize: 11,
                      color: Color(0xFF2D6A4F), fontWeight: FontWeight.w600)),
                ]),
              ),
            ),
          const SizedBox(width: 8),"""
if old_camera_guard in text:
    text = text.replace(old_camera_guard, new_camera_guard, 1)
    print("Fix 5: camera enabled on web (browser handles it natively)")
else:
    print("ERROR: camera guard anchor not found"); raise SystemExit(1)

if text != original:
    p.write_text(text, encoding='utf-8')
    print("\nDone.")
else:
    print("\nNo changes written.")