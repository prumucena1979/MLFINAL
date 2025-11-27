"""Remove all VIDEO segment marker cells from notebook"""
import re

path = r'Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Count before
before_count = content.count('## [VIDEO – Segment')
print(f'Found {before_count} VIDEO segment markers')

# Remove all VIDEO segment cells
# Pattern: <VSCode.Cell id="..." language="markdown">\n## [VIDEO – Segment ...]\n</VSCode.Cell>\n
pattern = r'<VSCode\.Cell id="[^"]*" language="markdown">\n## \[VIDEO – Segment \d+ – [^\]]+\]\n</VSCode\.Cell>\n'

content = re.sub(pattern, '', content)

# Count after
after_count = content.count('## [VIDEO – Segment')
print(f'Removed {before_count - after_count} markers')
print(f'Remaining: {after_count}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done!')
