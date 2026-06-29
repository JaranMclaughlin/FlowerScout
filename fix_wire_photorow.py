import pathlib, shutil

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
shutil.copy(p, p.with_suffix('.dart.bak7'))
text = p.read_text(encoding='utf-8')

# Fix 1: wire _buildPhotoRow() into the card build
old_issue_end = """            _labeledField(widget.s.issueObservation, _issueCtrl, hint: widget.s.describeObserved, (v) {
              widget.data.issue = v;
              widget.onChanged();
            }),
            const SizedBox(height: 14),
          ]),"""
new_issue_end = """            _labeledField(widget.s.issueObservation, _issueCtrl, hint: widget.s.describeObserved, (v) {
              widget.data.issue = v;
              widget.onChanged();
            }),
            _buildPhotoRow(),
          ]),"""
if old_issue_end in text:
    text = text.replace(old_issue_end, new_issue_end, 1)
    print("Fix 1: _buildPhotoRow() wired into finding card")
else:
    print("ERROR: issue field closing not found"); raise SystemExit(1)

p.write_text(text, encoding='utf-8')
print("Saved.")