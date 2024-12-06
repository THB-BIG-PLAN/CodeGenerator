import os
import pandas as pd
import openpyxl
import warnings

# 忽略警告
warnings.simplefilter(action='ignore', category=UserWarning)
CONFIG_PATH = 'ConfigByHand.xlsx'
ListDataFrame = pd.read_excel(CONFIG_PATH, sheet_name='List')
Condition_Header_String = '''
#ifndef CONDITION_H_
#define CONDITION_H_
#include <Type_define.h>
#include "EVT/Event/EVT.h"
#include "EVT/Logic/Logic.h"
#include <sgn/signal_api.h>
#include <stdbool.h>

#define CONDITION_TYPE_NUMBER false
#define CONDITION_TYPE_SIGNAL true
'''


def write_Symbol_Macro():
    global Condition_Header_String
    Condition_Header_String += '\n\n'
    for i, row in ListDataFrame.iterrows():
        if pd.notna(row.loc['Symbol']):
            Condition_Header_String += '#define ' + str(row.loc['Symbol']) + ' ' + str(i) + '\n'


def write_Struct():
    global Condition_Header_String
    Condition_Header_String += '\n\n'
    Condition_Header_String += '''
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
'''


def write_header_file():
    write_Symbol_Macro()
    write_Struct()
    print(Condition_Header_String)


def main():
    write_header_file()
    warnings.simplefilter(action='ignore', category=UserWarning)
    print("Condition.h and Condition.c have been generated successfully.")
    print("Press Enter to continue...")
    input()


if __name__ == "__main__":
    main()
