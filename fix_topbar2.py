import pathlib
import re

p = pathlib.Path('lib/features/scouting/presentation/topbar_widgets.dart')
text = p.read_text(encoding='utf-8')
changes = []

# 1. Loading chip - missing closing brackets after the Text('Loading...') row
old_loading = """              Text(
                'Loading...',
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                  color: _C.graphite,
                ),
              ),
      );
    }"""
new_loading = """              Text(
                'Loading...',
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                  color: _C.graphite,
                ),
              ),
            ],
          ),
        ),
      );
    }"""
if old_loading in text:
    text = text.replace(old_loading, new_loading, 1)
    changes.append("loading chip brackets")
else:
    raise SystemExit("Loading chip anchor not found - aborting, no changes saved.")

# 2. Temperature header - match by structure, ignore corrupted literal content
temp_pattern = re.compile(
    r"Text\(\s*'[^']*',\s*Text\(\s*style: const TextStyle\(\s*color: Colors\.white,\s*fontSize: 36,\s*fontWeight: FontWeight\.w800,\s*height: 1,\s*\),\s*\),",
    re.DOTALL,
)
temp_replacement = (
    "Text(\n"
    "                        '${weather.tempC.round()}\u00b0C',\n"
    "                        style: const TextStyle(\n"
    "                          color: Colors.white,\n"
    "                          fontSize: 36,\n"
    "                          fontWeight: FontWeight.w800,\n"
    "                          height: 1,\n"
    "                        ),\n"
    "                      ),"
)
new_text, count = temp_pattern.subn(temp_replacement, text, count=1)
if count == 0:
    raise SystemExit("Temperature header pattern not found - aborting, no changes saved.")
text = new_text
changes.append("temperature header")

# 3. Stats row - feelsLike tile, match by structure, ignore corrupted literal
stats_pattern = re.compile(
    r"_StatTile\(\s*icon: Icons\.thermostat_rounded,\s*color: const Color\(0xFFE65100\),\s*label: s\.feelsLike,\s*value: '[^']*',?\s*\),\s*\),\s*const SizedBox\(height: 20\),",
    re.DOTALL,
)
stats_replacement = (
    "_StatTile(\n"
    "                    icon: Icons.thermostat_rounded,\n"
    "                    color: const Color(0xFFE65100),\n"
    "                    label: s.feelsLike,\n"
    "                    value: '${weather.tempC.round()}\u00b0C'),\n"
    "              ],\n"
    "            ),\n"
    "          ),\n"
    "          const SizedBox(height: 20),"
)
new_text, count = stats_pattern.subn(stats_replacement, text, count=1)
if count == 0:
    raise SystemExit("Stats row pattern not found - aborting, no changes saved.")
text = new_text
changes.append("stats row brackets")

# 4. _buildEmpty() needs `s` threaded through
old_call = "                  ? _buildEmpty()"
new_call = "                  ? _buildEmpty(s)"
if old_call in text:
    text = text.replace(old_call, new_call, 1)
    changes.append("_buildEmpty call site")
else:
    raise SystemExit("_buildEmpty call site anchor not found - aborting, no changes saved.")

old_def = "  Widget _buildEmpty() {"
new_def = "  Widget _buildEmpty(AppStrings s) {"
if old_def in text:
    text = text.replace(old_def, new_def, 1)
    changes.append("_buildEmpty definition")
else:
    raise SystemExit("_buildEmpty definition anchor not found - aborting, no changes saved.")

p.write_text(text, encoding='utf-8')
print("topbar_widgets.dart fixed: " + ", ".join(changes))