import json

nb_path = r'c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb'

# Read notebook
with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)

# Show first 3 cells
for i in range(min(3, len(nb['cells']))):
    cell = nb['cells'][i]
    print(f"\n{'='*80}")
    print(f"Cell {i}: {cell['cell_type']}, ID: {cell.get('id', 'NO ID')}")
    print('='*80)
    source = ''.join(cell['source'])[:200]
    print(source)
