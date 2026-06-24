import pathlib

p = pathlib.Path('lib/features/maps/presentation/maps_screen.dart')
txt = p.read_text(encoding='utf-8')

txt = txt.replace(
    "import '../../../core/session/user_session.dart';",
    "import '../../../core/session/user_session.dart';\nimport '../../../shared/l10n/app_strings.dart';\nimport '../../../shared/providers/locale_provider.dart';"
)
txt = txt.replace(
    "const Text('Scout Trail Map',",
    "Text(AppStrings.of(ref.watch(localeProvider)).scoutTrailMap,"
)
txt = txt.replace(
    "const Text(\n                'Trail tracking and playback are available to farm managers and admins.',",
    "Text(\n                AppStrings.of(ref.watch(localeProvider)).trailManagerOnly,"
)
txt = txt.replace(
    "  Widget build(BuildContext context) {\n    return Scaffold(",
    "  Widget build(BuildContext context) {\n    final s = AppStrings.of(ref.watch(localeProvider));\n    return Scaffold("
)
txt = txt.replace("_toggleChip('Live Now', _showLive,", "_toggleChip(s.liveNow, _showLive,")
txt = txt.replace("_toggleChip('History', !_showLive,", "_toggleChip(s.history, !_showLive,")
txt = txt.replace("const Center(child: Text('Could not load trail history', style: TextStyle(color: _muted)))", "Center(child: Text(AppStrings.of(ref.watch(localeProvider)).couldNotLoadHistory, style: const TextStyle(color: _muted)))")
txt = txt.replace("const Center(child: Text('No completed trails yet', style: TextStyle(color: _muted, fontSize: 13)))", "Center(child: Text(AppStrings.of(ref.watch(localeProvider)).noCompletedTrails, style: const TextStyle(color: _muted, fontSize: 13)))")
txt = txt.replace("const Text('Delete trail?')", "Text(AppStrings.of(ref.watch(localeProvider)).deleteTrail)")
txt = txt.replace("const Text('This will permanently delete the trail and all its GPS points.')", "Text(AppStrings.of(ref.watch(localeProvider)).deleteTrailMsg)")
txt = txt.replace("Text(widget.isLive ? 'Live trail' : 'Trail playback')", "Text(widget.isLive ? AppStrings.of(ref.watch(localeProvider)).liveTrail : AppStrings.of(ref.watch(localeProvider)).trailPlayback)")
txt = txt.replace("const Center(child: Text('No GPS points recorded for this trail', style: TextStyle(color: _muted)))", "Center(child: Text(AppStrings.of(ref.watch(localeProvider)).noGpsPoints, style: const TextStyle(color: _muted)))")
p.write_text(txt, encoding='utf-8')
print('maps done')

p2 = pathlib.Path('lib/features/analytics/presentation/analytics_screen.dart')
txt2 = p2.read_text(encoding='utf-8')
txt2 = txt2.replace(
    'AppStrings get s => AppStrings.of(ref.read(localeProvider));',
    'AppStrings get s => AppStrings.of(ref.watch(localeProvider));'
)
p2.write_text(txt2, encoding='utf-8')
print('analytics done')