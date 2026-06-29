import pathlib, sys

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

old = "              if(mounted) { ScaffoldMessenger.of(context).showSnackBar(SnackBar(\n                content:Text('PDF export failed: $e'),\n                behavior:SnackBarBehavior.floating,\n                shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(10))));\n            }\n          },\n          style:ElevatedButton.styleFrom(backgroundColor:_P.forest,foregroundColor:Colors.white,\n            elevation:0,shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(8))),\n          child:Text(s.download)),"

new = "              if(mounted) { ScaffoldMessenger.of(context).showSnackBar(SnackBar(\n                content:Text('PDF export failed: $e'),\n                behavior:SnackBarBehavior.floating,\n                shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(10)))); }\n            }\n          },\n          style:ElevatedButton.styleFrom(backgroundColor:_P.forest,foregroundColor:Colors.white,\n            elevation:0,shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(8))),\n          child:Text(s.download)),"

if old not in text:
    sys.exit("Anchor not found.")

text = text.replace(old, new)
p.write_text(text, encoding='utf-8')
print("Fixed: catch block and ElevatedButton restored.")