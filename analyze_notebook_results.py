"""
Comprehensive Notebook Analysis for Hyperparameter Comparison
Analyzes Task 4.01, Task 5.01, and Task 5.03 for consistency
"""

import json
import re

def read_notebook(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_cell_content(cell):
    """Extract text content from a cell"""
    if 'source' in cell:
        if isinstance(cell['source'], list):
            return ''.join(cell['source'])
        return cell['source']
    return ''

def extract_output_content(cell):
    """Extract output text from a cell"""
    outputs = []
    if 'outputs' in cell:
        for output in cell['outputs']:
            if 'text' in output:
                if isinstance(output['text'], list):
                    outputs.append(''.join(output['text']))
                else:
                    outputs.append(output['text'])
            if 'data' in output and 'text/plain' in output['data']:
                data = output['data']['text/plain']
                if isinstance(data, list):
                    outputs.append(''.join(data))
                else:
                    outputs.append(data)
    return '\n'.join(outputs)

def analyze_notebook(filepath):
    nb = read_notebook(filepath)
    cells = nb.get('cells', [])
    
    print("=" * 80)
    print("NOTEBOOK ANALYSIS: HYPERPARAMETER COMPARISON REVIEW")
    print("=" * 80)
    
    # Find Task 4.01
    task_401_cells = []
    task_501_cells = []
    task_503_cells = []
    
    for idx, cell in enumerate(cells):
        content = extract_cell_content(cell)
        output = extract_output_content(cell)
        
        # Task 4.01
        if 'TASK 4.01' in content or 'Task 4.01' in content:
            task_401_cells.append((idx + 1, content, output, cell['cell_type']))
        
        # Task 5.01
        if 'TASK 5.01' in content or 'Task 5.01' in content:
            task_501_cells.append((idx + 1, content, output, cell['cell_type']))
        
        # Task 5.03
        if 'TASK 5.03' in content or 'Task 5.03' in content or 'Task 5.03' in output:
            task_503_cells.append((idx + 1, content, output, cell['cell_type']))
    
    # Analyze Task 4.01
    print("\n" + "=" * 80)
    print("TASK 4.01: HYPERPARAMETER COMPARISON")
    print("=" * 80)
    
    for cell_num, content, output, cell_type in task_401_cells:
        if output:
            print(f"\n--- Cell {cell_num} Output ---")
            
            # Look for comparison results
            if 'dropout_rate' in output.lower() or 'variant' in output.lower():
                lines = output.split('\n')
                for line in lines:
                    if 'dropout' in line.lower() or 'variant' in line.lower() or \
                       'f1' in line.lower() or 'accuracy' in line.lower():
                        print(line)
            
            # Look for winner indication
            if '✓' in output or 'winner' in output.lower():
                print("\n*** WINNER INDICATION ***")
                lines = output.split('\n')
                for line in lines:
                    if '✓' in line or 'winner' in line.lower():
                        print(line)
    
    # Analyze Task 5.01
    print("\n" + "=" * 80)
    print("TASK 5.01: RE-EVALUATE AND SELECT BEST VARIANT")
    print("=" * 80)
    
    for cell_num, content, output, cell_type in task_501_cells:
        if output:
            print(f"\n--- Cell {cell_num} Output ---")
            
            # Look for best variant selection
            if 'best variant' in output.lower() or 'winning' in output.lower():
                lines = output.split('\n')
                for line in lines:
                    if 'variant' in line.lower() or 'dropout' in line.lower() or \
                       'f1' in line.lower() or 'accuracy' in line.lower():
                        print(line)
    
    # Analyze Task 5.03 - Confusion Matrix
    print("\n" + "=" * 80)
    print("TASK 5.03: CONFUSION MATRIX FOR BEST VARIANT")
    print("=" * 80)
    
    for cell_num, content, output, cell_type in task_503_cells:
        if output:
            print(f"\n--- Cell {cell_num} Output ---")
            
            # Extract dropout rate mentioned
            dropout_matches = re.findall(r'Dropout.*?=.*?(0\.\d+)', output, re.IGNORECASE)
            variant_matches = re.findall(r'Variant:?\s*(\d+)', output, re.IGNORECASE)
            f1_matches = re.findall(r'F[₁1]-?Score:?\s*(0\.\d+)', output, re.IGNORECASE)
            acc_matches = re.findall(r'Accuracy:?\s*(0\.\d+)', output, re.IGNORECASE)
            
            if dropout_matches:
                print(f"  Dropout Rate mentioned: {dropout_matches}")
            if variant_matches:
                print(f"  Variant mentioned: {variant_matches}")
            if f1_matches:
                print(f"  F1-Score mentioned: {f1_matches}")
            if acc_matches:
                print(f"  Accuracy mentioned: {acc_matches}")
            
            # Show first few lines of output
            lines = output.split('\n')[:30]
            for line in lines:
                if 'variant' in line.lower() or 'dropout' in line.lower() or \
                   'f1' in line.lower() or 'accuracy' in line.lower() or \
                   'best' in line.lower():
                    print(line)
    
    # Summary
    print("\n" + "=" * 80)
    print("CONSISTENCY CHECK")
    print("=" * 80)
    print("\n✓ Expected: Variant 1 (Dropout=0.2) should win based on higher F1-Score")
    print("✓ Check all outputs above to verify consistency")
    print("✓ Confusion matrix should show Variant 1 with Dropout=0.2")

if __name__ == "__main__":
    notebook_path = r"c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb"
    analyze_notebook(notebook_path)
