import Condition
import EVT
import CartesianProductCal
import ScriptGenerator
import os

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

    # Step 5: Run the script to verify the requirements
    imported_module = __import__('requirement_verifier')
    imported_module.main()

if __name__ == '__main__':
    main()