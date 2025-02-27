#!/usr/local/bin/python
# coding: GBK
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
InputDataFrame = pd.read_excel(CONFIG_PATH, sheet_name='InputSignal')
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
            Condition_String += f"P_SignalsAndConditions->ConditionFlag[{row.iloc[i]}]"
        else:
            Condition_String += f" && \n        P_SignalsAndConditions->ConditionFlag[{row.iloc[i]}]"
    Condition_String += ')\n'
    # print(Condition_String)
    return Condition_String


def extract_function_parameters(action_str):
    # 提取函数参数，假设每个函数只有一个参数列表，并且参数之间用逗号分隔
    params = []
    actions = action_str.split(';')
    for action in actions:
        if '(' in action and ')' in action:
            start = action.find('(') + 1
            end = action.find(')')
            param_str = action[start:end].strip()
            params.extend([param.strip() for param in param_str.split(',')])
    return params


def get_Event_condition_string(row):
    Event_Condition_String = ''
    for i in range(3, row.shape[0]):
        if pd.isnull(row.iloc[i]):
            break
        if i == 3:
            Event_Condition_String = f"    if (P_SignalsAndConditions->ConditionFlag[{row.iloc[i]}]"
        else:
            Event_Condition_String += f" && \n        P_SignalsAndConditions->ConditionFlag[{row.iloc[i]}]"
    if Event_Condition_String != '':
        Event_Condition_String += ')\n'
    # print(Event_Condition_String)
    return Event_Condition_String
    pass


def create_param_mapping(row):
    # 创建参数映射字典
    param_mapping = {}
    for idx, row_input in InputDataFrame.iterrows():
        if row_input['SignalName'] in row:
            param_mapping[row_input[
                'SignalName']] = f"P_SignalsAndConditions->Signal_{row_input['Type']}[{row_input['SignalName']}_SIGNALNUM]"
    return param_mapping


def replace_params_in_action(action, param_mapping):
    # 替换参数
    if '(' in action and ')' in action:
        start = action.find('(')
        end = action.find(')')
        function_name = action[:start].strip()
        params = action[start + 1:end].strip().split(',')
        modified_params = [param_mapping.get(param.strip(), param.strip()) for param in params]
        modified_action = f"{function_name}({', '.join(modified_params)})"
        return modified_action
    return action


def get_Event_Action_List(row):
    if pd.isnull(row['Action']):
        return []

    # 提取初始参数列表
    Action_params_list = extract_function_parameters(row['Action'])

    # 创建参数映射字典
    param_mapping = create_param_mapping(Action_params_list)

    # 分割动作字符串并替换参数
    actions = row['Action'].split(';')
    modified_actions = [replace_params_in_action(action, param_mapping) for action in actions]

    # 合并修改后的动作字符串

    return modified_actions


def get_Event_source_code():
    Event_source_code = ''
    condition_string = ''
    Event_Action_List = []
    for index, row in Events_DataFrame.iterrows():
        Event_source_code += f"void {row.loc['EVTName']}()\n{{\n"
        if pd.notna(row.loc['Condition0']):
            condition_string = get_Event_condition_string(row)
        else:
            condition_string = ''
        Event_source_code += condition_string
        Event_Action_List = get_Event_Action_List(row)
        if condition_string != '':
            Event_source_code += "    {\n"
        for action in Event_Action_List:
            if condition_string != '':
                Event_source_code += f"        {action}\n"
            else:
                Event_source_code += f"    {action}\n"
        if condition_string != '':
            Event_source_code += "    }\n"
        Event_source_code += "}\n\n"

    print(Event_source_code)
    return Event_source_code
    pass


def write_event_source():
    ConstMacro_String = get_constMacros_String()
    Functions_declare_String = get_functions_declare_String()
    Functions_define_String = get_Event_source_code()
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
