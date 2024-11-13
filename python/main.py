import Condition
import EVT
import CartesianProductCal
import ScriptGenerator
import os
import sys
import importlib.util

def main():
    # Step 1: Create the Dictionaries for Event and Condition
    EVTFilePath = 'EVT'
    ConditionFilePath = 'Condition'
    if not os.path.exists(EVTFilePath):
        os.makedirs(EVTFilePath)
    if not os.path.exists(ConditionFilePath):
        os.makedirs(ConditionFilePath)
    # Step 2: Generate Event and Condition code Files
    Condition.main()
    EVT.main()

    # Step 3: Generate Cartesian Product of Event and Condition
    CartesianProductCal.main()

    # Step 4: Generate requirement verifier script
    ScriptGenerator.main()
    print("requirement_verifier.py generated successfully.")
    input()
    # Step 5: Run the script to verify the requirements

    current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

    script_path = os.path.join(current_dir, 'requirement_verifier.py')

    spec = importlib.util.spec_from_file_location('requirement_verifier', script_path)
    imported_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(imported_module)

    imported_module.main()



if __name__ == '__main__':
    main()
