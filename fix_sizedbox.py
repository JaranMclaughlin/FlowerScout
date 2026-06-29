import pathlib, shutil

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
shutil.copy(p, p.with_suffix('.dart.bak4'))
text = p.read_text(encoding='utf-8')

old_sizedbox = """      SizedBox(
    width: double.infinity, height: 54,
    child: ElevatedButton.icon(
      icon: _submitting
          ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
          : const Icon(Icons.check_circle_rounded),
      label: Text(_submitting ? s.submitting : s.submitReport,
        style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
      // Disabled if submitting OR already submitted (duplicate guard)
      onPressed: (_submitting || _submitted) ? null : _submitReport,
      style: ElevatedButton.styleFrom(
        backgroundColor: _C.forest, foregroundColor: Colors.white, elevation: 0,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      ),
    ),
    ],
  );
}"""

new_sizedbox = """      SizedBox(
        width: double.infinity, height: 54,
        child: ElevatedButton.icon(
          icon: _submitting
              ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
              : const Icon(Icons.check_circle_rounded),
          label: Text(_submitting ? s.submitting : s.submitReport,
            style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
          // Disabled if submitting OR already submitted (duplicate guard)
          onPressed: (_submitting || _submitted) ? null : _submitReport,
          style: ElevatedButton.styleFrom(
            backgroundColor: _C.forest, foregroundColor: Colors.white, elevation: 0,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
          ),
        ),
      ),
    ],
  );
}"""

if old_sizedbox in text:
    text = text.replace(old_sizedbox, new_sizedbox, 1)
    p.write_text(text, encoding='utf-8')
    print("Fixed: SizedBox closed and indentation corrected")
else:
    print("ERROR: anchor not found - printing repr of lines 718-735:")
    for i, l in enumerate(text.split('\n')[717:735], 718):
        print(f"  {i}: {repr(l)}")