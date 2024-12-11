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


def write_condition_header():
    global Condition_Header_Header_String

    # SignalIndex
    Signal_Number_Macro_String = ''
    Signal_Index = 0
    Signal_Type = None
    for i, row in SignalDataFrame.iterrows():
        if Signal_Type is None:
            Signal_Type = row.loc['Type']
        if row.loc['Type'] != Signal_Type:
            Signal_Type = row.loc['Type']
            Signal_Index = 0
        Signal_Number_Macro_String += f"#define {row.loc['SignalName']} {Signal_Index}\n"
        Signal_Index += 1
    # print(Signal_Number_Macro_String)

    # ConditionMacro
    ConditionNum = 0
    Threshold_Type_Macro_String = ''
    Condition_Macro_String = ''
    Symbol_Macro_String = ''
    Time_Macro_String = ''
    for i, row in ListDataFrame.iterrows():
        if pd.notna(row.loc['Symbol']):
            Symbol_Macro_String += f"#define {row.loc['Symbol']} {i}\n"
        if pd.notna(row.loc['ThresholdType']):
            Threshold_Type_Macro_String += f"#define {row.loc['ThresholdType']} {i}\n"
        if pd.notna(row.loc['ConditionMacro']):
            Condition_Macro_String += f"#define {row.loc['ConditionMacro']} {i}\n"
            ConditionNum += 1

    # TimeFlag
    for i, row in TimeFlagDataFrame.iterrows():
        if pd.notna(row.loc['FlagName']):
            Time_Macro_String += f"#define {row.loc['FlagName']} {i}\n"

    Type = None
    Type_Num = 0
    EVT_FLAG_String = ''
    for i, row in SignalDataFrame.iterrows():
        if Type is None:
            Type = row.loc['Type']
        if row.loc['Type'] != Type:
            EVT_FLAG_String += f"    {Type} Signal_{Type}[{Type_Num}];\n"
            Type_Num = 0
            Type = row.loc['Type']
        Type_Num += 1
        if i == len(SignalDataFrame) - 1:
            EVT_FLAG_String += f"    {Type} Signal_{Type}[{Type_Num}];\n"
    SignalNum = len(SignalDataFrame)
    TimeFlagNum = len(TimeFlagDataFrame)

    # combine all strings
    Condition_Header_Header_String += Signal_Number_Macro_String + '\n'
    Condition_Header_Header_String += Threshold_Type_Macro_String + '\n'
    Condition_Header_Header_String += Condition_Macro_String + '\n'
    Condition_Header_Header_String += Symbol_Macro_String + '\n'
    Condition_Header_Header_String += Time_Macro_String + '\n'
    Condition_Header_Header_String += f"#define SIGNAL_NUMBER {SignalNum}\n"
    Condition_Header_Header_String += f"#define TIME_FLAG_NUMBER {TimeFlagNum}\n"
    Condition_Header_Header_String += f"#define CONDITION_NUMBER {ConditionNum}\n"
    Condition_Header_Header_String += '''
typedef struct Condition {
Bit Type;
uint8 Threshold;
uint8 Symbol;
void (*EVT)();
uint8 ConditionID;
} Condition;

enum SignalType {
    Type_Bit,
    Type_double,
    Type_EEPROM_U8,
    Type_int16,
    Type_int32,
    Type_int64,
    Type_int8,
    Type_single,
    Type_uint16,
    Type_uint32,
    Type_uint64,
    Type_uint8,
}

typedef struct SignalCondition {
    uint8 Signal;
    enum SignalType Type;
    uint8 Len;
    const Condition* Condition;
} SignalCondition;

'''
    # define EVT_FLAG struct
    Condition_Header_Header_String += (f"typedef struct EVT_FLAG {{\n"
                                       f"{EVT_FLAG_String}"
                                       f"    uint8 TimeOutFlagNum;\n"
                                       f"    Bit TimeOutFlag[TIMEOUT_NUM];\n"
                                       f"    Bit ConditionFlag[CONDITION_NUMBER];\n"
                                       f"}} EVT_FLAG;\n\n"
                                       f"extern EVT_FLAG* EVT_flag;\n"
                                       f"static const SignalCondition SignalConditionArray[SIGNAL_NUM];\n"
                                       f"static const Condition TimeOutActionArray[TIMEOUT_NUM];\n"
                                       f"#endif // CONDITION_H_\n")

    # print(Condition_Header_Header_String)

    # Sava into file
    if not os.path.exists('Condition'):
        os.makedirs('Condition')
    with open(CONDITION_HEADER_PATH, 'w') as f:
        f.write(Condition_Header_Header_String)


def write_condition_source():
    # Condition
    Condition_String = ''
    Condition_Signal_String = ''
    Signal_Condition_Number = 0
    Signal_Name = None
    for i, row in ConditionDataFrame.iterrows():
        if Signal_Name is None:
            Signal_Name = row.loc['SignalName']
            Condition_String = ''
        if row.loc['SignalName'] != Signal_Name:
            Condition_Signal_String += f"const Condition {Signal_Name}_Condition [{Signal_Condition_Number}] = {{{Condition_String}}};\n"
            Signal_Condition_Number = 0
            Signal_Name = row.loc['SignalName']
            Condition_String = ''
        elif i != 0:
            Condition_String += ','
        Condition_String += f"{{{row.loc['ThresholdType']}, {row.loc['Threshold']}, {row.loc['Symbol']}, &{row.loc['EVT']}, {row.loc['Macro']}}}"
        Signal_Condition_Number += 1
        if i == len(ConditionDataFrame) - 1:
            Condition_Signal_String += f"const Condition {Signal_Name}_Condition [{Signal_Condition_Number}] = {{{Condition_String}}};\n"
    # print(Condition_Signal_String)

    # SignalConditionArray
    Condition_Array_String = 'static const SignalCondition SignalConditionArray[SIGNAL_NUM] = {\n'
    Signal_Name = None
    Signal_Condition_Number = 0
    for i, row in ConditionDataFrame.iterrows():
        if Signal_Name is None:
            Signal_Name = row.loc['SignalName']
        if row.loc['SignalName'] != Signal_Name:
            Signal_Type = SignalDataFrame.loc[SignalDataFrame['SignalName'] == Signal_Name, 'Type'].values[0]
            Condition_Array_String += f"{{{Signal_Name}_SIGNALNUM, Type_{Signal_Type} , {Signal_Condition_Number} , &{Signal_Name}_Condition}},\n"
            Signal_Condition_Number = 0
            Signal_Name = row.loc['SignalName']
        Signal_Condition_Number += 1
        if i == len(ConditionDataFrame) - 1:
            Signal_Type = SignalDataFrame.loc[SignalDataFrame['SignalName'] == Signal_Name, 'Type'].values[0]
            Condition_Array_String += f"{{{Signal_Name}_SIGNALNUM, Type_{Signal_Type}, {Signal_Condition_Number} , &{Signal_Name}_Condition}}}};\n"

    # TIMEOUT_ACTION_ARRAY
    Time_Out_Action_String = 'const Condition TimeOutActionArray[TIMEOUT_NUM] = {\n'
    for i, row in TimeFlagDataFrame.iterrows():
        if pd.notna(row.loc['FlagName']):
            Time_Out_Action_String += f"{{1,EQ,{row.loc['FlagName']},0}}\n"
    Time_Out_Action_String += '};\n'
    # print(Time_Out_Action_String)

    # print(Condition_Array_String)
    with open(CONDITION_SOURCE_PATH, 'w') as f:
        f.write(Condition_Source_Header_String)
        f.write(Condition_Signal_String + '\n')
        f.write(Condition_Array_String + '\n')
        f.write(Time_Out_Action_String + '\n')
    pass


def main():
    write_condition_header()
    write_condition_source()
    pass


if __name__ == '__main__':
    main()
