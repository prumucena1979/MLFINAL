import json

nb_path = r'c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb'

with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)

# Replace subscript characters
replacements = {
    '₁': '1',
    '₂': '2',
    '₃': '3',
    '₄': '4',
    '₅': '5',
    'F₁': 'F1',
}

cells_modified = []

for i, cell in enumerate(nb['cells']):
    source = ''.join(cell['source'])
    original = source
    
    # Replace subscripts
    for old, new in replacements.items():
        source = source.replace(old, new)
    
    if source != original:
        nb['cells'][i]['source'] = source.split('\n')
        cells_modified.append(i)

# Save
with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("="*80)
print("REMOVING SUBSCRIPT CHARACTERS")
print("="*80)
print(f"\nCells modified: {len(cells_modified)}")
print(f"Cell numbers: {cells_modified}")
print("\nReplacements:")
print("  F₁-Score -> F1-Score")
print("  All subscript numbers converted to regular numbers")
