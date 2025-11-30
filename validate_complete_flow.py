# Complete validation script - simulating actual Task 4 and Task 5 logic

import pandas as pd
import numpy as np

print("=" * 80)
print("COMPLETE VALIDATION: TASK 4.01 → TASK 5.01 FLOW")
print("=" * 80)

# Simulate Task 4.01 results (these would come from actual training)
print("\n" + "=" * 80)
print("TASK 4.01: Hyperparameter Comparison Results")
print("=" * 80)

results_task4 = [
    {
        'dropout_rate': 0.2,
        'test_accuracy': 0.9762,  # Higher is better
        'precision': 0.9767,
        'recall': 0.9762,
        'f1_score': 0.9762,  # This should be the winner
        'train_accuracy': 0.9850,
        'val_accuracy': 0.9800,
        'overfitting_gap': 0.0050,
        'epochs_trained': 28,
        'training_time': 42.5
    },
    {
        'dropout_rate': 0.4,
        'test_accuracy': 0.8571,  # Lower (what we see in confusion matrix)
        'precision': 0.8600,
        'recall': 0.8571,
        'f1_score': 0.8500,  # Lower F1-Score
        'train_accuracy': 0.8700,
        'val_accuracy': 0.8650,
        'overfitting_gap': 0.0050,
        'epochs_trained': 35,
        'training_time': 48.2
    }
]

results_df = pd.DataFrame(results_task4)
print("\nTask 4.01 Results:")
print(results_df[['dropout_rate', 'test_accuracy', 'f1_score']].to_string(index=False))

best_f1_idx = results_df['f1_score'].idxmax()
print(f"\nBest F1-Score: Index={best_f1_idx}, Dropout={results_df.loc[best_f1_idx, 'dropout_rate']}")

# Simulate Task 5.01 - retraining both variants
print("\n" + "=" * 80)
print("TASK 5.01: Re-evaluating Both Variants on Test Set")
print("=" * 80)

evaluation_results = []

for idx, dropout_rate in enumerate([0.2, 0.4], 1):
    print(f"\nVariant {idx} (Dropout={dropout_rate})")
    
    # In Task 5.01, models are retrained, so results might differ slightly
    # But Variant 1 should still be better
    if dropout_rate == 0.2:
        # Variant 1 - better performance
        result = {
            'variant': 1,
            'dropout_rate': 0.2,
            'accuracy': 0.9762,
            'precision': 0.9767,
            'recall': 0.9762,
            'f1_score': 0.9762,
            'training_time': 41.8,
            'val_loss': 0.0850,
            'epochs': 26,
            'model': f'model_dropout_{dropout_rate}',
            'predictions': np.array([0, 1, 2] * 14)  # Dummy predictions
        }
    else:
        # Variant 2 - worse performance (what we see in output)
        result = {
            'variant': 2,
            'dropout_rate': 0.4,
            'accuracy': 0.8571,
            'precision': 0.8600,
            'recall': 0.8571,
            'f1_score': 0.8500,  # This is what's shown in confusion matrix!
            'training_time': 47.5,
            'val_loss': 0.1250,
            'epochs': 33,
            'model': f'model_dropout_{dropout_rate}',
            'predictions': np.array([0, 1, 2] * 14)
        }
    
    evaluation_results.append(result)
    print(f"  F1-Score: {result['f1_score']:.4f}")
    print(f"  Accuracy: {result['accuracy']:.4f}")

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

print("\n" + "=" * 80)
print("Task 5.01 Comparison Table:")
print("=" * 80)
print(eval_df.to_string(index=False))

# Selection logic (as in notebook)
print("\n" + "=" * 80)
print("SELECTING BEST VARIANT")
print("=" * 80)

best_f1 = eval_df['F1_Score'].max()
candidates = eval_df[eval_df['F1_Score'] == best_f1]

print(f"\nPrimary criterion: F1-Score = {best_f1:.4f}")
print(f"Candidates: Variant {list(candidates['Variant'].values)}")

# Get winning variant number
winning_variant_number = int(candidates.iloc[0]['Variant'])
print(f"\nWinning Variant Number from DataFrame: {winning_variant_number}")

# CRITICAL: Map to evaluation_results list (0-indexed)
list_index = winning_variant_number - 1
print(f"Corresponding index in evaluation_results list: {list_index}")

best_variant = evaluation_results[list_index]

print("\n" + "=" * 80)
print("FINAL RESULT")
print("=" * 80)
print(f"✓ Best Variant: {best_variant['variant']}")
print(f"  Dropout Rate: {best_variant['dropout_rate']}")
print(f"  F1-Score: {best_variant['f1_score']:.4f}")
print(f"  Accuracy: {best_variant['accuracy']:.4f}")

# Verify against what's shown in confusion matrix
print("\n" + "=" * 80)
print("VERIFICATION AGAINST CONFUSION MATRIX OUTPUT")
print("=" * 80)
print("\nConfusion Matrix shows:")
print("  Variant: 2")
print("  Dropout: 0.4")
print("  F1-Score: 0.8500")
print("  Accuracy: 0.8571")

if best_variant['variant'] == 2:
    print("\n❌ PROBLEM CONFIRMED!")
    print("   The code is selecting Variant 2 (worse performance)")
    print("   Expected: Variant 1 (F1=0.9762)")
    print("   Actual: Variant 2 (F1=0.8500)")
    print("\n🔍 Issue: Check if Task 4.01 actually stored wrong results")
    print("   OR if Task 5.01 is using wrong index mapping")
else:
    print("\n✓ CORRECT!")
    print(f"   Best variant is {best_variant['variant']} as expected")

# Debug the indexing
print("\n" + "=" * 80)
print("DEBUG: Index Mapping")
print("=" * 80)
print("evaluation_results list:")
for i, res in enumerate(evaluation_results):
    print(f"  Index {i}: Variant {res['variant']}, Dropout {res['dropout_rate']}, F1={res['f1_score']:.4f}")

print("\nDataFrame candidates:")
print(candidates[['Variant', 'Dropout_Rate', 'F1_Score']])
print(f"\ncandidates.iloc[0]['Variant'] = {candidates.iloc[0]['Variant']}")
print(f"winning_variant_number = {winning_variant_number}")
print(f"list_index (winning_variant_number - 1) = {list_index}")
print(f"\nevaluation_results[{list_index}] gives us:")
print(f"  Variant: {evaluation_results[list_index]['variant']}")
print(f"  Dropout: {evaluation_results[list_index]['dropout_rate']}")
print(f"  F1-Score: {evaluation_results[list_index]['f1_score']:.4f}")
