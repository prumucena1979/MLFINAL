"""Find and extract the problematic lines"""
import json

filepath = r"c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb"

with open(filepath, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb.get('cells', [])

for idx, cell in enumerate(cells):
    source = cell.get('source', [])
    if isinstance(source, list):
        source_text = ''.join(source)
    else:
        source_text = source
    
    if '")print("\\n[TASK 4.01 COMPLETED]' in source_text or '")print("\\n[TASK 5.01 COMPLETED]' in source_text:
        print(f"Found issue in Cell {idx + 1} ({cell['cell_type']}):")
        print("="*80)
        # Find the problematic line
        lines = source_text.split('\n')
        for line_num, line in enumerate(lines, 1):
            if '")print("' in line:
                print(f"Line {line_num}: {line}")
                print("\nContext:")
                start = max(0, line_num - 3)
                end = min(len(lines), line_num + 2)
                for i in range(start, end):
                    marker = ">>> " if i == line_num - 1 else "    "
                    print(f"{marker}{i+1}: {lines[i]}")
                print("\n" + "="*80)
