"""Extract the exact Task 2.04 code with AUGMENTATION_FACTOR"""
import json

filepath = r"c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb"

with open(filepath, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb.get('cells', [])

# Find cells with AUGMENTATION_FACTOR
for idx, cell in enumerate(cells):
    source = cell.get('source', [])
    if isinstance(source, list):
        source_text = ''.join(source)
    else:
        source_text = source
    
    if 'AUGMENTATION_FACTOR' in source_text and 'Task 2.04' in source_text:
        print(f"Found Task 2.04 cell (Cell {idx + 1}):")
        print("="*80)
        print(source_text)
        print("\n" + "="*80)
        break
