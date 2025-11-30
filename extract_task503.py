"""Extract Task 5.03 code to see variable definitions"""
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
    
    if '# TASK 5.03:' in source_text:
        print(f"Task 5.03 Cell {idx + 1}:")
        print("="*80)
        print(source_text[:2000])
        if len(source_text) > 2000:
            print(f"\n... (showing first 2000 chars, total: {len(source_text)})")
        print("\n" + "="*80)
        break
