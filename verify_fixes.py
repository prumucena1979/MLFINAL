"""
Quick verification that all fixes were applied correctly
"""

def verify_fixes():
    notebook_path = r"c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb"
    
    with open(notebook_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("="*80)
    print("VERIFICATION: CHECKING ALL FIXES")
    print("="*80)
    
    checks = {
        "✓ Removed premature winner claim": "the ends up being our choice" not in content,
        "✓ Added 'automatically selected' text": "automatically selected based on" in content,
        "✓ Random seeds in Task 4.01": content.count("# Set random seeds for reproducibility") >= 2,
        "✓ Random seeds in Task 5.01": "# Set random seeds for reproducibility" in content,
        "✓ Neutral conclusion text": "dropout regularization" in content and "dropout = 0.2" not in content.split("dropout regularization")[0][-100:],
        "✓ Selection criteria updated": "The best performing variant is automatically selected" in content
    }
    
    print("\nFix Verification:")
    all_passed = True
    for check_name, passed in checks.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {check_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*80)
    if all_passed:
        print("✓ ALL FIXES VERIFIED SUCCESSFULLY")
        print("\n📋 NEXT STEP: Restart kernel and re-run all cells")
        print("   Expected: Variant 1 (dropout=0.2) should win consistently")
    else:
        print("✗ SOME FIXES MAY NOT HAVE APPLIED CORRECTLY")
        print("   Please review the fixes manually")
    print("="*80)

if __name__ == "__main__":
    verify_fixes()
