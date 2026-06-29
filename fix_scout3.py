import pathlib, sys

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
text = p.read_text(encoding='utf-8')
original = text

# 231 and 308: replace if(...) map entry with spread pattern
text = text.replace(
    "            if (trailId != null) 'trail_id': trailId,",
    "            ...{if (trailId != null) 'trail_id': trailId},"
)
text = text.replace(
    "          if (trailId != null) 'trail_id': trailId,",
    "          ...{if (trailId != null) 'trail_id': trailId},"
)

# 836: if(bytes == null) return Container(  — wrap in braces
text = text.replace(
    "                  if (bytes == null) return Container(\n                    width: 80, height: 80,",
    "                  if (bytes == null) { return Container(\n                    width: 80, height: 80,"
)
# find the closing ); of that Container and add the brace after it
text = text.replace(
    "                      borderRadius: BorderRadius.circular(8),\n                    ),\n                    child: const Icon(Icons.image_rounded, color: Color(0xFF6B7F6E)),\n                  );",
    "                      borderRadius: BorderRadius.circular(8),\n                    ),\n                    child: const Icon(Icons.image_rounded, color: Color(0xFF6B7F6E)),\n                  ); }"
)

if text == original:
    print("No changes — anchors differ.")
else:
    p.write_text(text, encoding='utf-8')
    print("Done.")