import pathlib, shutil

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
shutil.copy(p, p.with_suffix('.dart.bak2'))
text = p.read_text(encoding='utf-8')
original = text

# Step 1: Add _queueCount state field near _submitting/_submitted fields
old_fields = """  // Duplicate submit guard
  bool _submitting = false;
  bool _submitted  = false;"""
new_fields = """  // Duplicate submit guard
  bool _submitting = false;
  bool _submitted  = false;
  int  _queueCount = 0; // offline queue badge"""
if old_fields in text:
    text = text.replace(old_fields, new_fields, 1)
    print("Step 1: added _queueCount field")
else:
    print("ERROR: fields anchor not found"); raise SystemExit(1)

# Step 2: Load queue count in initState (find initState opening)
old_initstate = """  @override
  void initState() {
    super.initState();"""
new_initstate = """  @override
  void initState() {
    super.initState();
    _refreshQueueCount();"""
if old_initstate in text:
    text = text.replace(old_initstate, new_initstate, 1)
    print("Step 2: wired _refreshQueueCount to initState")
else:
    print("ERROR: initState not found"); raise SystemExit(1)

# Step 3: Add _refreshQueueCount helper before the queue helpers block
old_queue_anchor = "  // ── Offline queue helpers ─────────────────────────────────────────────────"
new_queue_anchor = """  // ── Queue badge ──────────────────────────────────────────────────────────────
  Future<void> _refreshQueueCount() async {
    final count = await ScoutingScreenState.queueLength();
    if (mounted) setState(() => _queueCount = count);
  }

  // ── Offline queue helpers ─────────────────────────────────────────────────"""
if old_queue_anchor in text:
    text = text.replace(old_queue_anchor, new_queue_anchor, 1)
    print("Step 3: added _refreshQueueCount helper")
else:
    print("ERROR: queue helpers anchor not found"); raise SystemExit(1)

# Step 4: After successful queue save, refresh the badge count
old_after_queue_save = """          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            backgroundColor: const Color(0xFFBA7517),
            behavior: SnackBarBehavior.floating,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            content: Row(children: [
              const Icon(Icons.cloud_off_rounded, color: Colors.white),
              const SizedBox(width: 10),
              const Expanded(child: Text('No connection — report saved locally and will sync when online',
                  style: TextStyle(color: Colors.white))),
            ]),
          ));"""
new_after_queue_save = """          _refreshQueueCount(); // update badge
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            backgroundColor: const Color(0xFFBA7517),
            behavior: SnackBarBehavior.floating,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            content: Row(children: [
              const Icon(Icons.cloud_off_rounded, color: Colors.white),
              const SizedBox(width: 10),
              const Expanded(child: Text('No connection — report saved locally and will sync when online',
                  style: TextStyle(color: Colors.white))),
            ]),
          ));"""
if old_after_queue_save in text:
    text = text.replace(old_after_queue_save, new_after_queue_save, 1)
    print("Step 4: badge refresh wired after queue save")
else:
    print("ERROR: snackbar anchor not found"); raise SystemExit(1)

# Step 5: Replace _buildSubmitButton to show amber badge when queue > 0
old_submit_btn = """  Widget _buildSubmitButton(AppStrings s) => SizedBox("""
new_submit_btn = """  Widget _buildSubmitButton(AppStrings s) => Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      if (_queueCount > 0)
        Padding(
          padding: const EdgeInsets.only(bottom: 8),
          child: Row(children: [
            const Icon(Icons.cloud_off_rounded, size: 14, color: Color(0xFFBA7517)),
            const SizedBox(width: 6),
            Text(
              '$_queueCount report${_queueCount > 1 ? "s" : ""} queued — will sync when online',
              style: const TextStyle(fontSize: 12, color: Color(0xFFBA7517),
                  fontWeight: FontWeight.w500),
            ),
          ]),
        ),
      SizedBox("""
if old_submit_btn in text:
    text = text.replace(old_submit_btn, new_submit_btn, 1)
    print("Step 5: added queue badge above submit button")
else:
    print("ERROR: _buildSubmitButton anchor not found"); raise SystemExit(1)

# Step 6: Close the extra Column wrapping the SizedBox
# Find the closing of _buildSubmitButton and add the Column closing bracket
# The method ends after the SizedBox closes - we need to add ]);
# Find onPressed line to locate the end of the button widget
old_btn_end = """      onPressed: (_submitting || _submitted) ? null : _submitReport,"""
# We need to find the method's last line - look for the semicolon after the SizedBox
# The SizedBox is now inside a Column, so we close Column after SizedBox
# Find the pattern: the SizedBox widget closing before next method
old_sizedbox_close = """      onPressed: (_submitting || _submitted) ? null : _submitReport,"""
# Actually let's find the full end of the old SizedBox and add Column close
# The submit button SizedBox ends with ); before the next Widget method
# Let's find it by looking for the width: double.infinity pattern
old_end_pattern = "      onPressed: (_submitting || _submitted) ? null : _submitReport,\n    );\n\n  Widget _buildAddFindingButton"
new_end_pattern = "      onPressed: (_submitting || _submitted) ? null : _submitReport,\n    ),\n    ],\n  );\n\n  Widget _buildAddFindingButton"
if old_end_pattern in text:
    text = text.replace(old_end_pattern, new_end_pattern, 1)
    print("Step 6: closed Column wrapper on submit button")
else:
    # Try alternate spacing
    old_end_alt = "      onPressed: (_submitting || _submitted) ? null : _submitReport,\n    );\n\n  Widget _FindingCard"
    new_end_alt = "      onPressed: (_submitting || _submitted) ? null : _submitReport,\n    ),\n    ],\n  );\n\n  Widget _FindingCard"
    if old_end_alt in text:
        text = text.replace(old_end_alt, new_end_alt, 1)
        print("Step 6 (alt): closed Column wrapper on submit button")
    else:
        print("WARNING: could not auto-close Column - checking structure...")
        # Print lines around submit button for manual inspection
        lines = text.split('\n')
        for i, l in enumerate(lines, 1):
            if '_buildSubmitButton' in l or '_buildAddFinding' in l or ('onPressed' in l and 'submitted' in l):
                print(f"  {i}: {l}")

if text != original:
    p.write_text(text, encoding='utf-8')
    print("\nDone.")
    print("Run: flutter analyze lib\\features\\scouting\\presentation\\scouting_screen.dart 2>&1 | Select-String -Pattern 'error' | Select-Object -First 20")
else:
    print("No changes written.")