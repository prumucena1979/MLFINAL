import json

nb_path = r'c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb'

# Read notebook
with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)

# New cell 30 code
new_code = """# TASK 5.01: Evaluate Both Variants on Test Set

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report
import time

print("=" * 80)
print("TASK 5.01: FINAL EVALUATION - BOTH VARIANTS ON TEST SET")
print("=" * 80)

# Define dropout rates if not already defined
if 'dropout_rates' not in locals():
    dropout_rates = [0.2, 0.4]

# Store models for evaluation
trained_models = []

# Retrain both variants to save the models
print("\\nRetraining both variants for final evaluation...")
print("=" * 80)

for idx, dropout_rate in enumerate(dropout_rates, 1):
    print(f"\\nTraining Variant {idx} (dropout={dropout_rate})...")

    # Build model
    final_model = models.Sequential([
        layers.Input(shape=(7,), name='input_layer'),
        layers.Dense(64, activation='relu', name='hidden_layer_1'),
        layers.Dropout(dropout_rate, name='dropout_1'),
        layers.Dense(32, activation='relu', name='hidden_layer_2'),
        layers.Dropout(dropout_rate, name='dropout_2'),
        layers.Dense(3, activation='softmax', name='output_layer')
    ], name=f'Final_MLP_Dropout_{dropout_rate}')

    # Compile model
    final_model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    # Train model with time tracking
    early_stopping_final = EarlyStopping(
        monitor='val_loss',
        patience=15,
        restore_best_weights=True,
        verbose=0
    )

    # Start timing
    start_time = time.time()
    
    history = final_model.fit(
        X_train_scaled,
        y_train_adj,
        epochs=100,
        batch_size=16,
        validation_split=0.2,
        callbacks=[early_stopping_final],
        verbose=0
    )
    
    # End timing
    training_time = time.time() - start_time
    
    # Get final validation loss and epochs trained
    final_val_loss = min(history.history['val_loss'])
    epochs_trained = len(history.history['val_loss'])

    trained_models.append({
        'variant': idx,
        'dropout_rate': dropout_rate,
        'model': final_model,
        'training_time': training_time,
        'val_loss': final_val_loss,
        'epochs': epochs_trained
    })

    print(f"[COMPLETED] Variant {idx} - Time: {training_time:.2f}s, Epochs: {epochs_trained}, Val Loss: {final_val_loss:.4f}")

print("\\n" + "=" * 80)
print("EVALUATING BOTH VARIANTS ON TEST SET")
print("=" * 80)

evaluation_results = []

for model_info in trained_models:
    variant = model_info['variant']
    dropout_rate = model_info['dropout_rate']
    model = model_info['model']
    training_time = model_info['training_time']
    val_loss = model_info['val_loss']
    epochs = model_info['epochs']

    print(f"\\n{'='*80}")
    print(f"VARIANT {variant}: DROPOUT RATE = {dropout_rate}")
    print(f"{'='*80}")

    # Get predictions
    y_pred_probs = model.predict(X_test_scaled, verbose=0)
    y_pred = np.argmax(y_pred_probs, axis=1)

    # Calculate metrics
    accuracy = accuracy_score(y_test_adj, y_pred)
    precision_weighted = precision_score(y_test_adj, y_pred, average='weighted', zero_division=0)
    recall_weighted = recall_score(y_test_adj, y_pred, average='weighted', zero_division=0)
    f1_weighted = f1_score(y_test_adj, y_pred, average='weighted', zero_division=0)

    # Per-class metrics
    precision_per_class = precision_score(y_test_adj, y_pred, average=None, zero_division=0)
    recall_per_class = recall_score(y_test_adj, y_pred, average=None, zero_division=0)
    f1_per_class = f1_score(y_test_adj, y_pred, average=None, zero_division=0)

    # Display results
    print(f"\\nOverall Metrics:")
    print(f"  Accuracy:  {accuracy:.4f}")
    print(f"  Precision: {precision_weighted:.4f} (weighted)")
    print(f"  Recall:    {recall_weighted:.4f} (weighted)")
    print(f"  F₁-Score:  {f1_weighted:.4f} (weighted)")

    print(f"\\nPer-Class Metrics:")
    for class_idx in range(3):
        print(f"  Class {class_idx} (Wheat Type {class_idx+1}):")
        print(f"    Precision: {precision_per_class[class_idx]:.4f}")
        print(f"    Recall:    {recall_per_class[class_idx]:.4f}")
        print(f"    F₁-Score:  {f1_per_class[class_idx]:.4f}")

    # Store results
    evaluation_results.append({
        'variant': variant,
        'dropout_rate': dropout_rate,
        'accuracy': accuracy,
        'precision': precision_weighted,
        'recall': recall_weighted,
        'f1_score': f1_weighted,
        'training_time': training_time,
        'val_loss': val_loss,
        'epochs': epochs,
        'model': model,
        'predictions': y_pred
    })

# Create comparison DataFrame
eval_df = pd.DataFrame([{
    'Variant': r['variant'],
    'Dropout_Rate': r['dropout_rate'],
    'Accuracy': r['accuracy'],
    'Precision': r['precision'],
    'Recall': r['recall'],
    'F1_Score': r['f1_score'],
    'Training_Time_s': r['training_time'],
    'Val_Loss': r['val_loss'],
    'Epochs': r['epochs']
} for r in evaluation_results])

print("\\n" + "=" * 80)
print("COMPARISON TABLE - BOTH VARIANTS")
print("=" * 80)
print(eval_df.to_string(index=False))

# Identify best variant with tiebreaker logic
print("\\n" + "=" * 80)
print("SELECTING BEST VARIANT (WITH TIEBREAKER CRITERIA)")
print("=" * 80)

# Primary: F1-Score
best_f1 = eval_df['F1_Score'].max()
candidates = eval_df[eval_df['F1_Score'] == best_f1]

print(f"\\nPrimary criterion: F1-Score = {best_f1:.4f}")
print(f"Candidates with best F1-Score: {list(candidates['Variant'].values)}")

if len(candidates) > 1:
    print("\\n🔄 TIE DETECTED! Applying tiebreaker criteria...")
    
    # Tiebreaker 1: Validation Loss (lower is better)
    print(f"\\n1️⃣ Tiebreaker #1: Validation Loss (lower = better)")
    for _, row in candidates.iterrows():
        print(f"   Variant {row['Variant']}: {row['Val_Loss']:.4f}")
    
    best_val_loss = candidates['Val_Loss'].min()
    candidates = candidates[candidates['Val_Loss'] == best_val_loss]
    print(f"   → Best Val Loss: {best_val_loss:.4f} (Candidates: {list(candidates['Variant'].values)})")
    
    if len(candidates) > 1:
        # Tiebreaker 2: Training Time (faster is better)
        print(f"\\n2️⃣ Tiebreaker #2: Training Time (faster = better)")
        for _, row in candidates.iterrows():
            print(f"   Variant {row['Variant']}: {row['Training_Time_s']:.2f}s")
        
        best_time = candidates['Training_Time_s'].min()
        candidates = candidates[candidates['Training_Time_s'] == best_time]
        print(f"   → Fastest: {best_time:.2f}s (Candidates: {list(candidates['Variant'].values)})")
        
        if len(candidates) > 1:
            # Tiebreaker 3: Epochs (fewer = faster convergence)
            print(f"\\n3️⃣ Tiebreaker #3: Epochs to Convergence (fewer = better)")
            for _, row in candidates.iterrows():
                print(f"   Variant {row['Variant']}: {row['Epochs']} epochs")
            
            best_epochs = candidates['Epochs'].min()
            candidates = candidates[candidates['Epochs'] == best_epochs]
            print(f"   → Fewest epochs: {best_epochs} (Candidates: {list(candidates['Variant'].values)})")
            
            if len(candidates) > 1:
                # Tiebreaker 4: Simpler model (lower dropout = less regularization)
                print(f"\\n4️⃣ Tiebreaker #4: Model Simplicity (lower dropout = simpler)")
                for _, row in candidates.iterrows():
                    print(f"   Variant {row['Variant']}: Dropout {row['Dropout_Rate']}")
                
                candidates = candidates[candidates['Dropout_Rate'] == candidates['Dropout_Rate'].min()]
                print(f"   → Simplest model: Dropout {candidates.iloc[0]['Dropout_Rate']} (Variant {candidates.iloc[0]['Variant']})")

best_variant_idx = candidates.index[0]
best_variant = evaluation_results[best_variant_idx]

print("\\n" + "=" * 80)
print("✅ BEST PERFORMING VARIANT")
print("=" * 80)
print(f"Variant {best_variant['variant']} with Dropout Rate = {best_variant['dropout_rate']}")
print(f"  Accuracy:       {best_variant['accuracy']:.4f}")
print(f"  Precision:      {best_variant['precision']:.4f}")
print(f"  Recall:         {best_variant['recall']:.4f}")
print(f"  F₁-Score:       {best_variant['f1_score']:.4f}")
print(f"  Training Time:  {best_variant['training_time']:.2f}s")
print(f"  Val Loss:       {best_variant['val_loss']:.4f}")
print(f"  Epochs:         {best_variant['epochs']}")

print("\\n[TASK 5.01 COMPLETED] Both variants evaluated on test set")
"""

# Replace cell 30 source
nb['cells'][30]['source'] = new_code.split('\n')

# Save notebook
with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("✅ Cell 30 updated successfully with tiebreaker logic!")
print("\nChanges:")
print("  - Added import time")
print("  - Captured training_time for each variant")
print("  - Captured val_loss and epochs from history")
print("  - Added Training_Time_s, Val_Loss, Epochs to comparison table")
print("  - Implemented 4-level tiebreaker hierarchy:")
print("    1. F1-Score (primary)")
print("    2. Validation Loss (lower = better)")
print("    3. Training Time (faster = better)")
print("    4. Epochs (fewer = better)")
print("    5. Model Simplicity (lower dropout = simpler)")
