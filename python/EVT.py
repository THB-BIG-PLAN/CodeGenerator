import pandas as pd
import re
import warnings

# 忽略警告
warnings.simplefilter(action='ignore', category=UserWarning)

# 常量定义
CONFIG_PATH = 'config.xlsx'
EVT_HEADER_PATH = 'EVT/EVT.h'
EVT_SOURCE_PATH = 'EVT/EVT.c'


def write_event_header(file):
    """写入 EVT.h 文件."""
    df = pd.read_excel(CONFIG_PATH, sheet_name=4).iloc[:, 0]

    file.write('''#ifndef EVT_EVENT_EVT_\n#define EVT_EVENT_EVT_\n\n''')

    for event in df:
        file.write(f'extern void {event}();\n')

    file.write('\n#endif /* EVT_EVENT_EVT_ */\n')


def write_event_definitions(file):
    """写入事件定义到 EVT.c 文件."""
    df_events = pd.read_excel(CONFIG_PATH, sheet_name=6)

    for index, row in df_events.iterrows():
        file.write(f'#define {row.iloc[0]} {row.iloc[1]}\n')
    file.write('\n\n')


def write_action_definitions(file):
    """写入动作定义到 EVT.c 文件."""
    df_actions = pd.read_excel(CONFIG_PATH, sheet_name=7)

    for i, row in df_actions.iterrows():
        file.write(f'#define {row.iloc[1]} {{ ')
        file.write('; '.join(str(cell) for cell in row[2:] if pd.notna(cell)))
        file.write(' ;}\n')
    file.write('\n\n')


def write_event_function_declarations(file):
    """写入事件函数声明到 EVT.c 文件."""
    df_event_funcs = pd.read_excel(CONFIG_PATH, sheet_name=4)

    for event in df_event_funcs.iloc[:, 0]:
        file.write(f'void {event}();\n')

    file.write('\n\nvoid LGL_initialize() {\n    Condition_Init();\n}\n\n')


def write_event_functions(file):
    """写入事件函数定义到 EVT.c 文件."""
    df_event_funcs = pd.read_excel(CONFIG_PATH, sheet_name=4)

    for i, event in enumerate(df_event_funcs.iloc[:, 0]):
        file.write(f'void {event}() \n{{\n')

        if pd.isna(df_event_funcs.iloc[i, 3]) or re.match('2', event):
            for j in range(1, 3):
                if pd.notna(df_event_funcs.iloc[i, j]):
                    file.write(f'    {df_event_funcs.iloc[i, j]};\n')
        else:
            conditions = [
                f'EVT_Flag->ConditionFlag[{df_event_funcs.iloc[i, j]}]'
                for j in range(3, df_event_funcs.shape[1])
                if pd.notna(df_event_funcs.iloc[i, j]) and df_event_funcs.iloc[i, j] != 'AND'
            ]
            file.write('    if (' + ' && \n        '.join(conditions) + ') \n    {\n')
            for j in range(1, 3):
                if pd.notna(df_event_funcs.iloc[i, j]):
                    file.write(f'        {df_event_funcs.iloc[i, j]};\n')
            file.write('    }\n')

        file.write('}\n\n')


def write_event_source():
    """写入 EVT.c 文件."""
    with open(EVT_SOURCE_PATH, 'w') as evt_file:
        evt_file.write('''#include <Type_define.h>
#include <stdlib.h>
#include <string.h>
#include <sgn/signal_api.h>
#include "EVT/Timer/Timer.api.h"
#include "EVT/Event/EVT.h"
#include "EVT/Logic/Logic.h"
#include "EVT/Condition/Condition.h"\n\n''')

        write_event_definitions(evt_file)
        write_action_definitions(evt_file)
        write_event_function_declarations(evt_file)
        write_event_functions(evt_file)


def main():
    with open(EVT_HEADER_PATH, 'w') as evt_file:
        write_event_header(evt_file)

    write_event_source()
    print("生成完成，按任意键继续")
    input()
