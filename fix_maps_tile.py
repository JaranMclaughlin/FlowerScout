import pathlib

p = pathlib.Path('lib/features/maps/presentation/maps_screen.dart')
text = p.read_text(encoding='utf-8')

old_tile = """        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(trail.scoutName ?? s.unknownScout,
                style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 14, color: _ink)),
            const SizedBox(height: 2),
            if (farmText != null)
              Padding(padding: const EdgeInsets.only(bottom: 2),
                child: Row(children: [
                  const Icon(Icons.agriculture_rounded, size: 12, color: _green),
                  const SizedBox(width: 4),
                  Text(farmText, style: const TextStyle(fontSize: 12, color: _green, fontWeight: FontWeight.w600)),
                ])),
            Text(statusText + _fmtDur(duration), style: const TextStyle(fontSize: 12, color: _muted)),
          ])),"""

new_tile = """        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(trail.scoutName ?? s.unknownScout,
                style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 14, color: _ink)),
            const SizedBox(height: 2),
            if (farmText != null)
              Padding(padding: const EdgeInsets.only(bottom: 2),
                child: Row(children: [
                  const Icon(Icons.agriculture_rounded, size: 12, color: _green),
                  const SizedBox(width: 4),
                  Text(farmText, style: const TextStyle(fontSize: 12, color: _green, fontWeight: FontWeight.w600)),
                ])),
            Text(statusText + _fmtDur(duration), style: const TextStyle(fontSize: 12, color: _muted)),
            if (trail.points.isNotEmpty) ...[
              const SizedBox(height: 2),
              Row(children: [
                const Icon(Icons.route_rounded, size: 11, color: _muted),
                const SizedBox(width: 3),
                Text(
                  _fmtDist(_calcDistance(trail.points.map((p) => LatLng(p.lat, p.lng)).toList())),
                  style: const TextStyle(fontSize: 11, color: _muted),
                ),
                const SizedBox(width: 8),
                const Icon(Icons.location_on_rounded, size: 11, color: _muted),
                const SizedBox(width: 3),
                Text('${trail.points.length} pts', style: const TextStyle(fontSize: 11, color: _muted)),
              ]),
            ],
          ])),"""

if old_tile not in text:
    import sys; sys.exit("Tile anchor not found.")
text = text.replace(old_tile, new_tile, 1)
p.write_text(text, encoding='utf-8')
print("maps_screen.dart fixed.")