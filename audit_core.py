import pathlib

files = [
    'lib/core/offline/pending_finding.dart',
    'lib/shared/trail/data/trail_repository.dart',
    'lib/shared/providers/farm_repository.dart',
    'lib/shared/providers/farm_providers.dart',
    'lib/shared/widgets/app_shell.dart',
    'lib/core/session/user_session.dart',
]

for f in files:
    p = pathlib.Path(f)
    print(f"\n{"="*60}")
    print(f"=== {f} ===")
    print("="*60)
    print(p.read_text(encoding="utf-8"))