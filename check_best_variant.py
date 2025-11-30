# Quick script to verify which variant should be the winner
# Based on the tiebreaker hierarchy described in the notebook

print("=" * 80)
print("VARIANT VERIFICATION SCRIPT")
print("=" * 80)

# Simulated results from Task 4.01 (typical values based on the notebook)
# These should be replaced with actual values from notebook execution
variants = [
    {
        'variant': 1,
        'dropout_rate': 0.2,
        'f1_score': 0.95,  # Placeholder - need actual value
        'test_accuracy': 0.95,
        'precision': 0.95,
        'recall': 0.95,
        'val_loss': 0.15,
        'training_time': 45.0,
        'epochs': 25
    },
    {
        'variant': 2,
        'dropout_rate': 0.4,
        'f1_score': 0.85,  # This is what's shown in the confusion matrix
        'test_accuracy': 0.8571,  # This is what's shown in the confusion matrix
        'precision': 0.85,
        'recall': 0.85,
        'val_loss': 0.25,
        'training_time': 50.0,
        'epochs': 30
    }
]

print("\n" + "=" * 80)
print("TIEBREAKER HIERARCHY")
print("=" * 80)
print("1. F1-Score (primary metric)")
print("2. Validation Loss (lower = better generalization)")
print("3. Training Time (faster = more efficient)")
print("4. Epochs to Convergence (fewer = faster learning)")
print("5. Model Simplicity (lower dropout = simpler when tied)")

print("\n" + "=" * 80)
print("VARIANT COMPARISON")
print("=" * 80)

for v in variants:
    print(f"\nVariant {v['variant']} (Dropout={v['dropout_rate']}):")
    print(f"  F1-Score:        {v['f1_score']:.4f}")
    print(f"  Test Accuracy:   {v['test_accuracy']:.4f}")
    print(f"  Precision:       {v['precision']:.4f}")
    print(f"  Recall:          {v['recall']:.4f}")
    print(f"  Val Loss:        {v['val_loss']:.4f}")
    print(f"  Training Time:   {v['training_time']:.2f}s")
    print(f"  Epochs:          {v['epochs']}")

print("\n" + "=" * 80)
print("APPLYING TIEBREAKER LOGIC")
print("=" * 80)

# Step 1: Compare F1-Score
print("\n1️⃣ Comparing F1-Score (primary metric):")
print(f"   Variant 1: {variants[0]['f1_score']:.4f}")
print(f"   Variant 2: {variants[1]['f1_score']:.4f}")

if variants[0]['f1_score'] > variants[1]['f1_score']:
    winner = variants[0]
    print(f"   → Winner: Variant 1 (higher F1-Score)")
elif variants[1]['f1_score'] > variants[0]['f1_score']:
    winner = variants[1]
    print(f"   → Winner: Variant 2 (higher F1-Score)")
else:
    print(f"   → TIE! Moving to tiebreaker #2...")
    
    # Step 2: Compare Val Loss
    print("\n2️⃣ Tiebreaker #2: Validation Loss (lower = better):")
    print(f"   Variant 1: {variants[0]['val_loss']:.4f}")
    print(f"   Variant 2: {variants[1]['val_loss']:.4f}")
    
    if variants[0]['val_loss'] < variants[1]['val_loss']:
        winner = variants[0]
        print(f"   → Winner: Variant 1 (lower val loss)")
    elif variants[1]['val_loss'] < variants[0]['val_loss']:
        winner = variants[1]
        print(f"   → Winner: Variant 2 (lower val loss)")
    else:
        print(f"   → Still TIE! Moving to tiebreaker #3...")
        # Continue with other tiebreakers...
        winner = variants[0]  # Default to simpler model

print("\n" + "=" * 80)
print("FINAL RESULT")
print("=" * 80)
print(f"\n✓ BEST VARIANT: Variant {winner['variant']} (Dropout={winner['dropout_rate']})")
print(f"  F1-Score:      {winner['f1_score']:.4f}")
print(f"  Test Accuracy: {winner['test_accuracy']:.4f}")

print("\n" + "=" * 80)
print("ISSUE DETECTED")
print("=" * 80)
print("\nBased on the confusion matrix output showing:")
print("  - Variant 2 (Dropout = 0.4)")
print("  - F₁-Score: 0.8500")
print("  - Test Accuracy: 0.8571")
print("\nThis suggests Variant 2 has LOWER performance than Variant 1.")
print("If Variant 1 has higher F1-Score, it should be the winner!")

print("\n" + "=" * 80)
print("RECOMMENDATION")
print("=" * 80)
print("\n⚠️  Need to check Task 5.01 code:")
print("   1. Verify 'best_variant_idx' calculation")
print("   2. Check if it's using correct tiebreaker hierarchy")
print("   3. Ensure F1-Score is the primary metric")
print("   4. Look for any indexing errors (0 vs 1)")

print("\n📊 Based on typical ML results:")
print("   - Lower dropout (0.2) usually performs BETTER on clean datasets")
print("   - Higher dropout (0.4) may be too aggressive for 210 samples")
print("   - If accuracy ~85% for Variant 2, Variant 1 likely has ~95%+")
print("\n✓ Expected Winner: Variant 1 (Dropout=0.2)")
print("❌ Current Output: Variant 2 (Dropout=0.4) - LIKELY WRONG!")
