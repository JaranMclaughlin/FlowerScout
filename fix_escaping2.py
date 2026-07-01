import pathlib
p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines()

# Line 1115 (index 1114)
old_1115 = lines[1114]
new_1115 = old_1115.replace("\\$", "$")
lines[1114] = new_1115

# Line 1309 (index 1308)
old_1309 = lines[1308]
new_1309 = old_1309.replace("\\$", "$").replace("\\'", "'")
lines[1308] = new_1309

p.write_text("\n".join(lines) + "\n", encoding="utf-8")

print("LINE 1115 BEFORE:", repr(old_1115))
print("LINE 1115 AFTER: ", repr(new_1115))
print()
print("LINE 1309 BEFORE:", repr(old_1309))
print("LINE 1309 AFTER: ", repr(new_1309))