import pathlib

mobile = pathlib.Path('lib')
for p in mobile.rglob('*.dart'):
    text = p.read_text(encoding='utf-8', errors='ignore')
    if 'supabase' in text.lower() and ('insert' in text or 'upsert' in text) and 'finding' in text.lower():
        print(f"\n=== {p} ===")
        for i, line in enumerate(text.split('\n'), 1):
            if any(x in line.lower() for x in ['insert', 'upsert', 'submit', 'finding', 'queue']):
                print(f"  {i}: {line}")