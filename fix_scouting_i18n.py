import pathlib
p = pathlib.Path('lib/features/scouting/presentation/scouting_screen.dart')
t = p.read_text(encoding='utf-8')

# Fix first date block (lines 350-352)
old1 = """    final days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
    final months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    final dateStr = '${days[now.weekday-1]}, ${now.day} ${months[now.month-1]} ${now.year}';"""
new1 = """    final days = s.chartLabelsWeek;
    final months = s.monthsShort;
    final dateStr = '${days[now.weekday-1]}, ${now.day} ${months[now.month-1]} ${now.year}';"""
if old1 not in t: raise SystemExit('anchor 1 not found')
t = t.replace(old1, new1, 1)

# Fix second date block (lines 390-392)
old2 = """    final days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
    final months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    final dateStr = '${days[now.weekday-1]}, ${now.day.toString().padLeft(2,"0")} ${months[now.month-1]} ${now.year}';"""
new2 = """    final days = s.chartLabelsWeek;
    final months = s.monthsShort;
    final dateStr = '${days[now.weekday-1]}, ${now.day.toString().padLeft(2,"0")} ${months[now.month-1]} ${now.year}';"""
if old2 not in t: raise SystemExit('anchor 2 not found')
t = t.replace(old2, new2, 1)

# Fix _addFinding hardcoded 'Disease' category
old3 = "void _addFinding([String category = 'Disease']) =>"
new3 = "void _addFinding([String? category]) {"
# Keep it simple - just use the string key not translated label for category
# category is stored in DB so keep as English key, only display is translated

p.write_text(t, encoding='utf-8')
print('scouting_screen.dart updated.')