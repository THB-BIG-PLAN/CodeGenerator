import re
import pandas as pd
import openpyxl
import warnings

# 忽略警告
warnings.simplefilter(action='ignore', category=UserWarning)
CONFIG_PATH = 'config.xlsx'
EvnetDataFrame = pd.read_excel(CONFIG_PATH, sheet_name='EVT')
OutputDataFrame = pd.read_excel(CONFIG_PATH, sheet_name='OutputInitializer')
InputDataFrame = pd.read_excel(CONFIG_PATH, sheet_name='InputSignal')


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


def write_Event_source_code():
    Event_source_code = ''
    condition_string = ''
    Event_Action_List = []
    for index, row in EvnetDataFrame.iterrows():
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
    pass


def main():
    write_Event_source_code()


if __name__ == "__main__":
    main()
