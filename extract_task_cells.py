"""Extract specific task cells from notebook"""
import json

def get_cells_with_content(filepath, search_terms):
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    cells = nb.get('cells', [])
    
    for idx, cell in enumerate(cells):
        source = cell.get('source', [])
        if isinstance(source, list):
            source_text = ''.join(source)
        else:
            source_text = source
        
        for term in search_terms:
            if term in source_text:
                print(f"\n{'='*80}")
                print(f"Cell {idx + 1} - Type: {cell['cell_type']}")
                print(f"Found: {term}")
                print(f"{'='*80}")
                print(source_text[:2000])  # First 2000 chars
                if len(source_text) > 2000:
                    print(f"\n... (truncated, total length: {len(source_text)} chars)")
                break

if __name__ == "__main__":
    notebook_path = r"c:\Users\fabio\OneDrive - GUSCanada\VSCODEGIT\MyUNFrepo\MLFINALINDIVIDUAL\MLFINAL\Turnin\notebook\Seeds_ML_FINALPRJ_NF1002000.ipynb"
    
    search_terms = [
        "# TASK 4.01:",
        "# TASK 5.01:",
        "# TASK 5.03:",
        "the ends up being our choice"
    ]
    
    get_cells_with_content(notebook_path, search_terms)
