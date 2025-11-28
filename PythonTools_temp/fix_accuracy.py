import json

nb_path = r'c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb'

# Read notebook
with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)

# Find and update cell 1 (walkthrough)
for i, cell in enumerate(nb['cells']):
    if cell.get('id') == '600df8d5':
        source = ''.join(cell['source'])
        
        # Replace the incorrect value
        new_source = source.replace(
            'Mean Accuracy: 97.62% ± 0.53%',
            'Mean Accuracy: 99.81% ± 0.15%'
        )
        
        nb['cells'][i]['source'] = new_source.split('\n')
        
        # Save
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
        
        print("✅ Acurácia corrigida no walkthrough!")
        print("\nAlteração:")
        print("  ❌ Errado: Mean Accuracy: 97.62% ± 0.53%")
        print("  ✅ Correto: Mean Accuracy: 99.81% ± 0.15%")
        break
