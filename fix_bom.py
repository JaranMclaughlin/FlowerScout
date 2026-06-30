import pathlib

p = pathlib.Path('.env')
text = p.read_text(encoding='utf-8-sig')  # utf-8-sig strips BOM automatically
p.write_text(text, encoding='utf-8')      # write back without BOM
print("BOM removed from .env")

# Verify
raw = p.read_bytes()[:3]
print(f"First 3 bytes: {raw} — {'BOM still present!' if raw == b'\\xef\\xbb\\xbf' else 'Clean'}")