import pathlib
p = pathlib.Path('lib/core/session/user_session.dart')
text = p.read_text(encoding='utf-8')
print(text)