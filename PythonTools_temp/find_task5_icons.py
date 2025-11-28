import json

nb_path = r'c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb'

with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)

# Find cells around Task 5.01
task_5_cells = []
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell['source'])
    if 'Task 5.01' in source or 'TASK 5.01' in source:
        task_5_cells.append(i)

print("Cells containing Task 5.01:")
for cell_num in task_5_cells:
    print(f"Cell {cell_num}")
    source = ''.join(nb['cells'][cell_num]['source'])
    # Check for any unicode symbols that might be icons
    import re
    # Find any non-ASCII characters
    non_ascii = re.findall(r'[^\x00-\x7F]', source)
    if non_ascii:
        unique = list(set(non_ascii))
        print(f"  Non-ASCII chars found: {unique}")
        # Show context
        for char in unique[:5]:
            idx = source.find(char)
            context = source[max(0, idx-20):idx+30]
            print(f"    '{char}': ...{context}...")
