import json

# Read the notebook
with open('MLfinalAssignment_NF1002000.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Find Task 6 completion
task_6_end = -1
for idx, cell in enumerate(notebook['cells']):
    source = ''.join(cell.get('source', []))
    if 'TASK 6: K-FOLD CROSS-VALIDATION - ALL SUBTASKS COMPLETED' in source:
        task_6_end = idx
        break

if task_6_end == -1:
    print("Searching for alternative Task 6 end markers...")
    for idx, cell in enumerate(notebook['cells']):
        source = ''.join(cell.get('source', []))
        if '[TASK 6.05 COMPLETED]' in source:
            task_6_end = idx
            break

# Remove everything after Task 6
if task_6_end > 0:
    removed = len(notebook['cells']) - (task_6_end + 1)
    notebook['cells'] = notebook['cells'][:task_6_end + 1]
    print(f"Removed {removed} cells after Task 6 (index {task_6_end})")
else:
    # Fallback: remove specific Task 7/8 cells
    print("Using fallback method...")
    to_remove = []
    for idx, cell in enumerate(notebook['cells']):
        source = ''.join(cell.get('source', []))
        keywords = ['Task 7', 'Task 8', 'BatchNorm', 'L2 Reg', 'l2_lambda', 'build_model_with']
        if any(k in source for k in keywords):
            to_remove.append(idx)
    
    for idx in reversed(to_remove):
        del notebook['cells'][idx]
    print(f"Removed {len(to_remove)} cells with Task 7/8 content")

# Add conclusion
notebook['cells'].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "---\n\n",
        "## **Assignment Complete**\n\n",
        "All required tasks (1-6) completed successfully.\n\n",
        "**Final Model:** Task 6 K-Fold CV - 97.62% accuracy\n\n",
        "---"
    ]
})

# Save
with open('MLfinalAssignment_NF1002000.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("Cleanup complete!")
