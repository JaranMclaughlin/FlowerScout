import pathlib

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
text = p.read_text(encoding='utf-8')

text = text.replace(
    "            ...{if (trailId != null) 'trail_id': trailId},",
    "            if (trailId != null) 'trail_id': trailId,"
)
text = text.replace(
    "          ...{if (trailId != null) 'trail_id': trailId},",
    "          if (trailId != null) 'trail_id': trailId,"
)

p.write_text(text, encoding='utf-8')
print("Reverted to if-entry syntax.")