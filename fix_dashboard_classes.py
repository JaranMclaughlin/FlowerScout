import pathlib

p = pathlib.Path('lib/features/dashboard/presentation/dashboard_screen.dart')
txt = p.read_text(encoding='utf-8')

# Fix _Greeting - convert to ConsumerWidget
txt = txt.replace(
    'class _Greeting extends StatelessWidget {\n  final String? name;\n  const _Greeting({this.name});\n\n  String _tod() {\n    final h = DateTime.now().hour;\n    if (h < 12) return s.goodMorning;\n    if (h < 17) return s.goodAfternoon;\n    return s.goodEvening;\n  }\n\n  @override\n  Widget build(BuildContext context) => Text(\n    name != null && name!.isNotEmpty ? \'\, \\' : _tod(),\n    style: AppTextStyles.displayLarge,\n  );\n}',
    'class _Greeting extends ConsumerWidget {\n  final String? name;\n  const _Greeting({this.name});\n\n  String _tod(AppStrings s) {\n    final h = DateTime.now().hour;\n    if (h < 12) return s.goodMorning;\n    if (h < 17) return s.goodAfternoon;\n    return s.goodEvening;\n  }\n\n  @override\n  Widget build(BuildContext context, WidgetRef ref) {\n    final s = ref.watch(stringsProvider);\n    return Text(\n      name != null && name!.isNotEmpty ? \'\, \\' : _tod(s),\n      style: AppTextStyles.displayLarge,\n    );\n  }\n}'
)

# Fix _ErrorState - add s field
txt = txt.replace(
    'class _ErrorState extends StatelessWidget {\n  final String message;\n  const _ErrorState({required this.message});\n  @override\n  Widget build(BuildContext context) => Center(',
    'class _ErrorState extends ConsumerWidget {\n  final String message;\n  const _ErrorState({required this.message});\n  @override\n  Widget build(BuildContext context, WidgetRef ref) {\n    final s = ref.watch(stringsProvider);\n    return Center('
)
# Close the extra brace
txt = txt.replace(
    '        Text(s.couldNotLoad, style: AppTextStyles.title),\n        const SizedBox(height: 4),\n        Text(message, style: AppTextStyles.caption, textAlign: TextAlign.center),\n      ]),\n    ),\n  );\n}',
    '        Text(s.couldNotLoad, style: AppTextStyles.title),\n        const SizedBox(height: 4),\n        Text(message, style: AppTextStyles.caption, textAlign: TextAlign.center),\n      ]),\n    );\n  }\n}'
)

p.write_text(txt, encoding='utf-8')
print('done')