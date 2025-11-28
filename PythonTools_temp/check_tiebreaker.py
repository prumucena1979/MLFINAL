import json

nb_path = r'c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb'

with open(nb_path, encoding='utf-8') as f:
    nb = json.load(f)

# Find cell with tiebreaker code
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'Tiebreaker' in source and 'SELECTING BEST VARIANT' in source:
            print(f"Found tiebreaker code in cell {i}")
            
            # Check for any emojis
            import re
            # Look for emoji patterns
            emojis = re.findall(r'[\U0001F300-\U0001F9FF]', source)
            if emojis:
                print(f"Found emojis: {emojis}")
            
            # Look for the specific lines
            lines = source.split('\n')
            for idx, line in enumerate(lines):
                if 'Tiebreaker #' in line:
                    print(f"Line {idx}: {line[:100]}")
