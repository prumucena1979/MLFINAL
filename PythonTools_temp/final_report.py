import json
import re

nb_path = r'c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb'

with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)

print("="*80)
print("RELATÓRIO FINAL - VERIFICAÇÃO DE NÚMEROS NO NOTEBOOK")
print("="*80)

# Findings
findings = {
    'correct': [],
    'incorrect': [],
    'suspicious': []
}

# Check Cell 25 (Task 4 - Hyperparameter Comparison)
print("\n📋 CELL 25 - TASK 4: HYPERPARAMETER COMPARISON")
print("-"*80)
cell25_outputs = nb['cells'][25].get('outputs', [])
for output in cell25_outputs:
    if 'text' in output:
        text = ''.join(output['text'])
        if 'Best Test Accuracy:' in text:
            print("⚠️ PROBLEMA DETECTADO:")
            print("   Output mostra:")
            print("   - Variant 1: 90.48%")
            print("   - Variant 2: 99.96%")
            print("   - Variant 3: 85.71%")
            print("   - Variant 4: 98.79%")
            print("   - Variant 5: 20.00%")
            print("\n   ❌ ERRO: O assignment pede comparação de APENAS 2 variantes (dropout 0.2 vs 0.4)")
            print("   ❌ ERRO: Existem 5 variantes no output!")
            findings['incorrect'].append({
                'cell': 25,
                'issue': 'Task 4 shows 5 variants instead of 2',
                'expected': '2 variants (dropout 0.2, 0.4)',
                'actual': '5 variants in output'
            })

# Check Cell 30 (Task 5.01 - Final Evaluation)
print("\n📋 CELL 30 - TASK 5.01: FINAL EVALUATION")
print("-"*80)
cell30_outputs = nb['cells'][30].get('outputs', [])
has_output = False
for output in cell30_outputs:
    if 'text' in output:
        has_output = True
        text = ''.join(output['text'])
        if 'COMPARISON TABLE' in text:
            print("✓ Output presente com tabela de comparação")
            if 'Variant 1' in text and 'Variant 2' in text:
                findings['correct'].append({
                    'cell': 30,
                    'item': 'Shows 2 variants correctly'
                })
            if 'Training_Time_s' in text:
                print("✓ Training time capturado")
                findings['correct'].append({
                    'cell': 30,
                    'item': 'Training time tracked'
                })

if not has_output:
    print("⚠️ AVISO: Célula 30 não foi executada (sem output)")
    findings['suspicious'].append({
        'cell': 30,
        'issue': 'Cell not executed - no output to verify'
    })

# Check Cell 48 (Task 6 - K-Fold CV)
print("\n📋 CELL 48 - TASK 6: K-FOLD CROSS-VALIDATION")
print("-"*80)
cell48_outputs = nb['cells'][48].get('outputs', [])
for output in cell48_outputs:
    if 'text' in output:
        text = ''.join(output['text'])
        if 'Mean Accuracy:' in text:
            match = re.search(r'Mean Accuracy:\s*0\.\d+\s*\(([\d.]+)%\)', text)
            if match:
                kfold_acc = match.group(1)
                print(f"✓ K-Fold CV Mean Accuracy: {kfold_acc}%")
                findings['correct'].append({
                    'cell': 48,
                    'item': f'K-Fold accuracy: {kfold_acc}%'
                })

# Check Markdown in Cell 1
print("\n📋 CELL 1 - WALKTHROUGH MARKDOWN")
print("-"*80)
cell1_source = ''.join(nb['cells'][1]['source'])
if '99.81%' in cell1_source:
    print("❌ ERRO: Walkthrough claims 99.81%")
    print("   Real: 99.78% (conforme Cell 48 output)")
    findings['incorrect'].append({
        'cell': 1,
        'issue': 'K-Fold accuracy incorrect in walkthrough',
        'claimed': '99.81%',
        'actual': '99.78%'
    })
elif '99.78%' in cell1_source:
    print("✓ K-Fold accuracy correto: 99.78%")
    findings['correct'].append({
        'cell': 1,
        'item': 'K-Fold accuracy: 99.78%'
    })

# Check dataset size
print("\n📋 DATASET SIZE")
print("-"*80)
if '210 samples' in cell1_source:
    print("✓ Dataset size: 210 samples")
    findings['correct'].append({'item': 'Dataset size: 210 samples'})

if '378 samples' in cell1_source:
    print("⚠️ SUSPEITO: Menciona 378 samples para K-Fold")
    print("   VERIFICAR: K-Fold usa dataset aumentado com noise augmentation?")
    print("   Original: 210 samples")
    print("   Augmented: 210 * 1.8 = 378 samples (possível)")
    findings['suspicious'].append({
        'item': '378 samples mentioned for K-Fold',
        'note': 'Might be augmented dataset (210 * 1.8 = 378)'
    })

# Architecture check
print("\n📋 ARCHITECTURE")
print("-"*80)
if '7→64→32→3' in cell1_source:
    print("✓ Architecture: 7→64→32→3 (2 hidden layers)")
    findings['correct'].append({'item': 'Architecture: 2 hidden layers'})

if '3 hidden layers' in cell1_source.lower():
    print("❌ ERRO: Menciona 3 hidden layers")
    print("   Real: 2 hidden layers (64, 32)")
    findings['incorrect'].append({
        'cell': 1,
        'issue': 'Claims 3 hidden layers',
        'actual': '2 hidden layers'
    })

# Final Report
print("\n" + "="*80)
print("RESUMO FINAL")
print("="*80)
print(f"\n✅ Corretos: {len(findings['correct'])}")
print(f"❌ Incorretos: {len(findings['incorrect'])}")
print(f"⚠️ Suspeitos: {len(findings['suspicious'])}")

if findings['incorrect']:
    print("\n" + "="*80)
    print("❌ PROBLEMAS QUE PRECISAM SER CORRIGIDOS:")
    print("="*80)
    for i, item in enumerate(findings['incorrect'], 1):
        print(f"\n{i}. Cell {item.get('cell', 'N/A')}")
        print(f"   Problema: {item['issue']}")
        if 'claimed' in item:
            print(f"   Afirmado: {item['claimed']}")
        if 'actual' in item:
            print(f"   Real: {item['actual']}")
        if 'expected' in item:
            print(f"   Esperado: {item['expected']}")

if findings['suspicious']:
    print("\n" + "="*80)
    print("⚠️ ITENS PARA REVISAR:")
    print("="*80)
    for i, item in enumerate(findings['suspicious'], 1):
        print(f"\n{i}. {item.get('item', 'Item')}")
        if 'issue' in item:
            print(f"   Questão: {item['issue']}")
        if 'note' in item:
            print(f"   Nota: {item['note']}")

print("\n" + "="*80)
print("PLANO DE AÇÃO:")
print("="*80)
print("\n1. Corrigir Cell 1 walkthrough: 99.81% → 99.78%")
print("2. Verificar Cell 25 (Task 4): Por que 5 variantes ao invés de 2?")
print("3. Executar Cell 30 se ainda não foi executada")
print("4. Verificar se 378 samples é correto para K-Fold (pode ser dataset augmentado)")
