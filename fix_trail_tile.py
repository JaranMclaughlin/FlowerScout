import pathlib

p = pathlib.Path('lib/features/maps/presentation/maps_screen.dart')
txt = p.read_text(encoding='utf-8')

txt = txt.replace(
    "    final duration = (trail.endedAt ?? DateTime.now()).difference(trail.startedAt);\n    final farms = ref.watch(farmsProvider).value ?? [];",
    "    final s = AppStrings.of(ref.watch(localeProvider));\n    final duration = (trail.endedAt ?? DateTime.now()).difference(trail.startedAt);\n    final farms = ref.watch(farmsProvider).value ?? [];"
)
txt = txt.replace(
    "    final statusText = isLive ? 'Live - ' : 'Completed - ';",
    "    final statusText = isLive ? s.liveTrail + ' - ' : s.history + ' - ';"
)
txt = txt.replace(
    "Text(trail.scoutName ?? 'Unknown scout',",
    "Text(trail.scoutName ?? s.unknownScout,"
)

p.write_text(txt, encoding='utf-8')
print('done')