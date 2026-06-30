import pathlib
p = pathlib.Path('.env')
lines = p.read_text().splitlines()
for l in lines:
    print(l.split('=')[0])