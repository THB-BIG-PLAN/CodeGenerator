import os
import pandas as pd
import openpyxl
import warnings

# 忽略警告
warnings.simplefilter(action='ignore', category=UserWarning)

# 常量定义
CONFIG_PATH = 'config.xlsx'
HEADER_FILE_PATH = "Condition/Condition.h"
SOURCE_FILE_PATH = 'Condition/Condition.c'
EVT_FILE_PATH = 'EVT/EVT.h'

HEADER_TEMPLATE = '''
#ifndef CONDITION_H_
#define CONDITION_H_
#include <Type_define.h>
#include "EVT/Event/EVT.h"
#include "EVT/Logic/Logic.h"
#include <sgn/signal_api.h>
#define EQ 1
#define NEQ 2
#define GREATER 3
#define GREATEROREQ 4
#define LESS 5
#define LESSOREQ 6
#define CHANGETO 7
#define CHANGE 8

typedef struct Condition {{
    T_u8 Threshold;
    T_u8 Symbol;
    void (*EVT)();
    T_u8 ConditionID;
}} Condition;

typedef struct SignalCondition {{
    T_u8 Signal;
    T_u8 Len;
    const Condition* Condition;
}} SignalCondition;

typedef struct EVT_FLAG {{
    T_u8 SignalNum[SIGNAL_NUM];
    T_u8 SignalPreNum[SIGNAL_NUM];
    T_u8 LGL_TimeOutFlagNum;
    T_bit TimeOutFlag[TIMEOUT_NUM];
    T_bit ConditionFlag[CONDITION_NUM];
}} EVT_FLAG;

extern EVT_FLAG* EVT_flag;
static const SignalCondition SignalConditionArray[SIGNAL_NUM];
static const Condition TimeOutActionArray[TIMEOUT_NUM];
#endif /* CONDITION_H_ */
'''


def write_header_file():
    # 读取不同 sheet 的数据
    df_signal = pd.read_excel(CONFIG_PATH, sheet_name=0)
    df_condition = pd.read_excel(CONFIG_PATH, sheet_name=5)
    df_timeout = pd.read_excel(CONFIG_PATH, sheet_name=3)

    # 统计数量
    signal_num = len(df_signal)
    condition_num = len(df_condition)
    timeout_num = len(df_timeout)

    # 写入 .h 文件
    with open(HEADER_FILE_PATH, "w") as file:
        file.write(HEADER_TEMPLATE)
        for index, row in df_signal.iterrows():
            file.write(f'#define {row.iloc[1]} {index}\n')
        file.write("\n")
        for index, row in df_condition.iterrows():
            file.write(f'#define {row.iloc[0]} {index}\n')
        file.write("\n")
        for index, row in df_timeout.iterrows():
            file.write(f'#define {row.iloc[0]} {index}\n')

        file.write(f'\n#define SIGNAL_NUM {signal_num}\n')
        file.write(f'#define TIMEOUT_NUM {timeout_num}\n')
        file.write(f'#define CONDITION_NUM {condition_num}\n')


def write_source_file():
    # 读取相关数据
    df_signal = pd.read_excel(CONFIG_PATH, sheet_name=0)
    df_condition_def = pd.read_excel(CONFIG_PATH, sheet_name=2)
    df_timeout_action = pd.read_excel(CONFIG_PATH, sheet_name=3)

    # 写入 .c 文件
    with open(SOURCE_FILE_PATH, "w") as file:
        file.write('#include "EVT/Condition/Condition.h"\n\n')

        # 写入 Condition 定义
        signal_name = None
        for index, row in df_condition_def.iterrows():
            if row.iloc[0] != signal_name:
                if signal_name is not None:
                    file.write('};\n\n')
                signal_name = row.iloc[0]
                condition_count = len(df_condition_def[df_condition_def.iloc[:, 0] == signal_name])
                file.write(f'const Condition {signal_name}_Condition[{condition_count}] = {{')
            else:
                file.write(',')
            file.write(f'{{{row.iloc[2]},{row.iloc[1]},&{row.iloc[3]},{row.iloc[4]}}}')
        file.write('};\n\n')

        # 写入 SignalCondition 数组
        file.write('static const SignalCondition SignalConditionArray[SIGNAL_NUM] = {\n')
        for index, row in df_signal.iterrows():
            signal_conditions = len(df_condition_def[df_condition_def.iloc[:, 0] == row.iloc[0]])
            pointer = f'{row.iloc[0]}_Condition'
            file.write(f'{{{row.iloc[1]},{signal_conditions},&{pointer}}}')
            if index != len(df_signal) - 1:
                file.write(',\n')
        file.write('};\n\n')

        # 写入 TimeOutAction 数组
        file.write(f'static const Condition TimeOutActionArray[TIMEOUT_NUM] = {{\n')
        for index, row in df_timeout_action.iterrows():
            file.write(f'{{1, EQ, &{row.iloc[2]}}}')
            if index != len(df_timeout_action) - 1:
                file.write(',\n')
        file.write('};\n\n\nEVT_FLAG* EVT_flag;\n')


def main():
    write_header_file()
    write_source_file()
    print("按任意键继续")
    input()


if __name__ == "__main__":
    main()
