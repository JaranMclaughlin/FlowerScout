import pathlib

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
lines = p.read_text(encoding='utf-8').split('\n')

# Line 522: TEAM MEMBERS label
lines[521] = "          label: '${_s.teamManagement} (${members.length})',"

# Line 540: EMAIL in wide layout
lines[539] = "              Expanded(child: _styledTextField(label: _s.emailLabel.toUpperCase(),"

# Line 556-557: ROLE dropdown in narrow layout - fix label and items
lines[555] = "            _labeledDropdown(label: _s.roleLabel.toUpperCase(), value: _roleKeyToLabel(_inviteRole, _s),"
lines[556] = "                items: [_s.roleScout, _s.roleViewer, _s.roleManager],"

p.write_text('\n'.join(lines), encoding='utf-8')
print("Fixed: TEAM MEMBERS, EMAIL (wide), ROLE (narrow)")