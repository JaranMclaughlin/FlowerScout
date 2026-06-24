import pathlib

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
txt = p.read_text(encoding='utf-8')

txt = txt.replace(
    '        child: Row(children: [\n          Icon(meta.icon, size: 18, color: active ? _C.leaf : _C.slate),\n          const SizedBox(width: 10),\n          Text(meta.label, style: _T.body.copyWith(\n            color: active ? _C.forest : _C.slate,\n            fontWeight: active ? FontWeight.w600 : FontWeight.w400,\n          )),\n        ]),',
    '        child: Row(children: [\n          Icon(meta.icon, size: 18, color: active ? _C.leaf : _C.slate),\n          const SizedBox(width: 10),\n          Expanded(child: Text(meta.label, style: _T.body.copyWith(\n            color: active ? _C.forest : _C.slate,\n            fontWeight: active ? FontWeight.w600 : FontWeight.w400,\n          ), overflow: TextOverflow.ellipsis)),\n        ]),'
)

p.write_text(txt, encoding='utf-8')
print('done')