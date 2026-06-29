import pathlib, sys

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

old = "            if(_activeFilter!='all') {\n              GestureDetector(onTap:()=>setState((){_activeFilter='all';_showAllInspections=false;\n}})," + "\n                child:Container("

new = "            if(_activeFilter!='all')\n              GestureDetector(\n                onTap:()=>setState((){_activeFilter='all';_showAllInspections=false;}),\n                child:Container("

if old not in text:
    sys.exit("Anchor not found — check indentation.")

text = text.replace(old, new)
p.write_text(text, encoding='utf-8')
print("Fixed: GestureDetector block restored.")