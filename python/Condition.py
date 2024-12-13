import os
from collections import defaultdict

import pandas as pd
import openpyxl
import warnings

# 忽略警告
warnings.simplefilter(action='ignore', category=UserWarning)
CONFIG_PATH = 'Config.xlsx'
ListDataFrame = pd.read_excel(CONFIG_PATH, sheet_name='List')
ConditionDataFrame = pd.read_excel(CONFIG_PATH, sheet_name='Condition')
SignalDataFrame = pd.read_excel(CONFIG_PATH, sheet_name='InputSignal')
TimeFlagDataFrame = pd.read_excel(CONFIG_PATH, sheet_name='TimeFlag')
CONDITION_HEADER_PATH = 'Condition/Condition.h'
CONDITION_SOURCE_PATH = 'Condition/Condition.c'
Condition_Header_Header_String = '''
#ifndef CONDITION_H_
#define CONDITION_H_
#include <Type_define.h>
#include "EVT/Event/EVT.h"
#include "EVT/Logic/Logic.h"
#include <sgn/signal_api.h>
#include <stdbool.h>
#include <stdint.h>

'''
Condition_Source_Header_String = '''
#include "EVT/Condition/Condition.h"\n\n
'''


def get_signal_macro_string():
    Signal_Macro_String = ''
    Signal_Macro_Index = 0
    Signal_Type = None
    Signal_Type_dict = {row['VariableType']: 0
                        for index, row in ListDataFrame.iterrows()
                        if pd.notna(row['VariableType']) and row['VariableType'] != ''}
    for index, row in SignalDataFrame.iterrows():
        if Signal_Type is None or Signal_Type != row.loc['Type']:
            Signal_Type = row.loc['Type']
            Signal_Macro_Index = 0
        Signal_Macro_String += f"#define {row.loc['Macro']} {Signal_Macro_Index}\n"
        Signal_Type_dict[Signal_Type] += 1
        Signal_Macro_Index += 1
    Signal_Macro_String += '\n\n'
    for key, value in Signal_Type_dict.items():
        Signal_Macro_String += f"#define {key.upper()}_SIGNAL_NUMBER {value}\n"
    Signal_Macro_String += '\n\n'
    # print(Signal_Macro_String)
    return Signal_Macro_String
    pass


def get_Condition_Struct_String():
    Condition_Struct_String = ''
    for index, row in ListDataFrame.iterrows():
        if pd.notna(row['VariableType']) and row['VariableType'] != '':
            Struct_String = f"typedef struct \n{{\n"
            Struct_String += f"\t{row['VariableType']} Threshold;\n"
            Struct_String += f"\tuint8 Symbol;\n"
            Struct_String += f"\tvoid (*EVT)();\n"
            Struct_String += f"\tuint8 ConditionIndex;\n"
            Struct_String += f"}}{row.loc['VariableType']}Condition;\n\n"
            Condition_Struct_String += Struct_String
    Condition_Struct_String += "typedef struct \n{\n"
    Condition_Struct_String += "\tuint8 SignalIndex;\n"
    Condition_Struct_String += "\tuint8 Symbol;\n"
    Condition_Struct_String += "\tvoid (*EVT)();\n"
    Condition_Struct_String += "\tuint8 ConditionIndex;\n"
    Condition_Struct_String += "}SignalCondition;\n\n"

    Condition_Struct_String += "typedef struct \n{\n"
    Condition_Struct_String += "\tBit Threshold;\n"
    Condition_Struct_String += "\tuint8 Symbol;\n"
    Condition_Struct_String += "\tvoid (*EVT)();\n"
    Condition_Struct_String += "\tuint8 ConditionIndex;\n"
    Condition_Struct_String += "}TimeOutCondition;\n\n"
    # print(Condition_Struct_String)
    return Condition_Struct_String
    pass


def get_Condition_Info_String():
    Condition_Info_String = ''
    for index, row in ListDataFrame.iterrows():
        if pd.notna(row['VariableType']) and row['VariableType'] != '':
            Condition_Info_Struct_String = f"typedef struct \n{{\n"
            Condition_Info_Struct_String += f"\tuint8 SignalIndex;\n"
            Condition_Info_Struct_String += f"\tuint8 length;\n"
            Condition_Info_Struct_String += f"\t{row.loc['VariableType']}Condition *Conditions;\n"
            Condition_Info_Struct_String += f"}}{row.loc['VariableType']}SignalConditionInfo;\n\n"
            Condition_Info_String += Condition_Info_Struct_String
    Condition_Info_String += "typedef struct \n{\n"
    Condition_Info_String += "\tuint8 SignalIndex;\n"
    Condition_Info_String += "\tuint8 length;\n"
    Condition_Info_String += "\tSignalCondition *Conditions;\n"
    Condition_Info_String += "}SignalConditionInfo;\n\n"
    # print(Condition_Info_String)
    return Condition_Info_String
    pass


def get_Signals_And_Conditions_String():
    Signals_And_Conditions_String = 'typedef struct \n{\n'
    for index, row in ListDataFrame.iterrows():
        if pd.notna(row['VariableType']) and row['VariableType'] != '':
            Signals_And_Conditions_String += f"\t{row.loc['VariableType']} Signal_{row.loc['VariableType']}[{row.loc['VariableType'].upper()}_SIGNAL_NUMBER];\n"
    Signals_And_Conditions_String += "\n"
    Signals_And_Conditions_String += "\tuint8 TimeOutFlagNum;\n"
    Signals_And_Conditions_String += "\tBit TimeOutFlag[TIME_FLAG_NUMBER];\n"
    Signals_And_Conditions_String += "\tBit ConditionFlag[CONDITION_NUMBER];\n"
    Signals_And_Conditions_String += "}SignalsAndConditions;\n\n"
    # print(Signals_And_Conditions_String)
    return Signals_And_Conditions_String
    pass


def get_Condition_Info_Array_String():
    Condition_Info_Array_String = ''
    for index, row in ListDataFrame.iterrows():
        if pd.notna(row['VariableType']) and row['VariableType'] != '':
            Condition_Info_Array_String += f"static const {row.loc['VariableType']}SignalConditionInfo {row.loc['VariableType']}ConditionInfoArray[{row.loc['VariableType'].upper()}_SIGNAL_NUMBER];\n"
    Condition_Info_Array_String += "\n\n"
    for index, row in ListDataFrame.iterrows():
        if pd.notna(row['VariableType']) and row['VariableType'] != '':
            Condition_Info_Array_String += f"static const SignalConditionInfo {row.loc['VariableType']}SignalConditionInfoArray[{row.loc['VariableType'].upper()}_SIGNAL_NUMBER];\n"
    Condition_Info_Array_String += "\n\n"
    Condition_Info_Array_String += "static const TimeOutCondition TimeOutActionArray[TIME_FLAG_NUMBER];\n"
    # print(Condition_Info_Array_String)
    return Condition_Info_Array_String
    pass


def get_time_flag_macro_string():
    Time_flag_macro_string = ''
    for index, row in TimeFlagDataFrame.iterrows():
        Time_flag_macro_string += f"#define {row.loc['FlagName']} {index}\n"
    Time_flag_macro_string += '\n\n'
    # print(Time_flag_macro_string)
    return Time_flag_macro_string
    pass


def get_condition_macro_string():
    Condition_Macro_String = ''
    for index, row in ListDataFrame.iterrows():
        if pd.notna(row.loc['ConditionMacro']) and row['ConditionMacro'] != '':
            Condition_Macro_String += f"#define {row.loc['ConditionMacro']} {index}\n"
    Condition_Macro_String += '\n\n'
    # print(Condition_Macro_String)
    return Condition_Macro_String
    pass


def get_symbol_macro_string():
    Symbol_macro_string = ''
    for index, row in ListDataFrame.iterrows():
        if pd.notna(row.loc['Symbol']) and row['Symbol'] != '':
            Symbol_macro_string += f"#define {row.loc['Symbol']} {index}\n"
    Symbol_macro_string += '\n\n'
    # print(Symbol_macro_string)
    return Symbol_macro_string
    pass


def write_condition_header():
    Signal_Macro_String = get_signal_macro_string()
    Symbol_Macro_String = get_symbol_macro_string()
    Condition_Macro_String = get_condition_macro_string()
    TimeOut_Flag_Macro_String = get_time_flag_macro_string()
    Time_Flag_Number_Macro_String = f"#define TIME_FLAG_NUMBER {len(TimeFlagDataFrame)}\n"
    Condition_Number_Macro_String = f"#define CONDITION_NUMBER {len(ListDataFrame)}\n"
    Signal_Condition_Struct_String = get_Condition_Struct_String()
    Signal_Condition_Info_String = get_Condition_Info_String()
    Signals_And_Conditions_String = get_Signals_And_Conditions_String()
    Signal_Condition_Info_Array_String = get_Condition_Info_Array_String()
    if not os.path.exists('Condition'):
        os.makedirs('Condition')
    with open(CONDITION_HEADER_PATH, 'w') as f:
        f.write(Condition_Header_Header_String)
        f.write(Signal_Macro_String)
        f.write(Symbol_Macro_String)
        f.write(Condition_Macro_String)
        f.write(TimeOut_Flag_Macro_String)
        f.write(Time_Flag_Number_Macro_String)
        f.write(Condition_Number_Macro_String)
        f.write(Signal_Condition_Struct_String)
        f.write(Signal_Condition_Info_String)
        f.write(Signals_And_Conditions_String)
        f.write(Signal_Condition_Info_Array_String)
        f.write('extern SignalsAndConditions *P_SignalsAndConditions;\n')
        f.write("#endif\n")
    pass


def get_signal_condition_string():
    Signal_Name = None
    Signal_Type = None
    Signal_Condition_String = ''
    Condition_Number = 0
    Condition_String = ''
    for index, row in SignalDataFrame.iterrows():
        Signal_Name = row.loc['SignalName']
        Signal_Type = row.loc['Type']
        filtered_df = ConditionDataFrame.loc[ConditionDataFrame['SignalName'] == Signal_Name]
        for filtered_index, filtered_row in filtered_df.iterrows():
            if filtered_row.loc['ThresholdType'] != 'CONDITION_TYPE_SIGNAL':
                if Condition_Number != 0:
                    Condition_String += " , "
                Condition_String += f"{{{filtered_row.loc['Threshold']}, {filtered_row.loc['Symbol']}, {filtered_row.loc['EVT']}, {filtered_row.loc['Macro']}}}"
                Condition_Number += 1
        Signal_Condition_String += f"const {Signal_Type}Condition {Signal_Name}_Conditions[{Condition_Number}] = {{{Condition_String}}};\n"
        Condition_String = ''
        Condition_Number = 0
    Signal_Condition_String += "\n\n"
    for index, row in SignalDataFrame.iterrows():
        Signal_Name = row.loc['SignalName']
        Signal_Type = row.loc['Type']
        filtered_df = ConditionDataFrame.loc[ConditionDataFrame['SignalName'] == Signal_Name]
        for filtered_index, filtered_row in filtered_df.iterrows():
            if filtered_row.loc['ThresholdType'] == 'CONDITION_TYPE_SIGNAL':
                if Condition_Number != 0:
                    Condition_String += " , "
                Condition_String += f"{{{filtered_row.loc['Threshold']}, {filtered_row.loc['Symbol']}, {filtered_row.loc['EVT']}, {filtered_row.loc['Macro']}}}"
                Condition_Number += 1
        Signal_Condition_String += f"const SignalCondition {Signal_Name}_SignalConditions[{Condition_Number}] = {{{Condition_String}}};\n"
        Condition_String = ''
        Condition_Number = 0
    Signal_Condition_String += "\n\n"
    # print(Signal_Condition_String)
    return Signal_Condition_String
    pass


def get_condition_number_type_info_string(matching_type_rows):
    condition_number_type_info_string = ''
    Signal_Name = None
    Condition_Length = 0
    matching_type_rows.reset_index(inplace=True, drop=True)
    for index, row in matching_type_rows.iterrows():
        Signal_Name = row.loc['SignalName']
        filtered_df = ConditionDataFrame.loc[ConditionDataFrame['SignalName'] == Signal_Name]
        filtered_df = filtered_df[filtered_df['ThresholdType'] != 'CONDITION_TYPE_SIGNAL']
        Condition_Length = len(filtered_df)
        if index != 0:
            condition_number_type_info_string += " ,\n"
        condition_number_type_info_string += f"{{{Signal_Name}_SIGNALNUM, {Condition_Length}, {Signal_Name}_Conditions}}"
    # print(condition_number_type_info_string)
    return condition_number_type_info_string

    pass


def get_signal_number_condition_info():
    signal_number_condition_info_string = ''
    Signal_Name = None
    Signal_Type = None
    Type_Number = 0
    signal_info_String = ''
    for index, row in ListDataFrame.iterrows():
        if pd.notna(row['VariableType']) and row['VariableType'] != '':
            Signal_Type = row['VariableType']
            matching_type_rows = SignalDataFrame[SignalDataFrame['Type'] == Signal_Type]
            Type_Number = len(matching_type_rows)
            Condition_Number_Type_Info_String = get_condition_number_type_info_string(matching_type_rows)
            signal_number_condition_info_string += f"static const {Signal_Type}SignalConditionInfo {Signal_Type}ConditionInfoArray[{Type_Number}] = {{\n{Condition_Number_Type_Info_String} \n}};\n\n"
    # print(signal_number_condition_info_string)
    return signal_number_condition_info_string
    pass


def get_condition_signal_type_info_string(matching_type_rows):
    condition_signal_type_info_string = ''
    Signal_Name = None
    Condition_Length = 0
    matching_type_rows.reset_index(inplace=True, drop=True)
    for index, row in matching_type_rows.iterrows():
        Signal_Name = row.loc['SignalName']
        filtered_df = ConditionDataFrame.loc[ConditionDataFrame['SignalName'] == Signal_Name]
        filtered_df = filtered_df[filtered_df['ThresholdType'] == 'CONDITION_TYPE_SIGNAL']
        Condition_Length = len(filtered_df)
        if index != 0:
            condition_signal_type_info_string += " ,\n"
        condition_signal_type_info_string += f"{{{Signal_Name}_SIGNALNUM, {Condition_Length}, {Signal_Name}_Conditions}}"
    # print(condition_signal_type_info_string)
    return condition_signal_type_info_string
    pass


def get_signal_signal_condition_info():
    signal_signal_condition_info_string = ''
    Signal_Name = None
    Signal_Type = None
    Type_Number = 0
    signal_info_String = ''
    for index, row in ListDataFrame.iterrows():
        if pd.notna(row['VariableType']) and row['VariableType'] != '':
            Signal_Type = row['VariableType']
            matching_type_rows = SignalDataFrame[SignalDataFrame['Type'] == Signal_Type]
            Type_Number = len(matching_type_rows)
            Condition_Number_Type_Info_String = get_condition_signal_type_info_string(matching_type_rows)
            signal_signal_condition_info_string += f"static const SignalConditionInfo {Signal_Type}SignalConditionInfoArray[{Type_Number}] = {{\n{Condition_Number_Type_Info_String} \n}};\n\n"
    # print(signal_signal_condition_info_string)
    return signal_signal_condition_info_string
    pass


def write_condition_source():
    signal_condition_string = get_signal_condition_string()
    signal_number_condition_info_string = get_signal_number_condition_info()
    signal_signal_condition_info_string = get_signal_signal_condition_info()

    if not os.path.exists('Condition'):
        os.makedirs('Condition')
    with open(CONDITION_SOURCE_PATH, 'w') as f:
        f.write('#include "EVT/Condition/Condition.h"\n\n')
        f.write(signal_condition_string)
        f.write(signal_number_condition_info_string)
        f.write(signal_signal_condition_info_string)
    pass


def main():
    write_condition_header()
    write_condition_source()
    pass


if __name__ == '__main__':
    main()
