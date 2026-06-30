import pathlib

# Check OfflineSyncService
osp = pathlib.Path('lib/core/offline/offline_sync_service.dart')
print("=== offline_sync_service.dart ===")
print(osp.read_text(encoding='utf-8') if osp.exists() else "FILE NOT FOUND")

# Check locale key in browser storage vs what initLocale reads
lp = pathlib.Path('lib/shared/providers/locale_provider.dart')
print("\n=== locale_provider.dart ===")
print(lp.read_text(encoding='utf-8'))