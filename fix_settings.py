import pathlib, re

p = pathlib.Path('lib/features/settings/presentation/settings_screen.dart')
text = p.read_text(encoding='utf-8')

# 1. Restore this. in constructors (the regex stripped it from required params)
text = text.replace(
    "  const _LoadingCard({required message});",
    "  const _LoadingCard({required this.message});"
)
text = text.replace(
    "  const _ErrorCard({required message, required onRetry});",
    "  const _ErrorCard({required this.message, required this.onRetry});"
)
text = text.replace(
    "  const _EmptyCard({required message});",
    "  const _EmptyCard({required this.message});"
)

# 2. Remove the wrongly added mounted guard (context.mounted already guards line 944)
text = text.replace(
    "      if (!mounted) return;\n      ScaffoldMessenger.of(context).showSnackBar(SnackBar(\n",
    "      ScaffoldMessenger.of(context).showSnackBar(SnackBar(\n"
)

# 3. use_build_context_synchronously line 944 — wrap Navigator call with mounted check on state
text = text.replace(
    "            if (context.mounted) {\n              Navigator.of(context).pushAndRemoveUntil(",
    "            if (mounted) {\n              Navigator.of(context).pushAndRemoveUntil("
)

p.write_text(text, encoding='utf-8')
print("settings_screen.dart restored.")