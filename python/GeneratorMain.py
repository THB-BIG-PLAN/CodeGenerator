import Condition
import EVT
import CartesianProductCal
import ScriptGenerator
import os
import sys
import importlib.util
import Initializer
import Logic

def main():
    # Step 1: Create the Dictionaries for Event and Condition
    Initializer.main()
    LogicFilePath = 'Logic'
    EVTFilePath = 'EVT'
    ConditionFilePath = 'Condition'
    if not os.path.exists(LogicFilePath):
        os.makedirs(LogicFilePath)
    if not os.path.exists(EVTFilePath):
        os.makedirs(EVTFilePath)
    if not os.path.exists(ConditionFilePath):
        os.makedirs(ConditionFilePath)
    # Step 2: Generate Event and Condition code Files
    Logic.main()
    Condition.main()
    EVT.main()
    print("Code Generation Complete,Press Enter to Exit")
    os.system("pause")
    #
    # # Step 3: Generate Cartesian Product of Event and Condition
    # CartesianProductCal.main()
    #
    # # Step 4: Generate requirement verifier script
    # ScriptGenerator.main()
    #
    # # Step 5: Run the script to verify the requirements
    #
    # current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    #
    # script_path = os.path.join(current_dir, 'requirement_verifier.py')
    #
    # spec = importlib.util.spec_from_file_location('requirement_verifier', script_path)
    # imported_module = importlib.util.module_from_spec(spec)
    # spec.loader.exec_module(imported_module)
    #
    # imported_module.main()
    # print("The requirements check is completed and the results have been output to result.xlsx")
    # print("Press any key to exit")
    # input()


if __name__ == '__main__':
    main()
