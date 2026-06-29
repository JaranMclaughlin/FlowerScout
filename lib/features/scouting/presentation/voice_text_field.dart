import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart';

/// Drop-in replacement for the issue text field inside _FindingCard.
/// Shows a mic button alongside the text field; tap to start/stop listening.
class VoiceTextField extends StatefulWidget {
  final TextEditingController controller;
  final String hint;
  final ValueChanged<String> onChanged;

  const VoiceTextField({
    super.key,
    required this.controller,
    required this.hint,
    required this.onChanged,
  });

  @override
  State<VoiceTextField> createState() => _VoiceTextFieldState();
}

class _VoiceTextFieldState extends State<VoiceTextField> {
  final SpeechToText _stt = SpeechToText();
  bool _available = false;
  bool _listening = false;
  String _prior   = '';   // text before mic was pressed

  @override
  void initState() {
    super.initState();
    _init();
  }

  Future<void> _init() async {
    final ok = await _stt.initialize(
      onError: (_) => _stopListening(),
    );
    if (mounted) setState(() => _available = ok);
  }

  Future<void> _toggleListening() async {
    if (!_available) return;
    if (_listening) {
      _stopListening();
    } else {
      _prior = widget.controller.text;
      setState(() => _listening = true);
      await _stt.listen(
        onResult: (result) {
          final spoken = result.recognizedWords;
          final updated = _prior.isEmpty ? spoken : '$_prior $spoken';
          widget.controller.text = updated;
          widget.controller.selection = TextSelection.fromPosition(
            TextPosition(offset: updated.length));
          widget.onChanged(updated);
        },
        listenFor: const Duration(seconds: 30),
        pauseFor: const Duration(seconds: 4),
        cancelOnError: true,
        partialResults: true,
        localeId: 'en_US',
      );
    }
  }

  void _stopListening() {
    _stt.stop();
    if (mounted) setState(() => _listening = false);
  }

  @override
  void dispose() {
    _stt.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    const borderColor  = Color(0xFFDDE5DD);
    const bgColor      = Color(0xFFF8FAF8);
    const labelColor   = Color(0xFF6B7F6E);
    const activeGreen  = Color(0xFF40916C);
    const forestGreen  = Color(0xFF1B4332);

    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      const Padding(
        padding: EdgeInsets.only(left: 2, bottom: 6),
        child: Text('ISSUE / OBSERVATION',
          style: TextStyle(fontSize: 10, fontWeight: FontWeight.w700,
              letterSpacing: 1.0, color: labelColor)),
      ),
      Container(
        decoration: BoxDecoration(
          color: _listening ? activeGreen.withValues(alpha: 0.06) : bgColor,
          borderRadius: BorderRadius.circular(10),
          border: Border.all(
            color: _listening ? activeGreen : borderColor,
            width: _listening ? 1.5 : 1.0,
          ),
        ),
        child: Row(crossAxisAlignment: CrossAxisAlignment.end, children: [
          Expanded(
            child: TextField(
              controller: widget.controller,
              onChanged: widget.onChanged,
              maxLines: null,
              minLines: 2,
              style: const TextStyle(fontSize: 13, color: Color(0xFF0D1B0F)),
              decoration: InputDecoration(
                hintText: widget.hint,
                hintStyle: const TextStyle(color: labelColor, fontSize: 13),
                border: InputBorder.none,
                contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
              ),
            ),
          ),
          if (_available)
            Padding(
              padding: const EdgeInsets.only(right: 8, bottom: 8),
              child: GestureDetector(
                onTap: _toggleListening,
                child: AnimatedContainer(
                  duration: const Duration(milliseconds: 200),
                  width: 36, height: 36,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: _listening ? activeGreen : forestGreen.withValues(alpha: 0.08),
                    border: Border.all(
                      color: _listening ? activeGreen : borderColor,
                    ),
                  ),
                  child: Icon(
                    _listening ? Icons.mic_rounded : Icons.mic_none_rounded,
                    size: 18,
                    color: _listening ? Colors.white : const Color(0xFF3D4F42),
                  ),
                ),
              ),
            ),
        ]),
      ),
      if (_listening)
        const Padding(
          padding: EdgeInsets.only(left: 4, top: 4),
          child: Row(children: [
            SizedBox(width: 6, height: 6,
              child: CircularProgressIndicator(strokeWidth: 1.5,
                  color: Color(0xFF40916C))),
            SizedBox(width: 6),
            Text('Listening…',
              style: TextStyle(fontSize: 11, color: Color(0xFF40916C),
                  fontWeight: FontWeight.w500)),
          ]),
        ),
    ]);
  }
}
