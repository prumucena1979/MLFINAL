import json

nb_path = r'c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb'

with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)

# Replace the checkmark emoji
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell['source'])
    
    if '✅ BEST PERFORMING VARIANT' in source:
        source = source.replace('✅ BEST PERFORMING VARIANT', '[BEST] BEST PERFORMING VARIANT')
        nb['cells'][i]['source'] = source.split('\n')
        print(f"Fixed cell {i}: Removed checkmark emoji")

# Save
with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("\n✓ Checkmark emoji removed")
print("  ✅ -> [BEST]")
