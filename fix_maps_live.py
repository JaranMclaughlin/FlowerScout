import pathlib

p = pathlib.Path('lib/features/maps/presentation/maps_screen.dart')
txt = p.read_text(encoding='utf-8')

old = """  Widget build(BuildContext context, WidgetRef ref) {
    final trailsAsync = ref.watch(activeTrailsProvider);
    return trailsAsync.when(
      loading: () => const Center(child: CircularProgressIndicator(color: _green, strokeWidth: 2)),
      error: (e, _) => Center(child: Text(s.couldNotLoadLive, style: const TextStyle(color: _muted))),
      data: (trails) {
        if (trails.isEmpty) {
          return const Center(
            child: Padding(
              padding: EdgeInsets.all(24),
              child: Column(mainAxisSize: MainAxisSize.min, children: [
                Icon(Icons.route_rounded, color: _muted, size: 36),
                SizedBox(height: 12),
                Text(s.noScoutsOut,
                    style: TextStyle(color: _muted, fontSize: 13)),
              ]),
            ),
          );
        }"""

new = """  Widget build(BuildContext context, WidgetRef ref) {
    final s = AppStrings.of(ref.watch(localeProvider));
    final trailsAsync = ref.watch(activeTrailsProvider);
    return trailsAsync.when(
      loading: () => const Center(child: CircularProgressIndicator(color: _green, strokeWidth: 2)),
      error: (e, _) => Center(child: Text(s.couldNotLoadLive, style: const TextStyle(color: _muted))),
      data: (trails) {
        if (trails.isEmpty) {
          return Center(
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Column(mainAxisSize: MainAxisSize.min, children: [
                const Icon(Icons.route_rounded, color: _muted, size: 36),
                const SizedBox(height: 12),
                Text(s.noScoutsOut,
                    style: const TextStyle(color: _muted, fontSize: 13)),
              ]),
            ),
          );
        }"""

txt = txt.replace(old, new)
p.write_text(txt, encoding='utf-8')
print('done')