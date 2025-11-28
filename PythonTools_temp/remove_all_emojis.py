import json
import re

nb_path = r'c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb'

with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)

# More comprehensive emoji mapping
replacements = {
    '✓': '[OK]',
    '✅': '[BEST]',
    '❌': '[ERROR]',
    '⚠️': '[WARNING]',
    '⚠': '[WARNING]',
    '📊': '[STATS]',
    '📋': '[INFO]',
    '🎯': '[TARGET]',
    '🏆': '[WINNER]',
    '🔄': '[TIE]',
    '💡': '[NOTE]',
    '•': '-',
    '◆': '*',
    '◇': '*',
    '★': '*',
    '☆': '*',
    '○': 'o',
    '●': '*',
    '→': '->',
    '←': '<-',
    '↑': '^',
    '↓': 'v',
    '⇒': '=>',
    '⇐': '<=',
    '×': 'x',
    '▪': '-',
    '1️⃣': '[1]',
    '2️⃣': '[2]',
    '3️⃣': '[3]',
    '4️⃣': '[4]',
    '5️⃣': '[5]',
}

changes_count = 0
cells_modified = []

for i, cell in enumerate(nb['cells']):
    source = ''.join(cell['source'])
    original = source
    
    # Replace all emojis
    for emoji, replacement in replacements.items():
        if emoji in source:
            source = source.replace(emoji, replacement)
    
    if source != original:
        nb['cells'][i]['source'] = source.split('\n')
        cells_modified.append(i)
        changes_count += 1

# Save
with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("="*80)
print("REMOVING ALL EMOJIS/ICONS FROM NOTEBOOK")
print("="*80)
print(f"\nCells modified: {changes_count}")
print(f"Cell numbers: {cells_modified[:10]}{'...' if len(cells_modified) > 10 else ''}")
print("\nAll modern icons replaced with classic text alternatives")
print("\nReplacements made:")
for emoji, replacement in replacements.items():
    print(f"  {emoji} -> {replacement}")
