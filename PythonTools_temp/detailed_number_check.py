import json
import re

nb_path = r'c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb'

# Read notebook
with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)

print("="*80)
print("ANÁLISE DETALHADA - TODOS OS NÚMEROS NO NOTEBOOK")
print("="*80)

# Collect all numeric claims
claims = []

for i, cell in enumerate(nb['cells']):
    source = ''.join(cell['source'])
    cell_type = cell['cell_type']
    
    # Extract all percentages
    percentages = re.findall(r'(\d+\.?\d*)\s*%', source)
    for pct in percentages:
        claims.append({
            'cell': i,
            'type': cell_type,
            'value': f"{pct}%",
            'context': source[max(0, source.find(pct)-50):source.find(pct)+100]
        })
    
    # Extract accuracy values
    if 'ccuracy' in source.lower():
        matches = re.findall(r'(0\.\d{4}|\d+\.\d+%)', source)
        for match in matches:
            claims.append({
                'cell': i,
                'type': cell_type,
                'value': match,
                'context': source[max(0, source.find(match)-50):source.find(match)+100]
            })

# Also check outputs
print("\n📊 VERIFICANDO OUTPUTS DE CÉLULAS EXECUTADAS:")
print("="*80)

output_values = {}

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        outputs = cell.get('outputs', [])
        for output in outputs:
            if 'text' in output:
                text = ''.join(output['text'])
                
                # K-Fold accuracy
                if 'Mean Accuracy:' in text:
                    match = re.search(r'Mean Accuracy:\s*(0\.\d+)\s*\(([\d.]+)%\)', text)
                    if match:
                        output_values['kfold_mean'] = f"{match.group(2)}%"
                        print(f"Cell {i}: K-Fold Mean Accuracy = {match.group(2)}%")
                
                if 'Std:' in text and '%' in text:
                    match = re.search(r'Std:\s*(0\.\d+)\s*\(([\d.]+)%\)', text)
                    if match:
                        output_values['kfold_std'] = f"{match.group(2)}%"
                        print(f"Cell {i}: K-Fold Std = {match.group(2)}%")
                
                # Test accuracy from hyperparameter comparison
                if 'Best Test Accuracy:' in text:
                    match = re.search(r'Best Test Accuracy:\s*(0\.\d+)\s*\(accuracy\s*=\s*(0\.\d+)\)', text)
                    if match:
                        output_values['best_test_acc'] = f"{float(match.group(2))*100:.2f}%"
                        print(f"Cell {i}: Best Test Accuracy = {float(match.group(2))*100:.2f}%")
                
                # Variant accuracies
                if 'Accuracy:' in text and 'VARIANT' in text:
                    matches = re.findall(r'Accuracy:\s*(0\.\d+)', text)
                    for idx, acc in enumerate(matches, 1):
                        print(f"Cell {i}: Variant {idx} Test Accuracy = {float(acc)*100:.2f}%")

print("\n" + "="*80)
print("VERIFICANDO CONSISTÊNCIA EM MARKDOWNS:")
print("="*80)

inconsistencies = []

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown':
        source = ''.join(cell['source'])
        
        # Check K-Fold claims
        if 'K-Fold' in source and '%' in source:
            # Extract percentage claims
            if '99.81%' in source and output_values.get('kfold_mean') and output_values['kfold_mean'] != '99.81%':
                inconsistencies.append({
                    'cell': i,
                    'claimed': '99.81%',
                    'actual': output_values['kfold_mean'],
                    'metric': 'K-Fold Mean Accuracy',
                    'text': source[:200]
                })
            
            if '99.91%' in source and output_values.get('kfold_mean') and output_values['kfold_mean'] != '99.91%':
                inconsistencies.append({
                    'cell': i,
                    'claimed': '99.91%',
                    'actual': output_values['kfold_mean'],
                    'metric': 'K-Fold Mean Accuracy',
                    'text': source[:200]
                })
            
            if '99.78%' in source and output_values.get('kfold_mean') and output_values['kfold_mean'] != '99.78%':
                inconsistencies.append({
                    'cell': i,
                    'claimed': '99.78%',
                    'actual': output_values['kfold_mean'],
                    'metric': 'K-Fold Mean Accuracy',
                    'text': source[:200]
                })
        
        # Check dataset size
        if '210 samples' in source:
            print(f"Cell {i}: Claims 210 samples ✓")
        
        if '378 samples' in source:
            print(f"Cell {i}: Claims 378 samples (VERIFICAR: K-Fold usa dataset completo?)")
        
        # Check architecture
        if '3 hidden layers' in source:
            inconsistencies.append({
                'cell': i,
                'claimed': '3 hidden layers',
                'actual': '2 hidden layers (64, 32)',
                'metric': 'Architecture',
                'text': source[:200]
            })

print("\n" + "="*80)
print(f"INCONSISTÊNCIAS ENCONTRADAS: {len(inconsistencies)}")
print("="*80)

if inconsistencies:
    for idx, issue in enumerate(inconsistencies, 1):
        print(f"\n❌ {idx}. Cell {issue['cell']}")
        print(f"   Métrica: {issue['metric']}")
        print(f"   Afirmado: {issue['claimed']}")
        print(f"   Real: {issue['actual']}")
        print(f"   Contexto: {issue['text'][:150]}...")

print("\n" + "="*80)
print("VALORES CORRETOS CONFIRMADOS:")
print("="*80)
if output_values:
    for key, value in output_values.items():
        print(f"  {key}: {value}")

print("\n" + "="*80)
print("PRÓXIMOS PASSOS:")
print("="*80)
if inconsistencies:
    print("⚠️ AÇÃO NECESSÁRIA: Corrigir as inconsistências listadas acima")
    print("\nResumo das correções:")
    metrics = {}
    for issue in inconsistencies:
        metric = issue['metric']
        if metric not in metrics:
            metrics[metric] = []
        metrics[metric].append(f"{issue['claimed']} → {issue['actual']}")
    
    for metric, corrections in metrics.items():
        print(f"\n  {metric}:")
        for correction in set(corrections):
            print(f"    - {correction}")
else:
    print("✅ Tudo está correto! Nenhuma ação necessária.")
