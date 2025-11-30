"""
Comprehensive Notebook Analysis - Check for errors, inconsistencies, and alignment
"""

import json
import re

def analyze_notebook(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    cells = nb.get('cells', [])
    issues = []
    
    print("=" * 80)
    print("COMPREHENSIVE NOTEBOOK ANALYSIS")
    print("=" * 80)
    
    # Track important variables and values
    config_values = {}
    
    for idx, cell in enumerate(cells):
        cell_num = idx + 1
        cell_type = cell.get('cell_type', 'unknown')
        
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
        
        # Check 1: AUGMENTATION_FACTOR consistency
        if 'AUGMENTATION_FACTOR' in source_text:
            match = re.search(r'AUGMENTATION_FACTOR\s*=\s*(\d+)', source_text)
            if match:
                value = int(match.group(1))
                config_values['AUGMENTATION_FACTOR'] = value
                if value != 19:
                    issues.append({
                        'cell': cell_num,
                        'type': 'ERROR',
                        'issue': f'AUGMENTATION_FACTOR should be 19, found {value}'
                    })
        
        # Check 2: Dropout values in code vs output
        if 'dropout_rates = [' in source_text:
            match = re.search(r'dropout_rates\s*=\s*\[([\d\.,\s]+)\]', source_text)
            if match:
                dropout_values = [float(x.strip()) for x in match.group(1).split(',')]
                config_values['dropout_rates'] = dropout_values
                if dropout_values != [0.2, 0.4]:
                    issues.append({
                        'cell': cell_num,
                        'type': 'WARNING',
                        'issue': f'Dropout rates are {dropout_values}, expected [0.2, 0.4]'
                    })
        
        # Check 3: Markdown claims vs actual code
        if cell_type == 'markdown':
            # Check for hardcoded winner claims
            if 'dropout 0.2' in source_text.lower() and 'our choice' in source_text.lower():
                issues.append({
                    'cell': cell_num,
                    'type': 'ERROR',
                    'issue': 'Markdown claims "dropout 0.2 is our choice" but winner should be determined by results'
                })
            
            # Check for hardcoded dropout values in descriptions
            if 'dropout = 0.2' in source_text and 'validation' in source_text.lower():
                if 'dropout regularization' not in source_text:
                    issues.append({
                        'cell': cell_num,
                        'type': 'WARNING',
                        'issue': 'Markdown hardcodes dropout=0.2 but actual winner may vary'
                    })
        
        # Check 4: Random seed consistency
        if 'random.seed' in source_text or 'np.random.seed' in source_text or 'tf.random.set_seed' in source_text:
            seed_matches = re.findall(r'(?:random|np\.random|tf\.random)\.(?:seed|set_seed)\((\d+)\)', source_text)
            if seed_matches:
                for seed in seed_matches:
                    if int(seed) != 42:
                        issues.append({
                            'cell': cell_num,
                            'type': 'WARNING',
                            'issue': f'Random seed is {seed}, not 42 (inconsistent with other cells)'
                        })
        
        # Check 5: Output mentions wrong variant
        if output_text:
            # Check Task 4.01 outputs
            if 'TASK 4.01' in source_text or 'Task 4.01' in source_text:
                winner_match = re.search(r'Variant (\d+) ✓', output_text)
                if winner_match:
                    winner = int(winner_match.group(1))
                    config_values['task_4_winner'] = winner
            
            # Check Task 5.01 outputs
            if 'TASK 5.01' in source_text or 'Task 5.01' in source_text:
                winner_match = re.search(r'Best Variant:?\s*(\d+)', output_text)
                if winner_match:
                    winner = int(winner_match.group(1))
                    config_values['task_5_winner'] = winner
            
            # Check confusion matrix
            if 'CONFUSION MATRIX' in output_text:
                variant_match = re.search(r'Variant:?\s*(\d+)', output_text)
                dropout_match = re.search(r'Dropout.*?=.*?(0\.\d+)', output_text)
                if variant_match:
                    config_values['confusion_matrix_variant'] = int(variant_match.group(1))
                if dropout_match:
                    config_values['confusion_matrix_dropout'] = float(dropout_match.group(1))
        
        # Check 6: Task numbering consistency
        if cell_type == 'markdown':
            task_matches = re.findall(r'(?:^|\n)(?:#+\s*)?(?:Task|TASK)\s+(\d+)\.(\d+)', source_text)
            for major, minor in task_matches:
                # Validate task structure (should be 1-6 for major, 01-05 for minor)
                if int(major) > 6:
                    issues.append({
                        'cell': cell_num,
                        'type': 'ERROR',
                        'issue': f'Task {major}.{minor} exceeds maximum task number (should be 1-6)'
                    })
        
        # Check 7: Code without random seeds in training sections
        if cell_type == 'code':
            if any(keyword in source_text for keyword in ['test_model.fit', 'final_model.fit', 'model.fit']):
                if 'random.seed' not in source_text and 'np.random.seed' not in source_text:
                    # Check if seeds might be set in earlier cell (acceptable)
                    if 'TASK 4.01' in source_text or 'TASK 5.01' in source_text:
                        issues.append({
                            'cell': cell_num,
                            'type': 'INFO',
                            'issue': 'Model training without explicit random seed in this cell (check if set earlier)'
                        })
    
    # Cross-cell consistency checks
    print("\n" + "=" * 80)
    print("CROSS-CELL CONSISTENCY CHECKS")
    print("=" * 80)
    
    if 'task_4_winner' in config_values and 'task_5_winner' in config_values:
        if config_values['task_4_winner'] != config_values['task_5_winner']:
            issues.append({
                'cell': 'Cross-cell',
                'type': 'CRITICAL',
                'issue': f"Task 4.01 winner (Variant {config_values['task_4_winner']}) != Task 5.01 winner (Variant {config_values['task_5_winner']})"
            })
        else:
            print(f"✓ Task 4.01 and Task 5.01 winners match: Variant {config_values['task_4_winner']}")
    
    if 'task_5_winner' in config_values and 'confusion_matrix_variant' in config_values:
        if config_values['task_5_winner'] != config_values['confusion_matrix_variant']:
            issues.append({
                'cell': 'Cross-cell',
                'type': 'CRITICAL',
                'issue': f"Task 5.01 winner (Variant {config_values['task_5_winner']}) != Confusion Matrix (Variant {config_values['confusion_matrix_variant']})"
            })
        else:
            print(f"✓ Task 5.01 and Confusion Matrix match: Variant {config_values['task_5_winner']}")
    
    if 'confusion_matrix_dropout' in config_values and 'dropout_rates' in config_values:
        cm_dropout = config_values['confusion_matrix_dropout']
        if cm_dropout not in config_values['dropout_rates']:
            issues.append({
                'cell': 'Cross-cell',
                'type': 'ERROR',
                'issue': f"Confusion Matrix shows dropout={cm_dropout} which is not in tested dropout_rates {config_values['dropout_rates']}"
            })
    
    # Report findings
    print("\n" + "=" * 80)
    print("ISSUES FOUND")
    print("=" * 80)
    
    if not issues:
        print("\n✓ NO ISSUES FOUND - Notebook is consistent!")
    else:
        critical = [i for i in issues if i['type'] == 'CRITICAL']
        errors = [i for i in issues if i['type'] == 'ERROR']
        warnings = [i for i in issues if i['type'] == 'WARNING']
        info = [i for i in issues if i['type'] == 'INFO']
        
        if critical:
            print(f"\n❌ CRITICAL ISSUES ({len(critical)}):")
            for issue in critical:
                print(f"  Cell {issue['cell']}: {issue['issue']}")
        
        if errors:
            print(f"\n⚠️  ERRORS ({len(errors)}):")
            for issue in errors:
                print(f"  Cell {issue['cell']}: {issue['issue']}")
        
        if warnings:
            print(f"\n⚠️  WARNINGS ({len(warnings)}):")
            for issue in warnings:
                print(f"  Cell {issue['cell']}: {issue['issue']}")
        
        if info:
            print(f"\nℹ️  INFO ({len(info)}):")
            for issue in info:
                print(f"  Cell {issue['cell']}: {issue['issue']}")
    
    print("\n" + "=" * 80)
    print("CONFIGURATION VALUES DETECTED")
    print("=" * 80)
    for key, value in config_values.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    
    return issues, config_values

if __name__ == "__main__":
    notebook_path = r"c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb"
    issues, config = analyze_notebook(notebook_path)
