import os

import pandas as pd
import re
import warnings

warnings.simplefilter(action='ignore', category=UserWarning)
CONFIG_PATH = 'Config.xlsx'
EVENTS_HEADER_PATH = 'EVT/EVT.h'
EVENTS_SOURCE_PATH = 'EVT/EVT.c'
Events_DataFrame = pd.read_excel(CONFIG_PATH, sheet_name='EVT')
ConstMacro_DataFrame = pd.read_excel(CONFIG_PATH, sheet_name='ConstMacro')
EVENTS_SOURCE_HEADER = '''
#include <Type_define.h>
#include <stdlib.h>
#include <string.h>
#include "EVT/Timer/Timer.api.h"
#include "EVT/Event/EVT.h"
#include "EVT/Logic/Logic.h"
#include "EVT/Condition/Condition.h"
'''


def write_event_header():
    Events_Header_String = '#ifndef EVT_EVENT_EVT_\n#define EVT_EVENT_EVT_\n\n'
    for index, row in Events_DataFrame.iterrows():
        Events_Header_String += f"extern void {row.loc['EVTName']}();\n"
    Events_Header_String += '\n\n#endif // EVT_EVENT_EVT_\n'
    if not os.path.exists('EVT'):
        os.makedirs('EVT')
    with open(EVENTS_HEADER_PATH, 'w') as f:
        f.write(Events_Header_String)
    pass


def get_constMacros_String():
    ConstMacro_String = ''
    for index, row in ConstMacro_DataFrame.iterrows():
        ConstMacro_String += f"#define {row.loc['Macro']} {row.loc['value']}\n"
    return ConstMacro_String
    pass


def get_functions_declare_String():
    Event_function_declare_String = ''
    for index, row in Events_DataFrame.iterrows():
        Event_function_declare_String += f"void {row.loc['EVTName']}();\n"
    return Event_function_declare_String
    pass


def get_action_List(row):
    Action_String_List = []
    for i in range(1, 3):
        if pd.notna(row.iloc[i]):
            Action_String_List.append(row.iloc[i])
    return Action_String_List


def get_condition_String(row):
    Condition_String = '    if ('
    for i in range(3, row.shape[0]):
        if pd.isnull(row.iloc[i]):
            break
        if i == 3:
            Condition_String += f"EVT_flag->ConditionFlag[{row.iloc[i]}]"
        else:
            Condition_String += f" && \n        EVT_flag->ConditionFlag[{row.iloc[i]}]"
    Condition_String += ')\n'
    # print(Condition_String)
    return Condition_String


def get_functions_define_String():
    Event_function_define_String = ''
    for index, row in Events_DataFrame.iterrows():
        Event_function_define_String += f"void {row.loc['EVTName']}()\n{{\n"
        if pd.isnull(row.loc['Condition0']):
            Action_String_List = get_action_List(row)
            for Action_String in Action_String_List:
                Event_function_define_String += f"    {Action_String};\n"
        else:
            Condition_String = get_condition_String(row)
            Event_function_define_String += f"{Condition_String}    {{\n"
            Action_String_List = get_action_List(row)
            for Action_String in Action_String_List:
                Event_function_define_String += f"        {Action_String};\n"
            Event_function_define_String += "    }\n"
        Event_function_define_String += '}\n\n'
    return Event_function_define_String
    pass


def write_event_source():
    ConstMacro_String = get_constMacros_String()
    Functions_declare_String = get_functions_declare_String()
    Functions_define_String = get_functions_define_String()
    Events_Source_String = f"{EVENTS_SOURCE_HEADER}\n\n{ConstMacro_String}\n\n{Functions_declare_String}\n\n{Functions_define_String}"
    if not os.path.exists('EVT'):
        os.makedirs('EVT')
    with open(EVENTS_SOURCE_PATH, 'w') as f:
        f.write(Events_Source_String)
    pass


def main():
    write_event_header()
    write_event_source()
    pass


if __name__ == '__main__':
    main()
