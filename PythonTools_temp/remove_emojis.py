import json
import re

nb_path = r'c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb'

with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)

# Mapping of modern emojis to classic alternatives
replacements = {
    '🔄': '[TIE]',
    '✅': '[BEST]',
    '❌': '[ERROR]',
    '⚠️': '[WARNING]',
    '📊': '[STATS]',
    '📋': '[INFO]',
    '🎯': '[TARGET]',
    '🏆': '[WINNER]',
    '1️⃣': '[1]',
    '2️⃣': '[2]',
    '3️⃣': '[3]',
    '4️⃣': '[4]',
    '5️⃣': '[5]',
    '→': '->',
}

changes_made = []

for i, cell in enumerate(nb['cells']):
    source = ''.join(cell['source'])
    original = source
    
    # Replace all emojis
    for emoji, replacement in replacements.items():
        if emoji in source:
            source = source.replace(emoji, replacement)
            if emoji not in [change[0] for change in changes_made]:
                changes_made.append((emoji, replacement))
    
    if source != original:
        nb['cells'][i]['source'] = source.split('\n')
        print(f"Cell {i} updated")

# Save
with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("\n" + "="*80)
print("EMOJI REPLACEMENTS COMPLETED")
print("="*80)
for emoji, replacement in changes_made:
    print(f"  {emoji} -> {replacement}")

print(f"\nTotal cells modified: {sum(1 for _ in changes_made)}")
print("✓ All modern emojis replaced with classic alternatives")
