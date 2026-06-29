import pathlib

p = pathlib.Path('lib/features/scouting/presentation/topbar_widgets.dart')
text = p.read_text(encoding='utf-8')

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
if old_loading not in text:
    raise SystemExit("Loading chip anchor not found - aborting, no changes made.")
text = text.replace(old_loading, new_loading, 1)

# 2. Temperature header - mangled into two overlapping Text() calls with mojibake placeholder
old_temp = """                      Text(
                        'ï¿½C',
                      Text(
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 36,
                          fontWeight: FontWeight.w800,
                          height: 1,
                        ),
                      ),"""
new_temp = """                      Text(
                        '\u00b0C'.replaceFirst('\u00b0', weather.tempC.round().toString() + '\u00b0'),
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 36,
                          fontWeight: FontWeight.w800,
                          height: 1,
                        ),
                      ),"""
if old_temp not in text:
    raise SystemExit("Temperature header anchor not found - aborting, no changes made.")
text = text.replace(old_temp, new_temp, 1)

# 3. Stats row - feelsLike tile has mojibake value and missing closing brackets for the Row
old_stats = """                _StatTile(
                    icon: Icons.thermostat_rounded,
                    color: const Color(0xFFE65100),
                    label: s.feelsLike,
                    value: 'ï¿½C',
                  ),
          ),
          const SizedBox(height: 20),"""
new_stats = """                _StatTile(
                    icon: Icons.thermostat_rounded,
                    color: const Color(0xFFE65100),
                    label: s.feelsLike,
                    value: '${weather.tempC.round()}\u00b0C'),
              ],
            ),
          ),
          const SizedBox(height: 20),"""
if old_stats not in text:
    raise SystemExit("Stats row anchor not found - aborting, no changes made.")
text = text.replace(old_stats, new_stats, 1)

# 4. _buildEmpty() needs `s` threaded through
old_call = "                  ? _buildEmpty()"
new_call = "                  ? _buildEmpty(s)"
if old_call not in text:
    raise SystemExit("_buildEmpty call site anchor not found - aborting, no changes made.")
text = text.replace(old_call, new_call, 1)

old_def = "  Widget _buildEmpty() {"
new_def = "  Widget _buildEmpty(AppStrings s) {"
if old_def not in text:
    raise SystemExit("_buildEmpty definition anchor not found - aborting, no changes made.")
text = text.replace(old_def, new_def, 1)

p.write_text(text, encoding='utf-8')
print("topbar_widgets.dart fixed: loading chip brackets, temperature display, stats row brackets, _buildEmpty(s).")