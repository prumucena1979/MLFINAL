import json
import re

nb_path = r'c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb'

# Read notebook
with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)

# Store findings
issues = []
stats = {
    'dataset_size': None,
    'features': None,
    'classes': None,
    'train_size': None,
    'test_size': None,
    'dropout_rates': [],
    'kfold_accuracy': None,
    'test_accuracy': None,
    'epochs': None,
    'batch_size': None,
    'architecture': None
}

print("="*80)
print("ANÁLISE COMPLETA DO NOTEBOOK - VERIFICAÇÃO DE NÚMEROS")
print("="*80)

# First pass: extract actual values from code outputs
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        # Check outputs
        outputs = cell.get('outputs', [])
        for output in outputs:
            if 'text' in output:
                text = ''.join(output['text'])
                
                # Extract dataset info
                if 'Total samples:' in text:
                    match = re.search(r'Total samples:\s*(\d+)', text)
                    if match:
                        stats['dataset_size'] = int(match.group(1))
                
                if 'Features:' in text and 'Classes:' in text:
                    match_feat = re.search(r'Features:\s*(\d+)', text)
                    match_class = re.search(r'Classes:\s*(\d+)', text)
                    if match_feat:
                        stats['features'] = int(match_feat.group(1))
                    if match_class:
                        stats['classes'] = int(match_class.group(1))
                
                # Extract train/test split
                if 'Train/Test split:' in text:
                    match = re.search(r'(\d+)/(\d+)\s+samples', text)
                    if match:
                        stats['train_size'] = int(match.group(1))
                        stats['test_size'] = int(match.group(2))
                
                # Extract K-Fold accuracy
                if 'Mean Accuracy:' in text and '99.' in text:
                    match = re.search(r'Mean Accuracy:\s*(0\.\d+)\s*\(([\d.]+)%\)', text)
                    if match:
                        stats['kfold_accuracy'] = match.group(2) + '%'
                
                # Extract dropout rates
                if 'Dropout Rate' in text and 'Variant' in text:
                    matches = re.findall(r'dropout[_=\s]*(0\.\d+)', text, re.IGNORECASE)
                    for m in matches:
                        if m not in stats['dropout_rates']:
                            stats['dropout_rates'].append(m)

print("\n" + "="*80)
print("VALORES ENCONTRADOS NOS OUTPUTS DO CÓDIGO:")
print("="*80)
print(f"Dataset size: {stats['dataset_size']}")
print(f"Features: {stats['features']}")
print(f"Classes: {stats['classes']}")
print(f"Train size: {stats['train_size']}")
print(f"Test size: {stats['test_size']}")
print(f"Dropout rates tested: {stats['dropout_rates']}")
print(f"K-Fold CV accuracy: {stats['kfold_accuracy']}")

# Second pass: verify markdown claims
print("\n" + "="*80)
print("VERIFICANDO MARKDOWNS E COMENTÁRIOS:")
print("="*80)

for i, cell in enumerate(nb['cells']):
    source = ''.join(cell['source'])
    
    # Check dataset size claims
    if '210 samples' in source:
        if stats['dataset_size'] and stats['dataset_size'] != 210:
            issues.append({
                'cell': i,
                'type': 'markdown' if cell['cell_type'] == 'markdown' else 'code',
                'issue': f"Claims 210 samples but actual is {stats['dataset_size']}",
                'text': source[:100]
            })
    
    # Check features
    if '7 features' in source.lower():
        if stats['features'] and stats['features'] != 7:
            issues.append({
                'cell': i,
                'type': cell['cell_type'],
                'issue': f"Claims 7 features but actual is {stats['features']}",
                'text': source[:100]
            })
    
    # Check K-Fold accuracy
    if '97.62%' in source or '97.62' in source:
        issues.append({
            'cell': i,
            'type': cell['cell_type'],
            'issue': f"Claims 97.62% but K-Fold shows {stats['kfold_accuracy']}",
            'text': source[:150]
        })
    
    if '99.91%' in source:
        if stats['kfold_accuracy'] and '99.81%' in str(stats['kfold_accuracy']):
            issues.append({
                'cell': i,
                'type': cell['cell_type'],
                'issue': f"Claims 99.91% but K-Fold shows {stats['kfold_accuracy']}",
                'text': source[:150]
            })
    
    # Check train/test split ratios
    if stats['train_size'] and stats['test_size']:
        total = stats['train_size'] + stats['test_size']
        if f'{stats["train_size"]}/{stats["test_size"]}' not in source and '80/20' in source:
            actual_ratio = f"{stats['train_size']}/{stats['test_size']}"
            if actual_ratio != f"{int(total*0.8)}/{int(total*0.2)}":
                issues.append({
                    'cell': i,
                    'type': cell['cell_type'],
                    'issue': f"Claims 80/20 split but actual is {actual_ratio}",
                    'text': source[:100]
                })
    
    # Check architecture claims
    if '7→64→32→3' in source or '7-64-32-3' in source:
        # This is correct, no issue
        pass
    
    if '3 hidden layers' in source.lower():
        issues.append({
            'cell': i,
            'type': cell['cell_type'],
            'issue': "Claims 3 hidden layers but architecture is 7→64→32→3 (2 hidden layers)",
            'text': source[:150]
        })

print("\n" + "="*80)
print(f"PROBLEMAS ENCONTRADOS: {len(issues)}")
print("="*80)

if issues:
    for idx, issue in enumerate(issues, 1):
        print(f"\n{idx}. Cell {issue['cell']} ({issue['type']})")
        print(f"   Problema: {issue['issue']}")
        print(f"   Trecho: {issue['text']}...")
else:
    print("\n✅ Nenhum problema encontrado!")

# Summary report
print("\n" + "="*80)
print("RELATÓRIO FINAL")
print("="*80)
print(f"\nTotal de células analisadas: {len(nb['cells'])}")
print(f"Problemas identificados: {len(issues)}")

if issues:
    print("\n📋 CATEGORIAS DE PROBLEMAS:")
    problem_types = {}
    for issue in issues:
        key = issue['issue'].split('but')[0].strip()
        problem_types[key] = problem_types.get(key, 0) + 1
    
    for prob_type, count in problem_types.items():
        print(f"  - {prob_type}: {count} ocorrências")
    
    print("\n⚠️ AÇÃO NECESSÁRIA: Corrigir os valores incorretos identificados acima")
else:
    print("\n✅ TUDO CORRETO: Todos os números estão consistentes!")
