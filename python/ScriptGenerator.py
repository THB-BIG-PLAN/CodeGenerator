import pandas as pd
from enum import Enum
import warnings
import re

warnings.simplefilter(action='ignore', category=UserWarning)
InputSignal = pd.read_excel('ConfigByHand.xlsx', sheet_name='InputSignal')
signal_num = len(InputSignal) + 1
Action = pd.read_excel('ConfigByHand.xlsx', sheet_name='Action')
List = pd.read_excel('Config.xlsx', sheet_name='List')
Condition = pd.read_excel('Config.xlsx', sheet_name='Condition')
Event = pd.read_excel('Config.xlsx', sheet_name='EVT')

def get_action_status_String():
    action_status_String = ''
    for index, row in Action.iterrows():
        if pd.notna(row.loc['Group']):
            len_row = len(row)
            for i in range(2, len_row):
                if pd.notna(row.iloc[i]):
                    action_status_String += f"{row.iloc[i]} = '{row.iloc[i]}'\n"
    return action_status_String

    pass


def get_resultDataFrame_String():
    resultDataFrame_String = ''
    signal_string = ''
    row_number = 0
    for index, row in InputSignal.iterrows():
        signal_string += f"'{row.loc['SignalName']}', "
        row_number += 1
        if row_number == 3:
            signal_string += '\n'
            row_number = 0
    resultDataFrame_String += f"resultDataFrame = pd.DataFrame(columns=[{signal_string}'result'])\n"
    # print(resultDataFrame_String)
    return resultDataFrame_String
    pass


def get_header_String():
    action_status_String = get_action_status_String()
    resultDataFrame_String = get_resultDataFrame_String()
    header_String = f"import pandas as pd\n\n\n{action_status_String}\n{resultDataFrame_String}"
    # print(header_String)
    return header_String
    pass


def get_init_function_signal_string():
    signal_string = ''
    for index, row in InputSignal.iterrows():
        signal_string += f"'{row.loc['SignalName']}', "
    signal_string += "'TIMEFLAGNUM'"
    # print(signal_string)
    return signal_string
    pass


def get_init_function_Macro_string():
    init_macro_string = ''
    for index, row in List.iterrows():
        if pd.notna(row.loc['ConditionMacro']):
            init_macro_string += f"\t\tself.{row.loc['ConditionMacro']} = None\n"
    # print(init_macro_string)
    return init_macro_string
    pass


def get_init_function_Action_String():
    init_Action_String = ''
    for index, row in Action.iterrows():
        if pd.notna(row.loc['Group']):
            action_name = re.sub(r'\(.*?\)', '', row.loc['ActionName'])
            init_Action_String += f"\t\tself.{action_name}_Set = set()\n"
    # print(init_Action_String)
    return init_Action_String


def get_Class_State_init_function_String():
    init_function_signal_string = get_init_function_signal_string()
    init_function_Macro_string = get_init_function_Macro_string()
    Check_Action_String = get_init_function_Action_String()
    class_state_init_function_String = (f"\tdef __init__(self, states_tuple):\n"
                                        f"\t\tkeys = [{init_function_signal_string}]\n"
                                        f"{init_function_Macro_string}\n"
                                        f"{Check_Action_String}\n"
                                        f"\t\tself.current_state = {{key: None for key in keys}}\n"
                                        f"\t\tself.previous_state = {{key: None for key in keys}}\n"
                                        f"\t\tself.update_state(states_tuple)\n")
    # print(class_state_init_function_String)
    return class_state_init_function_String
    pass


def get_update_function_update_signal_string():
    update_signal_string = '\t\t('
    row_number = 0
    for index, row in InputSignal.iterrows():
        update_signal_string += f"self.current_state['{row.loc['SignalName']}']"
        if index < len(InputSignal) - 1:
            update_signal_string += ', '
        row_number += 1
        if row_number == 3:
            update_signal_string += '\n\t\t '
            row_number = 0
    update_signal_string += ") = states_tuple[:9]\n"
    # print(update_signal_string)
    return update_signal_string
    pass


def get_Class_State_update_function_String():
    update_function_update_signal_string = get_update_function_update_signal_string()
    Check_Action_String = get_init_function_Action_String()
    class_state_update_function_String = (f"\tdef update_state(self, states_tuple):\n"
                                          f"\t\tfor k in self.current_state.keys():\n"
                                          f"\t\t\tself.previous_state[k] = self.current_state[k]\n"
                                          f"{update_function_update_signal_string}\n"
                                          f"\t\tself.current_state['TIMEFLAGNUM'] = 0\n"
                                          f"\t\tself.calculate_flags()\n"
                                          f"{Check_Action_String}")
    # print(class_state_update_function_String)
    return class_state_update_function_String
    pass


def get_calculate_function_condition_string():
    calculate_condition_string = ''
    for index, row in Condition.iterrows():
        calculate_condition_string += f"\t\tself.{row.loc['Macro']} = 1 if self."
        if re.search(r'_Pre$', row.loc['SignalName']):
            signal_name = re.sub(r'_Pre$', '', row.loc['SignalName'])
            calculate_condition_string += f"previous_state['{signal_name}']"
        else:
            calculate_condition_string += f"current_state['{row.loc['SignalName']}'] "
        if row.loc['Symbol'] == 'EQ':
            calculate_condition_string += f"== "
        elif row.loc['Symbol'] == 'NEQ' or row.loc['Symbol'] == 'CHANGE':
            calculate_condition_string += f"!= "
        elif row.loc['Symbol'] == 'GREATER':
            calculate_condition_string += f"> "
        elif row.loc['Symbol'] == 'LESS':
            calculate_condition_string += f"< "
        elif row.loc['Symbol'] == 'GREATEROREQ':
            calculate_condition_string += f">= "
        elif row.loc['Symbol'] == 'LESSOREQ':
            calculate_condition_string += f"<= "
        if re.search(r'_SIGNALNUM$', str(row.loc['Threshold'])):
            signal_name = re.sub(r'_SIGNALNUM$', '', row.loc['Threshold'])
            if re.search(r'_Pre$', signal_name):
                signal_name = re.sub(r'_Pre$', '', signal_name)
                calculate_condition_string += f"self.previous_state['{signal_name}']"
            else:
                calculate_condition_string += f"self.current_state['{signal_name}']"
        else:
            calculate_condition_string += f"{row.loc['Threshold']}"
        calculate_condition_string += " else 0\n"
    # print(calculate_condition_string)
    return calculate_condition_string

    pass


def get_timeflag_condition_string(row):
    timeflag_condition_string = ''
    for index in range(3, len(row)):
        if pd.notna(row.iloc[index]):
            if index > 3:
                timeflag_condition_string += " and "
            timeflag_condition_string += f"self.{row.iloc[index]}"
    # print(timeflag_condition_string)
    return timeflag_condition_string
    pass


def get_calculate_function_timeflag_string():
    timeflag_update_string = ''
    for index, row in Event.iterrows():
        for i in range(1, 3):
            if pd.notna(row.iloc[i]) and re.search(r'addTimer', str(row.iloc[i])):
                timeflag_update_string += (f"\t\tif {get_timeflag_condition_string(row)}:\n"
                                           f"\t\t\tself.current_state['TIMEFLAGNUM'] += 1\n")
    # print(timeflag_update_string)
    timeflag_update_string += f"\t\tself.TIMEFLAGNUM_EQ_0 = 1 if self.current_state['TIMEFLAGNUM'] == 0 else 0\n"
    return timeflag_update_string
    pass


def get_calculate_flags_function_String():
    condition_update_string = get_calculate_function_condition_string()
    timeflag_update_string = get_calculate_function_timeflag_string()
    calculate_flags_function_String = (f"\tdef calculate_flags(self):\n"
                                       f"{condition_update_string}\n"
                                       f"{timeflag_update_string}")
    # print(calculate_flags_function_String)
    return calculate_flags_function_String
    pass


def get_get_current_state_function_String():
    get_current_state_function_String = ("\tdef get_current_state(self, param):\n"
                                         "\t\treturn self.current_state.get(param)\n")
    return get_current_state_function_String
    pass


def get_get_previous_state_function_String():
    get_previous_state_function_String = ("\tdef get_previous_state(self, param):\n"
                                          "\t\treturn self.previous_state.get(param)\n")
    return get_previous_state_function_String
    pass


def get_Class_State_String():
    init_function_String = get_Class_State_init_function_String()
    update_function_String = get_Class_State_update_function_String()
    calculate_flags_function_String = get_calculate_flags_function_String()
    get_current_state_function_String = get_get_current_state_function_String()
    get_previous_state_function_String = get_get_previous_state_function_String()
    Class_State_String = (f"class State:\n"
                          f"{init_function_String}\n"
                          f"{update_function_String}\n"
                          f"{calculate_flags_function_String}\n"
                          f"{get_current_state_function_String}\n"
                          f"{get_previous_state_function_String}\n")
    # print(Class_State_String)
    return Class_State_String
    pass


def get_Class_ComplexRule_String():
    Class_ComplexRule_String = """
class ComplexRule:
    def __init__(self, condition):
        self.condition = condition

    def check_condition(self, state):
        try:
            self.condition(state)
        except Exception as e:
            print(f"执行规则时发生错误: {e}")
    """
    # print(Class_ComplexRule_String)
    return Class_ComplexRule_String
    pass


def get_Class_ConflictDetector_init_function_String():
    init_function_String = '''
    def __init__(self, rules):
        self.rules = rules
        self.device_state = State(tuple(0 for _ in range(signal_num)))
    '''
    return init_function_String
    pass


def get_detect_and_execute_function_Action_verify_string():
    detect_and_execute_function_Action_verify_string = ''
    for index, row in Action.iterrows():
        if pd.notna(row.loc['Group']):
            action_name = re.sub(r'\(.*?\)', '', row.loc['ActionName'])
            detect_and_execute_function_Action_verify_string += (f"\t\tif len(self.device_state.{action_name}_Set) > 1\n"
                                                                 f"\t\t\tresult = 'Conflict'\n"
                                                                 f"\t\telif len(self.device_state.{action_name}_Set) == 1\n"
                                                                 f"\t\t\tresult = self.device_state.LGL_Set_Set.pop()\n"
                                                                 f"\t\telif len(self.device_state.{action_name}_Set) == 0\n"
                                                                 f"\t\t\tresult = 'No action needed'\n")
    # print(detect_and_execute_function_Action_verify_string)
    return detect_and_execute_function_Action_verify_string
    pass


def get_Class_ConflictDetector_detect_and_execute_function_String():
    detect_and_execute_function_String = ''
    detect_and_execute_function_Action_verify_string = get_detect_and_execute_function_Action_verify_string()
    detect_and_execute_function_String += '''    
    def detect_and_execute(self, states_tuple):
        result = ''
        self.device_state.update_state(states_tuple)
        for rule in self.rules:
            rule.check_condition(self.device_state)
    '''
    detect_and_execute_function_String += detect_and_execute_function_Action_verify_string
    pass


def get_Class_ConflictDetector_String():
    init_function_String = get_Class_ConflictDetector_init_function_String()
    detect_and_execute_function_String = get_Class_ConflictDetector_detect_and_execute_function_String()
    pass


def main():
    Header_String = get_header_String()
    Class_State_String = get_Class_State_String()
    Class_ComplexRule_String = get_Class_ComplexRule_String()
    Class_ConflictDetector = get_Class_ConflictDetector_String()


if __name__ == "__main__":
    main()
