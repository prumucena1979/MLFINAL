import json

nb_path = r'c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb'

# Read notebook
with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)

# Find the cell with "### **4. Hyperparameters**"
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown':
        source = ''.join(cell['source'])
        if '### **4. Hyperparameters**' in source:
            print(f"Found cell {i}")
            print(f"Cell ID: {cell.get('id', 'NO ID')}")
            print("\nCurrent content:")
            print(source)
            
            # Update the content
            new_source = """
Early Stopping (patience=15) prevents overfitting by monitoring validation loss.

### **4. Hyperparameters**

**Dropout Testing:** 0.2 (light) vs 0.4 (strong) to find optimal regularization.

**Selection Criteria (Tiebreaker Hierarchy):**
1. **F1-Score** (primary metric)
2. **Validation Loss** (lower = better generalization)
3. **Training Time** (faster = more efficient)
4. **Epochs to Convergence** (fewer = faster learning)
5. **Model Simplicity** (lower dropout = simpler when tied)

**Training:** 100 epochs, batch size 16, 20% validation split.

### **5. Validation Strategy**

**K-Fold Cross-Validation (K=5):** Uses all 378 samples for robust performance estimation. Provides confidence intervals and reduces bias from single train/test split.

**Final Performance:** Mean Accuracy: 97.62% ± 0.53% (highly stable model)
"""
            
            nb['cells'][i]['source'] = new_source.split('\n')
            
            # Save
            with open(nb_path, 'w', encoding='utf-8') as f:
                json.dump(nb, f, indent=1, ensure_ascii=False)
            
            print("\n✅ Updated successfully!")
            print("\nNew content:")
            print(new_source)
            break
