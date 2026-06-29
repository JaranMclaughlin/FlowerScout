import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
text = p.read_text(encoding='utf-8')

# Both chart renderers have the same pattern — replace both occurrences
old_label = "            return Padding(padding:const EdgeInsets.only(top:4),\n              child:Text(labels[i],style:const TextStyle(fontSize:9,color:AppColors.slate)));"
new_label = "            final lbl=labels[i].length>3?labels[i].substring(0,3):labels[i];\n            return Padding(padding:const EdgeInsets.only(top:4),\n              child:Text(lbl,style:const TextStyle(fontSize:9,color:AppColors.slate)));"

count = text.count(old_label)
text = text.replace(old_label, new_label)
p.write_text(text, encoding='utf-8')
print(f"Fixed {count} chart label occurrence(s).")