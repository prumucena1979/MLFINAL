"""
Deep analysis - Check actual execution outputs for winner consistency
"""

import json
import re

def deep_analysis(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    cells = nb.get('cells', [])
    
    print("=" * 80)
    print("DEEP ANALYSIS: CHECKING ACTUAL EXECUTION OUTPUTS")
    print("=" * 80)
    
    task_401_results = {}
    task_501_results = {}
    task_503_results = {}
    
    for idx, cell in enumerate(cells):
        cell_num = idx + 1
        
        source = cell.get('source', [])
        if isinstance(source, list):
            source_text = ''.join(source)
        else:
            source_text = source
        
        outputs = []
        if 'outputs' in cell:
            for output in cell['outputs']:
                if 'text' in output:
                    if isinstance(output['text'], list):
                        outputs.append(''.join(output['text']))
                    else:
                        outputs.append(output['text'])
        output_text = '\n'.join(outputs)
        
        # Task 4.01
        if 'TASK 4.01' in source_text and output_text:
            print(f"\n{'='*80}")
            print(f"TASK 4.01 - Cell {cell_num}")
            print(f"{'='*80}")
            
            # Extract test accuracy and F1 scores
            variant_1_f1 = re.search(r'Variant 1.*?F1.*?Score.*?(0\.\d+)', output_text, re.DOTALL | re.IGNORECASE)
            variant_2_f1 = re.search(r'Variant 2.*?F1.*?Score.*?(0\.\d+)', output_text, re.DOTALL | re.IGNORECASE)
            
            # Look for winner indication
            winner_lines = [line for line in output_text.split('\n') if '✓' in line and 'Variant' in line]
            
            if winner_lines:
                print("\nWinner indications found:")
                for line in winner_lines[:5]:  # First 5 lines with checkmarks
                    print(f"  {line}")
                
                # Determine winner from checkmarks
                v1_wins = sum(1 for line in winner_lines if 'Variant 1' in line)
                v2_wins = sum(1 for line in winner_lines if 'Variant 2' in line)
                
                if v1_wins > v2_wins:
                    task_401_results['winner'] = 1
                    print("\n→ Task 4.01 Winner: Variant 1")
                elif v2_wins > v1_wins:
                    task_401_results['winner'] = 2
                    print("\n→ Task 4.01 Winner: Variant 2")
            
            if variant_1_f1:
                task_401_results['variant_1_f1'] = float(variant_1_f1.group(1))
                print(f"  Variant 1 F1-Score: {task_401_results['variant_1_f1']}")
            if variant_2_f1:
                task_401_results['variant_2_f1'] = float(variant_2_f1.group(1))
                print(f"  Variant 2 F1-Score: {task_401_results['variant_2_f1']}")
        
        # Task 5.01
        if 'TASK 5.01' in source_text and output_text:
            print(f"\n{'='*80}")
            print(f"TASK 5.01 - Cell {cell_num}")
            print(f"{'='*80}")
            
            # Look for best variant selection
            best_variant = re.search(r'(?:BEST|Best)\s+(?:PERFORMING\s+)?VARIANT.*?(?:Variant\s+)?(\d+)', output_text, re.IGNORECASE)
            dropout_match = re.search(r'Dropout.*?(?:Rate|rate).*?=.*?(0\.\d+)', output_text)
            f1_match = re.search(r'F[₁1].*?Score.*?(0\.\d+)', output_text)
            
            if best_variant:
                task_501_results['winner'] = int(best_variant.group(1))
                print(f"\n→ Task 5.01 Winner: Variant {task_501_results['winner']}")
            
            if dropout_match:
                task_501_results['dropout'] = float(dropout_match.group(1))
                print(f"  Dropout Rate: {task_501_results['dropout']}")
            
            if f1_match:
                task_501_results['f1'] = float(f1_match.group(1))
                print(f"  F1-Score: {task_501_results['f1']}")
        
        # Task 5.03
        if 'TASK 5.03' in source_text and output_text:
            print(f"\n{'='*80}")
            print(f"TASK 5.03 - Cell {cell_num} (Confusion Matrix)")
            print(f"{'='*80}")
            
            # Extract variant, dropout, F1, accuracy
            variant_match = re.search(r'(?:Best\s+)?Variant:?\s*(\d+)', output_text)
            dropout_match = re.search(r'Dropout.*?(?:Rate)?.*?=.*?(0\.\d+)', output_text)
            f1_match = re.search(r'F[₁1].*?Score.*?(0\.\d+)', output_text)
            acc_match = re.search(r'(?:Test\s+)?Accuracy.*?(0\.\d+)', output_text)
            
            if variant_match:
                task_503_results['variant'] = int(variant_match.group(1))
                print(f"\n→ Confusion Matrix Variant: {task_503_results['variant']}")
            
            if dropout_match:
                task_503_results['dropout'] = float(dropout_match.group(1))
                print(f"  Dropout Rate: {task_503_results['dropout']}")
            
            if f1_match:
                task_503_results['f1'] = float(f1_match.group(1))
                print(f"  F1-Score: {task_503_results['f1']}")
            
            if acc_match:
                task_503_results['accuracy'] = float(acc_match.group(1))
                print(f"  Accuracy: {task_503_results['accuracy']}")
    
    # Final consistency check
    print(f"\n{'='*80}")
    print("FINAL CONSISTENCY CHECK")
    print(f"{'='*80}")
    
    all_consistent = True
    
    if task_401_results.get('winner') and task_501_results.get('winner'):
        if task_401_results['winner'] != task_501_results['winner']:
            print(f"\n❌ MISMATCH: Task 4.01 winner (Variant {task_401_results['winner']}) != Task 5.01 winner (Variant {task_501_results['winner']})")
            all_consistent = False
        else:
            print(f"\n✓ Task 4.01 and 5.01 agree: Variant {task_401_results['winner']} wins")
    
    if task_501_results.get('winner') and task_503_results.get('variant'):
        if task_501_results['winner'] != task_503_results['variant']:
            print(f"❌ MISMATCH: Task 5.01 winner (Variant {task_501_results['winner']}) != Confusion Matrix (Variant {task_503_results['variant']})")
            all_consistent = False
        else:
            print(f"✓ Task 5.01 and Confusion Matrix agree: Variant {task_501_results['winner']}")
    
    if all_consistent and task_401_results.get('winner'):
        print(f"\n{'='*80}")
        print(f"✅ ALL OUTPUTS ARE CONSISTENT!")
        print(f"   Winner: Variant {task_401_results['winner']}")
        print(f"{'='*80}")
    elif not all_consistent:
        print(f"\n{'='*80}")
        print(f"⚠️  INCONSISTENCIES DETECTED - NEED TO RE-RUN NOTEBOOK")
        print(f"{'='*80}")
        print("\nRECOMMENDATION:")
        print("1. Restart kernel")
        print("2. Run all cells from top to bottom")
        print("3. Random seeds (42) should ensure consistent results")
    
    return task_401_results, task_501_results, task_503_results

if __name__ == "__main__":
    notebook_path = r"c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb"
    t4, t5, t5_3 = deep_analysis(notebook_path)
