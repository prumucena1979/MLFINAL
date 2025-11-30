"""Find where AUGMENTATION_FACTOR = 19 is defined"""
import json

filepath = r"c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb"

with open(filepath, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb.get('cells', [])

# Find cells with AUGMENTATION_FACTOR = 19
for idx, cell in enumerate(cells):
    source = cell.get('source', [])
    if isinstance(source, list):
        source_text = ''.join(source)
    else:
        source_text = source
    
    if 'AUGMENTATION_FACTOR = 1' in source_text:
        print(f"Found AUGMENTATION_FACTOR definition in Cell {idx + 1}:")
        print("="*80)
        # Print first 1500 chars
        print(source_text[:1500])
        if len(source_text) > 1500:
            print(f"\n... (truncated, total length: {len(source_text)} chars)")
        print("\n" + "="*80)
