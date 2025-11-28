import json

nb_path = r'c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb'

with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)

# Get cell 30 id
cell30_id = nb['cells'][30].get('id', 'NO ID')
print(f"Cell 30 ID: {cell30_id}")

# Show first few cell IDs
for i in range(28, 33):
    cell = nb['cells'][i]
    cell_id = cell.get('id', 'NO ID')
    source_preview = ''.join(cell['source'])[:60]
    print(f"Cell {i}: ID={cell_id}, Type={cell['cell_type']}, Content={source_preview}")
