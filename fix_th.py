import pathlib
rp = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
rc = rp.read_text(encoding='utf-8')
rc = rc.replace(
    "  Widget _th(String label,{int flex=1})=>Expanded(flex:flex,child:\n    Text(label,style:const TextStyle(fontSize:10,fontWeight:FontWeight.w700,\n      letterSpacing:0.8,color:_P.slate)));",
    "  Widget _th(String label, {int flex = 1}) {\n    return Expanded(flex: flex, child: Text(label,\n      style: const TextStyle(fontSize:10, fontWeight:FontWeight.w700,\n        letterSpacing:0.8, color:_P.slate)));\n  }"
)
rp.write_text(rc, encoding='utf-8')
print('done')