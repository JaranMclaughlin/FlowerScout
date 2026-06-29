import pathlib, shutil

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
shutil.copy(p, p.with_suffix('.dart.bak6'))
text = p.read_text(encoding='utf-8')
original = text

# ── Step 1: Add image_picker import ──────────────────────────────────────────
old_imports = "import 'dart:async';\nimport 'dart:convert';\nimport 'package:flutter/material.dart';"
new_imports  = """import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:uuid/uuid.dart';"""
if old_imports in text:
    text = text.replace(old_imports, new_imports, 1)
    print("Step 1: added imports")
else:
    print("ERROR: import anchor not found"); raise SystemExit(1)

# ── Step 2: Add photoUrls to FindingData ─────────────────────────────────────
old_finding = """class FindingData {
  String category;
  String severity;
  String issue;
  FindingData({this.category = 'Disease', this.severity = 'Medium', this.issue = ''});
}"""
new_finding = """class FindingData {
  String category;
  String severity;
  String issue;
  List<XFile>  photoFiles = [];   // local files (pre-upload)
  List<String> photoUrls  = [];   // Supabase Storage URLs (post-upload)
  FindingData({this.category = 'Disease', this.severity = 'Medium', this.issue = ''});
}"""
if old_finding in text:
    text = text.replace(old_finding, new_finding, 1)
    print("Step 2: added photoFiles + photoUrls to FindingData")
else:
    print("ERROR: FindingData anchor not found"); raise SystemExit(1)

# ── Step 3: Upload photos in _submitReport before inserting findings ──────────
old_finding_insert = """      for (final finding in findings.where((f) => f.issue.trim().isNotEmpty)) {
        await Supabase.instance.client.from('inspection_findings').insert({
          'report_id': reportId['id'],
          'category': finding.category,
          'severity': finding.severity,
          'issue': finding.issue.trim(),
        });
      }"""
new_finding_insert = """      for (final finding in findings.where((f) => f.issue.trim().isNotEmpty)) {
        // Upload any photos for this finding
        final List<String> uploadedUrls = [];
        for (final photo in finding.photoFiles) {
          try {
            final bytes    = await photo.readAsBytes();
            final ext      = photo.name.split('.').last.toLowerCase();
            final fileName = '${const Uuid().v4()}.$ext';
            final path     = 'findings/${reportId['id']}/$fileName';
            await Supabase.instance.client.storage
                .from('finding-photos')
                .uploadBinary(path, bytes,
                    fileOptions: FileOptions(contentType: 'image/$ext', upsert: false));
            final url = Supabase.instance.client.storage
                .from('finding-photos')
                .getPublicUrl(path);
            uploadedUrls.add(url);
          } catch (photoErr) {
            debugPrint('[photos] upload failed: \$photoErr');
          }
        }
        await Supabase.instance.client.from('inspection_findings').insert({
          'report_id': reportId['id'],
          'category': finding.category,
          'severity': finding.severity,
          'issue': finding.issue.trim(),
          if (uploadedUrls.isNotEmpty) 'photo_urls': uploadedUrls,
        });
      }"""
if old_finding_insert in text:
    text = text.replace(old_finding_insert, new_finding_insert, 1)
    print("Step 3: photo upload wired into submit")
else:
    print("ERROR: finding insert anchor not found"); raise SystemExit(1)

# ── Step 4: Add photo fields to offline queue payload ────────────────────────
old_queue_finding = """        }, findings.where((f) => f.issue.trim().isNotEmpty).map((f) => {
          'category': f.category,
          'severity': f.severity,
          'issue': f.issue.trim(),
        }).toList());"""
new_queue_finding = """        }, findings.where((f) => f.issue.trim().isNotEmpty).map((f) => {
          'category': f.category,
          'severity': f.severity,
          'issue': f.issue.trim(),
          // photos are local files - paths only, re-upload on drain
          'photo_paths': f.photoFiles.map((x) => x.path).toList(),
        }).toList());"""
if old_queue_finding in text:
    text = text.replace(old_queue_finding, new_queue_finding, 1)
    print("Step 4: photo paths added to offline queue payload")
else:
    print("WARNING: offline queue finding anchor not found - skipping")

# ── Step 5: Add _issueCtrl to _FindingCardState + photo picker state ─────────
old_card_state = """class _FindingCardState extends State<_FindingCard> {
  late TextEditingController _issueCtrl;"""
new_card_state = """class _FindingCardState extends State<_FindingCard> {
  late TextEditingController _issueCtrl;
  final _picker = ImagePicker();
  bool _pickingPhoto = false;"""
if old_card_state in text:
    text = text.replace(old_card_state, new_card_state, 1)
    print("Step 5: added picker state to _FindingCardState")
else:
    print("ERROR: _FindingCardState anchor not found"); raise SystemExit(1)

# ── Step 6: Add photo picker helpers to _FindingCardState ────────────────────
old_init = """  @override
  void initState() {
    super.initState();
    _issueCtrl = TextEditingController(text: widget.data.issue);
  }"""
new_init = """  @override
  void initState() {
    super.initState();
    _issueCtrl = TextEditingController(text: widget.data.issue);
  }

  Future<void> _pickPhoto(ImageSource source) async {
    if (_pickingPhoto) return;
    setState(() => _pickingPhoto = true);
    try {
      final file = await _picker.pickImage(source: source, imageQuality: 80, maxWidth: 1920);
      if (file != null) {
        setState(() => widget.data.photoFiles.add(file));
        widget.onChanged();
      }
    } catch (e) {
      debugPrint('[photos] pick failed: \$e');
    } finally {
      if (mounted) setState(() => _pickingPhoto = false);
    }
  }

  void _removePhoto(int index) {
    setState(() => widget.data.photoFiles.removeAt(index));
    widget.onChanged();
  }

  Widget _buildPhotoRow() {
    final photos = widget.data.photoFiles;
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      const SizedBox(height: 14),
      Row(children: [
        const Icon(Icons.photo_camera_rounded, size: 14, color: Color(0xFF6B7F6E)),
        const SizedBox(width: 6),
        Text('Photos (${photos.length}/5)',
            style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600,
                color: Color(0xFF6B7F6E), letterSpacing: 0.5)),
        const Spacer(),
        if (photos.length < 5) ...[
          // Camera button - not available on web
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
          if (!kIsWeb) const SizedBox(width: 8),
          GestureDetector(
            onTap: () => _pickPhoto(ImageSource.gallery),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
              decoration: BoxDecoration(
                color: const Color(0xFF2D6A4F).withValues(alpha: 0.08),
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: const Color(0xFF2D6A4F).withValues(alpha: 0.2)),
              ),
              child: Row(mainAxisSize: MainAxisSize.min, children: [
                const Icon(Icons.photo_library_rounded, size: 14, color: Color(0xFF2D6A4F)),
                const SizedBox(width: 4),
                const Text('Gallery', style: TextStyle(fontSize: 11,
                    color: Color(0xFF2D6A4F), fontWeight: FontWeight.w600)),
              ]),
            ),
          ),
        ],
      ]),
      if (photos.isNotEmpty) ...[
        const SizedBox(height: 10),
        SizedBox(
          height: 80,
          child: ListView.separated(
            scrollDirection: Axis.horizontal,
            itemCount: photos.length,
            separatorBuilder: (_, __) => const SizedBox(width: 8),
            itemBuilder: (context, i) => Stack(children: [
              ClipRRect(
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
              ),
              Positioned(top: 2, right: 2,
                child: GestureDetector(
                  onTap: () => _removePhoto(i),
                  child: Container(
                    width: 20, height: 20,
                    decoration: const BoxDecoration(
                        color: Color(0xFFD32F2F), shape: BoxShape.circle),
                    child: const Icon(Icons.close_rounded, size: 12, color: Colors.white),
                  ),
                ),
              ),
            ]),
          ),
        ),
      ],
    ]);
  }"""
if old_init in text:
    text = text.replace(old_init, new_init, 1)
    print("Step 6: added _pickPhoto, _removePhoto, _buildPhotoRow to _FindingCardState")
else:
    print("ERROR: initState anchor not found"); raise SystemExit(1)

# ── Step 7: Wire _buildPhotoRow into the finding card build ──────────────────
old_issue_field = """            _labeledField(widget.s.issueObservation, _issueCtrl, hint: widget.s.describeObserved, (v) {
              widget.data.issue = v;
              widget.onChanged();"""
new_issue_field = """            _labeledField(widget.s.issueObservation, _issueCtrl, hint: widget.s.describeObserved, (v) {
              widget.data.issue = v;
              widget.onChanged();"""
# Just add _buildPhotoRow() after the issue field closing
# Find the closing of the issue field block
old_after_issue = """              widget.data.issue = v;
              widget.onChanged();
            }),
          ]),
        ),
      ],
    );
  }

  Widget _labeledDropdown"""
new_after_issue = """              widget.data.issue = v;
              widget.onChanged();
            }),
            _buildPhotoRow(),
          ]),
        ),
      ],
    );
  }

  Widget _labeledDropdown"""
if old_after_issue in text:
    text = text.replace(old_after_issue, new_after_issue, 1)
    print("Step 7: wired _buildPhotoRow into finding card")
else:
    print("WARNING: issue field closing anchor not found - checking alternate")
    # Try without the trailing widget
    old_after2 = """              widget.data.issue = v;
              widget.onChanged();
            }),
          ]),
        ),
      ],
    );
  }
}"""
    new_after2 = """              widget.data.issue = v;
              widget.onChanged();
            }),
            _buildPhotoRow(),
          ]),
        ),
      ],
    );
  }
}"""
    if old_after2 in text:
        text = text.replace(old_after2, new_after2, 1)
        print("Step 7 alt: wired _buildPhotoRow into finding card")
    else:
        print("ERROR: could not wire _buildPhotoRow - manual inspection needed")

if text != original:
    p.write_text(text, encoding='utf-8')
    print("\nDone.")
else:
    print("\nNo changes written.")