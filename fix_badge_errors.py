import pathlib, shutil

p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
shutil.copy(p, p.with_suffix('.dart.bak3'))
text = p.read_text(encoding='utf-8')
original = text

# Fix 1: ScoutingScreenState -> _ScoutingScreenState
text = text.replace(
    'await ScoutingScreenState.queueLength()',
    'await _ScoutingScreenState.queueLength()', 1)
print("Fix 1: corrected state class name in _refreshQueueCount")

# Fix 2: also fix main.dart reference
import pathlib as pl
mp = pl.Path('lib/main.dart')
mt = mp.read_text(encoding='utf-8')
if 'ScoutingScreenState.drainQueue' in mt:
    mt = mt.replace('ScoutingScreenState.drainQueue', '_ScoutingScreenState.drainQueue')
    mp.write_text(mt, encoding='utf-8')
    print("Fix 2: corrected state class name in main.dart")
else:
    print("Fix 2: main.dart already correct or not found")

# Fix 3: close the Column - line 733 has ); but needs ],  before it
old_end = "    ),\n  );\n}\n\nclass _FindingCard"
new_end = "    ),\n    ],\n  );\n}\n\nclass _FindingCard"
if old_end in text:
    text = text.replace(old_end, new_end, 1)
    print("Fix 3: closed Column with ],")
else:
    # Try with method-style ending (no bare })
    old_end2 = "    ),\n  );\n\n\nclass _FindingCard"
    new_end2 = "    ),\n    ],\n  );\n\n\nclass _FindingCard"
    if old_end2 in text:
        text = text.replace(old_end2, new_end2, 1)
        print("Fix 3 alt: closed Column with ],")
    else:
        # Print raw chars around line 733 for exact match
        lines = text.split('\n')
        print("Fix 3 WARNING: printing lines 728-738 for inspection:")
        for i, l in enumerate(lines[727:738], 728):
            print(f"  {i}: {repr(l)}")

if text != original:
    p.write_text(text, encoding='utf-8')

print("\nAnalyzing...")