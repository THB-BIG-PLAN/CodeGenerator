import os
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

'''
Condition_Source_Header_String = '''
#include "EVT/Condition/Condition.h"\n\n
'''


def write_condition_header():
    global Condition_Header_Header_String
    ConditionNum = 0
    Signal_Number_Macro_String = ''
    for i, row in SignalDataFrame.iterrows():
        Signal_Number_Macro_String += f"#define {row.loc['SignalName']} {i}\n"
    # print(Signal_Number_Macro_String)
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

    for i, row in TimeFlagDataFrame.iterrows():
        if pd.notna(row.loc['FlagName']):
            Time_Macro_String += f"#define {row.loc['FlagName']} {i}\n"
    SignalNum = len(SignalDataFrame)
    TimeFlagNum = len(TimeFlagDataFrame)
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
bool Type;
T_u8 Threshold;
T_u8 Symbol;
void (*EVT)();
T_u8 ConditionID;
} Condition;

typedef struct SignalCondition {
    T_u8 Signal;
    T_u8 Len;
    const Condition* Condition;
} SignalCondition;

typedef struct EVT_FLAG {
    T_u8 SignalNum[SIGNAL_NUM];
    T_u8 SignalPreNum[SIGNAL_NUM];
    T_u8 LGL_TimeOutFlagNum;
    T_bit TimeOutFlag[TIMEOUT_NUM];
    T_bit ConditionFlag[CONDITION_NUM];
} EVT_FLAG;

extern EVT_FLAG* EVT_flag;
static const SignalCondition SignalConditionArray[SIGNAL_NUM];
static const Condition TimeOutActionArray[TIMEOUT_NUM];
#endif /*CONDITION_H_*/
'''
    # print(Condition_Header_Header_String)
    if not os.path.exists('Condition'):
        os.makedirs('Condition')
    with open(CONDITION_HEADER_PATH, 'w') as f:
        f.write(Condition_Header_Header_String)


def write_condition_source():
    Condition_String = ''
    Condition_Signal_String = ''
    Signal_Condition_Number = 0
    Signal_Name = None
    for i, row in ConditionDataFrame.iterrows():
        if Signal_Name is None:
            Signal_Name = row.loc['SignalName']
            Condition_String = ''
        if row.loc['SignalName'] != Signal_Name:
            Condition_Signal_String += f"const Condition {Signal_Name}_Condition [{Signal_Condition_Number}] = {{{Condition_String}}}\n"
            Signal_Condition_Number = 0
            Signal_Name = row.loc['SignalName']
            Condition_String = ''
        elif i != 0:
            Condition_String += ','
        Condition_String += f"{{{row.loc['ThresholdType']}, {row.loc['Threshold']}, {row.loc['Symbol']}, &{row.loc['EVT']}, {row.loc['Macro']}}}"
        Signal_Condition_Number += 1
        if i == len(ConditionDataFrame) - 1:
            Condition_Signal_String += f"const Condition {Signal_Name}_Condition [{Signal_Condition_Number}] = {{{Condition_String}}}\n"
    # print(Condition_Signal_String)
    Condition_Array_String = 'static const SignalCondition SignalConditionArray[SIGNAL_NUM] ={\n'
    Signal_Name = None
    Signal_Condition_Number = 0
    for i, row in ConditionDataFrame.iterrows():
        if Signal_Name is None:
            Signal_Name = row.loc['SignalName']
        if row.loc['SignalName'] != Signal_Name:
            Condition_Array_String += f"{{{Signal_Name}_SIGNALNUM, {Signal_Condition_Number}, &{Signal_Name}_Condition}},\n"
            Signal_Condition_Number = 0
            Signal_Name = row.loc['SignalName']
        Signal_Condition_Number += 1
        if i == len(ConditionDataFrame) - 1:
            Condition_Array_String += f"{{{Signal_Name}_SIGNALNUM, {Signal_Condition_Number}, &{Signal_Name}_Condition}}}};\n"
    # print(Condition_Array_String)
    with open(CONDITION_SOURCE_PATH, 'w') as f:
        f.write(Condition_Source_Header_String)
        f.write(Condition_Signal_String)
        f.write(Condition_Array_String)
    pass


def main():
    write_condition_header()
    write_condition_source()
    pass


if __name__ == '__main__':
    main()
