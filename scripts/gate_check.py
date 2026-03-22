import os
import sys
import re

def parse_control_matrix():
    """Parses the MCSB markdown matrix to find 'Must' controls."""
    matrix_path = os.path.join(os.path.dirname(__file__), '../controls/MCSB-control-matrix.md')

    if not os.path.exists(matrix_path):
        print(f"Error: Control matrix not found at {matrix_path}")
        return []

    must_controls = []

    with open(matrix_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Basic table parsing assuming format: | ID | ... | Priority | ...
            if '|' in line and 'Must' in line:
                parts = [p.strip() for p in line.split('|')]
                # Check if this line looks like a control row (skip headers)
                if len(parts) > 7 and parts[1] != 'Control ID':
                    control = {
                        'id': parts[1],
                        'mcsb_id': parts[2],
                        'name': parts[4],
                        'priority': parts[7]
                    }
                    if control['priority'] == 'Must':
                        must_controls.append(control)

    return must_controls

def main():
    print("--- starting iac-azure-security-framework gate check ---")

    must_controls = parse_control_matrix()
    print(f"Loaded {len(must_controls)} 'Must' priority controls from Matrix.")

    # Placeholder: Logic to load checkov results would go here
    # checkov_results = json.load(open('checkov_report.json'))

    print("Validation complete. (Simulation mode)")
    sys.exit(0)

if __name__ == "__main__":
    main()
