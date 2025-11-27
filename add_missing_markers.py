"""Add missing video segment markers to notebook"""
import re

path = r'Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Count existing markers
existing = content.count('## [VIDEO – Segment')
print(f'Found {existing} existing markers')

# Define insertions (search pattern, replacement)
insertions = [
    # Segment 5 - Before Task 4
    (
        r'<VSCode\.Cell id="#VSC-2f9b1e66" language="markdown">\n## \*\*Task 4: Hyperparameter Comparison\*\*',
        r'<VSCode.Cell language="markdown">\n## [VIDEO – Segment 5 – Dropout Comparison]\n</VSCode.Cell>\n<VSCode.Cell id="#VSC-2f9b1e66" language="markdown">\n## **Task 4: Hyperparameter Comparison**'
    ),
    # Segment 6 - Before Task 3.03
    (
        r'<VSCode\.Cell id="#VSC-4f1c416e" language="markdown">\n### \*\*Task 3\.03: Train the Model\*\*',
        r'<VSCode.Cell language="markdown">\n## [VIDEO – Segment 6 – Training]\n</VSCode.Cell>\n<VSCode.Cell id="#VSC-4f1c416e" language="markdown">\n### **Task 3.03: Train the Model**'
    ),
    # Segment 7 - Before Task 5.01
    (
        r'<VSCode\.Cell id="([^"]*)" language="markdown">\n### \*\*Task 5\.01: Evaluate Both Variants on Test Set\*\*',
        r'<VSCode.Cell language="markdown">\n## [VIDEO – Segment 7 – Test Results]\n</VSCode.Cell>\n<VSCode.Cell id="\1" language="markdown">\n### **Task 5.01: Evaluate Both Variants on Test Set**'
    ),
    # Segment 8 - Before Task 5.03  
    (
        r'<VSCode\.Cell id="([^"]*)" language="markdown">\n### \*\*Task 5\.03: Confusion Matrix for Best Variant\*\*',
        r'<VSCode.Cell language="markdown">\n## [VIDEO – Segment 8 – Confusion Matrix]\n</VSCode.Cell>\n<VSCode.Cell id="\1" language="markdown">\n### **Task 5.03: Confusion Matrix for Best Variant**'
    ),
    # Segment 9 - Before Task 6
    (
        r'<VSCode\.Cell id="([^"]*)" language="markdown">\n## \*\*Task 6: K-Fold Cross-Validation for Robust Model Evaluation\*\*',
        r'<VSCode.Cell language="markdown">\n## [VIDEO – Segment 9 – K-Fold Cross-Validation]\n</VSCode.Cell>\n<VSCode.Cell id="\1" language="markdown">\n## **Task 6: K-Fold Cross-Validation for Robust Model Evaluation**'
    ),
    # Segment 10 - Before Assignment Complete
    (
        r'<VSCode\.Cell id="([^"]*)" language="python">\n# Assignment Complete message with dynamic values',
        r'<VSCode.Cell language="markdown">\n## [VIDEO – Segment 10 – Wrap-Up]\n</VSCode.Cell>\n<VSCode.Cell id="\1" language="python">\n# Assignment Complete message with dynamic values'
    ),
]

# Apply insertions
for pattern, replacement in insertions:
    segment_num = replacement.split('Segment ')[1].split(' –')[0]
    if f'## [VIDEO – Segment {segment_num}' not in content:
        match = re.search(pattern, content)
        if match:
            content = re.sub(pattern, replacement, content, count=1)
            print(f'✓ Added Segment {segment_num}')
        else:
            print(f'✗ Pattern not found for Segment {segment_num}')
    else:
        print(f'- Segment {segment_num} already exists')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Final count
final_count = content.count('## [VIDEO – Segment')
print(f'\nTotal markers: {final_count}/11')
print('Done!')
