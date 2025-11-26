import json

# Read the notebook
with open('MLfinalAssignment_NF1002000.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Clear all outputs
for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        cell['outputs'] = []
        cell['execution_count'] = None

# Save the cleaned notebook
with open('MLfinalAssignment_NF1002000.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("Notebook cleaned successfully!")
print("All cell outputs have been removed.")
