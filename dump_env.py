import pathlib
p = pathlib.Path('lib/main.dart')
lines = p.read_text(encoding='utf-8').splitlines()
for i, line in enumerate(lines, start=1):
    if any(x in line for x in ['SUPABASE', 'publishable', 'anonKey', 'anon']):
        print(f"{i}\t{repr(line)}")