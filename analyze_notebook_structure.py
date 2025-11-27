"""
Notebook Structure Analyzer
Reads and documents the structure of Seeds_ML_FINALPRJ_NF1002000.ipynb
"""

import json
import re
from pathlib import Path
from collections import defaultdict

class NotebookAnalyzer:
    def __init__(self, notebook_path):
        self.notebook_path = Path(notebook_path)
        self.cells = []
        self.structure = {
            'total_cells': 0,
            'markdown_cells': 0,
            'code_cells': 0,
            'tasks': [],
            'sections': [],
            'key_variables': set(),
            'imports': set()
        }
        
    def load_notebook(self):
        """Load and parse the notebook JSON structure"""
        with open(self.notebook_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse XML-like structure
        cell_pattern = r'<VSCode\.Cell id="([^"]*)" language="([^"]*)">(.*?)</VSCode\.Cell>'
        matches = re.findall(cell_pattern, content, re.DOTALL)
        
        for cell_id, language, content_text in matches:
            self.cells.append({
                'id': cell_id,
                'language': language,
                'content': content_text.strip()
            })
            
        self.structure['total_cells'] = len(self.cells)
        self.structure['markdown_cells'] = sum(1 for c in self.cells if c['language'] == 'markdown')
        self.structure['code_cells'] = sum(1 for c in self.cells if c['language'] == 'python')
        
    def analyze_tasks(self):
        """Extract task structure"""
        task_pattern = r'##\s*\*\*Task\s+(\d+(?:\.\d+)?)[:\s]+([^*]+)\*\*'
        
        for i, cell in enumerate(self.cells):
            if cell['language'] == 'markdown':
                matches = re.finditer(task_pattern, cell['content'])
                for match in matches:
                    task_num = match.group(1)
                    task_title = match.group(2).strip()
                    self.structure['tasks'].append({
                        'number': task_num,
                        'title': task_title,
                        'cell_index': i,
                        'cell_id': cell['id']
                    })
    
    def analyze_sections(self):
        """Extract main sections"""
        section_pattern = r'^##\s+\*\*([^*]+)\*\*'
        
        for i, cell in enumerate(self.cells):
            if cell['language'] == 'markdown':
                matches = re.finditer(section_pattern, cell['content'], re.MULTILINE)
                for match in matches:
                    section_title = match.group(1).strip()
                    if not section_title.startswith('Task'):
                        self.structure['sections'].append({
                            'title': section_title,
                            'cell_index': i
                        })
    
    def analyze_code(self):
        """Extract key variables and imports"""
        import_pattern = r'^import\s+(\S+)|^from\s+(\S+)\s+import'
        variable_pattern = r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*='
        
        for cell in self.cells:
            if cell['language'] == 'python':
                # Find imports
                for line in cell['content'].split('\n'):
                    line = line.strip()
                    if match := re.match(import_pattern, line):
                        module = match.group(1) or match.group(2)
                        self.structure['imports'].add(module)
                    
                    # Find key variables (only major assignments)
                    if match := re.match(variable_pattern, line):
                        var_name = match.group(1)
                        # Filter for important variables
                        if any(keyword in var_name.lower() for keyword in 
                               ['model', 'train', 'test', 'data', 'x_', 'y_', 'scaler', 'history']):
                            self.structure['key_variables'].add(var_name)
    
    def get_task_flow(self):
        """Get the logical flow of tasks"""
        flow = {
            'Task 1': 'Data Loading and EDA',
            'Task 1.01': 'Load dataset from UCI',
            'Task 1.02': 'Class distribution and statistics',
            'Task 2': 'Data Preprocessing',
            'Task 2.01': 'Check missing values',
            'Task 2.02': 'Train/Test split (80/20)',
            'Task 2.03': 'StandardScaler normalization',
            'Task 2.04': 'Noise injection (σ=0.02)',
            'Task 3': 'Model Design and Training',
            'Task 3.01': 'Build MLP (7→64→32→3)',
            'Task 3.02': 'Apply Dropout regularization',
            'Task 3.03': 'Train model (100 epochs)',
            'Task 4': 'Hyperparameter Comparison',
            'Task 4.01': 'Compare dropout rates (0.2 vs 0.4)',
            'Task 5': 'Final Evaluation',
            'Task 5.01': 'Test set evaluation',
            'Task 5.02': 'Classification reports',
            'Task 5.03': 'Confusion matrix',
            'Task 5.04': 'Final recommendations',
            'Task 6': 'K-Fold Cross-Validation',
            'Task 6.01': 'Setup 5-Fold CV',
            'Task 6.02': 'Train across folds',
            'Task 6.03': 'Calculate statistics',
            'Task 6.04': 'Visualize results',
            'Task 6.05': 'Compare with single split'
        }
        return flow
    
    def get_video_segments(self):
        """Map video segments to notebook sections"""
        segments = {
            'Segment 0': {
                'title': 'Introduction',
                'description': 'Assignment header, technical overview',
                'starts_at_task': None,
                'cell_range': [0, 2]
            },
            'Segment 1': {
                'title': 'EDA',
                'description': 'Load data, column naming, class distribution, statistics',
                'starts_at_task': 'Task 1',
                'cell_range': [3, 8]
            },
            'Segment 2': {
                'title': 'Preprocessing',
                'description': 'Missing values, train/test split, scaling',
                'starts_at_task': 'Task 2.01',
                'cell_range': [9, 12]
            },
            'Segment 3': {
                'title': 'Noise Injection',
                'description': 'Data augmentation with Gaussian noise',
                'starts_at_task': 'Task 2.04',
                'cell_range': [13, 14]
            },
            'Segment 4': {
                'title': 'MLP Architecture',
                'description': 'Build neural network (7→64→32→3)',
                'starts_at_task': 'Task 3.01',
                'cell_range': [15, 16]
            },
            'Segment 5': {
                'title': 'Dropout Comparison',
                'description': 'Compare dropout rates 0.2 vs 0.4',
                'starts_at_task': 'Task 4.01',
                'cell_range': [20, 22]
            },
            'Segment 6': {
                'title': 'Training',
                'description': 'Train with early stopping',
                'starts_at_task': 'Task 3.03',
                'cell_range': [18, 19]
            },
            'Segment 7': {
                'title': 'Test Results',
                'description': 'Evaluate accuracy and metrics',
                'starts_at_task': 'Task 5.01',
                'cell_range': [23, 24]
            },
            'Segment 8': {
                'title': 'Confusion Matrix',
                'description': 'Visualize classification results',
                'starts_at_task': 'Task 5.03',
                'cell_range': [26, 27]
            },
            'Segment 9': {
                'title': 'K-Fold Cross-Validation',
                'description': '5-Fold CV for robust evaluation',
                'starts_at_task': 'Task 6',
                'cell_range': [29, 35]
            },
            'Segment 10': {
                'title': 'Wrap-Up',
                'description': 'Final results and conclusion',
                'starts_at_task': None,
                'cell_range': [36, -1]
            }
        }
        return segments
    
    def print_summary(self):
        """Print comprehensive summary"""
        print("=" * 80)
        print("NOTEBOOK STRUCTURE ANALYSIS")
        print("=" * 80)
        print(f"\nNotebook: {self.notebook_path.name}")
        print(f"Total Cells: {self.structure['total_cells']}")
        print(f"  - Markdown: {self.structure['markdown_cells']}")
        print(f"  - Code: {self.structure['code_cells']}")
        
        print("\n" + "=" * 80)
        print("TASK STRUCTURE")
        print("=" * 80)
        for task in self.structure['tasks']:
            print(f"  {task['number']:>6} | {task['title']}")
        
        print("\n" + "=" * 80)
        print("MAIN SECTIONS")
        print("=" * 80)
        for section in self.structure['sections']:
            print(f"  Cell {section['cell_index']:>3} | {section['title']}")
        
        print("\n" + "=" * 80)
        print("KEY IMPORTS")
        print("=" * 80)
        for imp in sorted(self.structure['imports']):
            print(f"  - {imp}")
        
        print("\n" + "=" * 80)
        print("KEY VARIABLES")
        print("=" * 80)
        for var in sorted(self.structure['key_variables']):
            print(f"  - {var}")
        
        print("\n" + "=" * 80)
        print("TASK FLOW")
        print("=" * 80)
        flow = self.get_task_flow()
        for task, desc in flow.items():
            print(f"  {task:>10} → {desc}")
        
        print("\n" + "=" * 80)
        print("VIDEO SEGMENT MAPPING")
        print("=" * 80)
        segments = self.get_video_segments()
        for seg_id, seg_info in segments.items():
            print(f"\n{seg_id}: {seg_info['title']}")
            print(f"  Description: {seg_info['description']}")
            if seg_info['starts_at_task']:
                print(f"  Starts at: {seg_info['starts_at_task']}")
            print(f"  Cell Range: {seg_info['cell_range']}")
    
    def export_structure(self, output_file='notebook_structure.json'):
        """Export structure to JSON"""
        # Convert sets to lists for JSON serialization
        export_data = {
            'notebook_path': str(self.notebook_path),
            'total_cells': self.structure['total_cells'],
            'markdown_cells': self.structure['markdown_cells'],
            'code_cells': self.structure['code_cells'],
            'tasks': self.structure['tasks'],
            'sections': self.structure['sections'],
            'key_variables': sorted(list(self.structure['key_variables'])),
            'imports': sorted(list(self.structure['imports'])),
            'task_flow': self.get_task_flow(),
            'video_segments': self.get_video_segments()
        }
        
        output_path = self.notebook_path.parent / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"\n✓ Structure exported to: {output_path}")
        return output_path


def main():
    # Path to notebook
    notebook_path = Path(__file__).parent / 'Turnin' / 'notebook' / 'Seeds_ML_FINALPRJ_NF1002000.ipynb'
    
    if not notebook_path.exists():
        print(f"ERROR: Notebook not found at {notebook_path}")
        return
    
    # Create analyzer
    analyzer = NotebookAnalyzer(notebook_path)
    
    # Run analysis
    print("Loading notebook...")
    analyzer.load_notebook()
    
    print("Analyzing tasks...")
    analyzer.analyze_tasks()
    
    print("Analyzing sections...")
    analyzer.analyze_sections()
    
    print("Analyzing code...")
    analyzer.analyze_code()
    
    # Print summary
    analyzer.print_summary()
    
    # Export to JSON
    analyzer.export_structure()


if __name__ == '__main__':
    main()
