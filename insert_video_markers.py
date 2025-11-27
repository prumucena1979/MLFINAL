"""
Insert VIDEO segment markers into the notebook
"""

import re
from pathlib import Path

notebook_path = Path(__file__).parent / 'Turnin' / 'notebook' / 'Seeds_ML_FINALPRJ_NF1002000.ipynb'

# Read the notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define markers to insert (cell_id_pattern, marker_text)
# We'll insert AFTER the specified cell (so it appears BEFORE the next section)
markers_to_insert = [
    # Segment 6 (Training) - before Task 3.03
    (r'(<VSCode\.Cell id="[^"]*" language="markdown">)\s*### \*\*Task 3\.03: Train the Model\*\*',
     '## [VIDEO – Segment 6 – Training]'),
    
    # Segment 5 (Dropout Comparison) - before Task 4
    (r'(<VSCode\.Cell id="[^"]*" language="markdown">)\s*## \*\*Task 4: Hyperparameter Comparison\*\*',
     '## [VIDEO – Segment 5 – Dropout Comparison]'),
    
    # Segment 7 (Test Results) - before Task 5.01
    (r'(<VSCode\.Cell id="[^"]*" language="markdown">)\s*### \*\*Task 5\.01: Evaluate Both Variants on Test Set\*\*',
     '## [VIDEO – Segment 7 – Test Results]'),
    
    # Segment 8 (Confusion Matrix) - before Task 5.03
    (r'(<VSCode\.Cell id="[^"]*" language="markdown">)\s*### \*\*Task 5\.03: Confusion Matrix for Best Variant\*\*',
     '## [VIDEO – Segment 8 – Confusion Matrix]'),
    
    # Segment 9 (K-Fold) - before Task 6
    (r'(<VSCode\.Cell id="[^"]*" language="markdown">)\s*## \*\*Task 6: K-Fold Cross-Validation',
     '## [VIDEO – Segment 9 – K-Fold Cross-Validation]'),
    
    # Segment 10 (Wrap-Up) - before Assignment Complete
    (r'(<VSCode\.Cell id="[^"]*" language="python">)\s*# Assignment Complete message',
     '## [VIDEO – Segment 10 – Wrap-Up]'),
]

# Process each marker
for pattern, marker_text in markers_to_insert:
    # Find the cell
    match = re.search(pattern, content, re.DOTALL)
    if match:
        # Insert a new markdown cell BEFORE this cell
        insertion_point = match.start()
        new_cell = f'<VSCode.Cell language="markdown">\n{marker_text}\n</VSCode.Cell>\n'
        content = content[:insertion_point] + new_cell + content[insertion_point:]
        print(f"✓ Inserted: {marker_text}")
    else:
        print(f"✗ Not found: {marker_text}")

# Write back
with open(notebook_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✓ Video markers inserted into {notebook_path}")
