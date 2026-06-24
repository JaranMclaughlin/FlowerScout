import pathlib

p = pathlib.Path('lib/features/reports/presentation/reports_screen.dart')
lines = p.read_text(encoding='utf-8').splitlines(keepends=True)

start = next(i for i, l in enumerate(lines) if l.strip() == '// Table header')
end_marker = next(i for i, l in enumerate(lines) if 'Widget _buildTableRows' in l)

j = end_marker - 1
while lines[j].strip() in ('', '}', ');'):
    j -= 1
old_block_end = j

replacement = "          _buildTableRows(rows),\n"
new_lines = lines[:start] + [replacement] + lines[old_block_end:]

p.write_text(''.join(new_lines), encoding='utf-8')
print(f"Removed lines {start+1}-{old_block_end} (1-indexed), inserted helper call.")