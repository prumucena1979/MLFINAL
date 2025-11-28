import json

nb_path = r'c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb'

# Read notebook
with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)

# Full walkthrough content
full_content = """---

## **Code Walkthrough: Technical Implementation Overview**

### **1. Preprocessing**

**Data Loading:** Dataset loaded directly from UCI Repository (https://archive.ics.uci.edu/dataset/236/seeds) (fall back to local dataset if that doesn't work). `Automatic download` and extraction from ZIP file. Parsed with `delim_whitespace=True` for space-separated values. Column names assigned per requirements. `Fallback to local file` if web unavailable.

**Train-Test Split:** 80/20 with `stratify=y` for balanced classes.

**Scaling:** `StandardScaler` normalizes features to ~zero mean for faster training.

**Augmentation:** `Noise injection (σ=0.02)` on training set only to reduce overfitting.

### **2. Model Architecture**

**MLP (7→64→32→3):** Input (7 features) → Hidden1 (64) → Hidden2 (32) → Output (3 classes). `ReLU activations`, `Softmax output`. Sparse Categorical Crossentropy loss, `Adam` optimizer.

### **3. Regularization**

**Final Model:** Dropout (0.2) applied after each of the 2 hidden layers for regularization.

**Architecture:** Dense → ReLU → Dropout (repeated for the 2 hidden layers: 64 units and 32 units)

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

---
"""

# Update cell 1
nb['cells'][1]['source'] = full_content.split('\n')

# Save
with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("✅ Walkthrough completo restaurado na célula 1!")
print("\nSeções incluídas:")
print("  1. Preprocessing")
print("  2. Model Architecture")
print("  3. Regularization")
print("  4. Hyperparameters (com tiebreaker hierarchy)")
print("  5. Validation Strategy")
