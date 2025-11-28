import json

nb_path = r'c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb'

with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)

print("="*80)
print("PROCURANDO CONFUSION MATRIX")
print("="*80)

for i, cell in enumerate(nb['cells']):
    source = ''.join(cell.get('source', []))
    
    if 'confusion_matrix' in source.lower():
        print(f"\n{'='*80}")
        print(f"CELL {i} (ID: {cell.get('id', 'no-id')})")
        print(f"{'='*80}")
        print(source[:500])
        print("...")
