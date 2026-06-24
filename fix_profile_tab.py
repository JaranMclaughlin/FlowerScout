import pathlib

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
txt = p.read_text(encoding='utf-8')

txt = txt.replace("const _LoadingCard(message: 'Loading profile...')", "const _LoadingCard(message: 'Loading profile...')".replace("'Loading profile...'", "s.loadingProfile"))
txt = txt.replace("_sectionHeader('Your profile',\n              'Update your personal details.',", "_sectionHeader(s.yourProfile,\n              s.yourProfileDesc,")
txt = txt.replace("_card(label: 'PERSONAL INFO', child: Column(children: [", "_card(label: s.personalInfo, child: Column(children: [")
txt = txt.replace("_styledTextField(label: 'FULL NAME', controller: _nameCtrl)", "_styledTextField(label: s.fullName, controller: _nameCtrl)")
txt = txt.replace("_styledTextField(label: 'EMAIL', controller: _emailCtrl,", "_styledTextField(label: s.emailLabel, controller: _emailCtrl,")
txt = txt.replace("_styledTextField(label: 'PHONE', controller: _phoneCtrl,", "_styledTextField(label: s.phone, controller: _phoneCtrl,")
txt = txt.replace("_saveButton('Save profile', onTap:", "_saveButton(s.saveProfile, onTap:")
txt = txt.replace("_sectionHeader('Team management',\n          'View and manage team access.',", "_sectionHeader(s.teamManagement,\n          s.teamManagementDesc,")

p.write_text(txt, encoding='utf-8')
print('done')