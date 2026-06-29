import pathlib

p = pathlib.Path('lib/features/dashboard/presentation/dashboard_screen.dart')
txt = p.read_text(encoding='utf-8')

old_greeting = """class _Greeting extends StatelessWidget {
  final String? name;
  const _Greeting({this.name});

  String _tod() {
    final h = DateTime.now().hour;
    if (h < 12) return s.goodMorning;
    if (h < 17) return s.goodAfternoon;
    return s.goodEvening;
  }

  @override
  Widget build(BuildContext context) => Text(
    name != null && name!.isNotEmpty ? '${_tod()}, $name' : _tod(),
    style: AppTextStyles.displayLarge,
  );
}"""

new_greeting = """class _Greeting extends ConsumerWidget {
  final String? name;
  const _Greeting({this.name});

  String _tod(AppStrings s) {
    final h = DateTime.now().hour;
    if (h < 12) return s.goodMorning;
    if (h < 17) return s.goodAfternoon;
    return s.goodEvening;
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = ref.watch(stringsProvider);
    return Text(
      name != null && name!.isNotEmpty ? '${_tod(s)}, $name' : _tod(s),
      style: AppTextStyles.displayLarge,
    );
  }
}"""

old_error = """class _ErrorState extends StatelessWidget {
  final String message;
  const _ErrorState({required this.message});
  @override
  Widget build(BuildContext context) => Center(
    child: Padding(padding: const EdgeInsets.all(24),
      child: Column(mainAxisSize: MainAxisSize.min, children: [
        const Icon(Icons.error_outline_rounded, size: 40, color: AppColors.critical),
        const SizedBox(height: AppSizes.spaceMd),
        Text(s.couldNotLoad, style: AppTextStyles.title),
        const SizedBox(height: 4),
        Text(message, style: AppTextStyles.caption, textAlign: TextAlign.center),
      ]),
    ),
  );
}"""

new_error = """class _ErrorState extends ConsumerWidget {
  final String message;
  const _ErrorState({required this.message});
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = ref.watch(stringsProvider);
    return Center(
      child: Padding(padding: const EdgeInsets.all(24),
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          const Icon(Icons.error_outline_rounded, size: 40, color: AppColors.critical),
          const SizedBox(height: AppSizes.spaceMd),
          Text(s.couldNotLoad, style: AppTextStyles.title),
          const SizedBox(height: 4),
          Text(message, style: AppTextStyles.caption, textAlign: TextAlign.center),
        ]),
      ),
    );
  }
}"""

txt = txt.replace(old_greeting, new_greeting)
txt = txt.replace(old_error, new_error)
p.write_text(txt, encoding='utf-8')
print('done')