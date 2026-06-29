import pathlib

p = pathlib.Path('lib/features/scouting/presentation/topbar_widgets.dart')
txt = p.read_text(encoding='utf-8', errors='replace')

txt = txt.replace(
    'timeLabel: _timeAgo(n.time),',
    'timeLabel: _timeAgo(n.time, s),'
)

p.write_text(txt, encoding='utf-8')
print('done')