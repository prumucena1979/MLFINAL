import json

nb_path = r'c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb'

with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)

print("="*80)
print("CORRIGINDO PROBLEMAS IDENTIFICADOS")
print("="*80)

# Fix 1: Cell 1 - Walkthrough accuracy
print("\n1. Corrigindo Cell 1 - K-Fold accuracy...")
for i, cell in enumerate(nb['cells']):
    if cell.get('id') == '600df8d5':
        source = ''.join(cell['source'])
        if '99.81%' in source:
            new_source = source.replace('99.81%', '99.78%')
            nb['cells'][i]['source'] = new_source.split('\n')
            print("   ✅ 99.81% → 99.78%")
        else:
            print("   ℹ️ Já estava correto ou não encontrado")
        break

# Fix 2: Check Cell 25 code
print("\n2. Analisando Cell 25 - Task 4 Hyperparameter Comparison...")
cell25_source = ''.join(nb['cells'][25]['source'])

# Check if it's testing more than 2 dropout rates
import re
dropout_matches = re.findall(r'dropout_rates\s*=\s*\[(.*?)\]', cell25_source)
if dropout_matches:
    print(f"   Dropout rates definidos: {dropout_matches[0]}")
    
    # Check if it has more than 2 values
    values = [x.strip() for x in dropout_matches[0].split(',')]
    if len(values) > 2:
        print(f"   ❌ PROBLEMA: {len(values)} valores ao invés de 2")
        print("   Corrigindo para apenas [0.2, 0.4]...")
        
        # Fix the dropout_rates definition
        new_source = re.sub(
            r'dropout_rates\s*=\s*\[.*?\]',
            'dropout_rates = [0.2, 0.4]',
            cell25_source
        )
        
        nb['cells'][25]['source'] = new_source.split('\n')
        print("   ✅ Corrigido para dropout_rates = [0.2, 0.4]")
    else:
        print(f"   ℹ️ Código já tem apenas 2 valores: {values}")
        print("   ⚠️ Output pode ser de execução antiga - precisa re-executar célula")
else:
    print("   ⚠️ Não encontrou definição de dropout_rates")

# Save notebook
with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("\n" + "="*80)
print("CORREÇÕES APLICADAS")
print("="*80)
print("\n✅ Notebook salvo com correções")
print("\n⚠️ IMPORTANTE: Cell 25 precisa ser RE-EXECUTADA para gerar output correto")
print("   Atualmente o output mostra 5 variantes (execução antiga)")
print("   Após re-executar, deve mostrar apenas 2 variantes (0.2 e 0.4)")
