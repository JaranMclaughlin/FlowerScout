import pathlib, re

p = pathlib.Path('lib/core/session/user_session.dart')
text = p.read_text(encoding='utf-8')

# Remove unused ManagerType enum and currentManagerType field
text = re.sub(
    r'\nenum ManagerType \{.*?\}\n',
    '\n',
    text, count=1, flags=re.DOTALL
)
text = text.replace(
    "\n  static ManagerType? currentManagerType;\n",
    "\n"
)

p.write_text(text, encoding='utf-8')
print("user_session.dart: ManagerType removed.")