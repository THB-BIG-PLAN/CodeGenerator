import os
import pandas as pd
import openpyxl
import warnings

# 忽略警告
warnings.simplefilter(action='ignore', category=UserWarning)
# 写H文件
Condition_File = open("../Condition/Condition.h", "w+")
Condition_File.write('''
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
#define CHANGE 8\n\n\n''')
df = pd.read_excel('config.xlsx', sheet_name=0)
Condition_File.write('\n\n\n')
SIGNALNUM = len(df)
for index in range(len(df.index)):
    Condition_File.write('#define ' + df.iloc[index, 1] + ' ' + str(index) + '\n')
Condition_File.write('\n\n\n')

df = pd.read_excel('config.xlsx', sheet_name=5)
for index in range(len(df.index)):
    Condition_File.write('#define ' + df.iloc[index, 0] + ' ' + str(index) + '\n')
Condition_File.write('\n\n\n')

# 根据第四个sheet超时标志位写入.h文件
df = pd.read_excel('config.xlsx', sheet_name=3)
for index in range(len(df.index)):
    Condition_File.write('#define ' + str(df.iloc[index, 0]) + ' ' + str(index) + '\n')
Condition_File.write('\n\n\n')
TIMEOUT_NUM = len(df)
df = pd.read_excel('config.xlsx', sheet_name=5)
CONDITION_NUM = len(df)
Condition_File.write('#define ' + 'SIGNAL_NUM ' + str(SIGNALNUM) + '\n')
Condition_File.write('#define ' + 'TIMEOUT_NUM ' + str(TIMEOUT_NUM) + '\n')
Condition_File.write('#define ' + 'CONDITION_NUM ' + str(CONDITION_NUM) + '\n')
Condition_File.write('\n\n\n')

# 写结构体类型
Condition_File.write('''typedef struct Condition{
	T_u8 Threshold;
	T_u8 Symbol;
	void (*EVT)();
	T_u8 ConditionID;
}Condition;


typedef struct SignalCondition
{
	T_u8 Signal;
	T_u8 Len;
	const Condition* Condition;
}SignalCondition;


typedef struct EVT_FLAG {

	T_u8 SignalNum[SIGNAL_NUM];
	T_u8 SignalPreNum[SIGNAL_NUM];
	T_u8 LGL_TimeOutFlagNum;
	T_bit TimeOutFlag[TIMEOUT_NUM];
	T_bit ConditionFlag[CONDITION_NUM];
}EVT_FLAG;

extern EVT_FLAG* EVT_flag;
static const SignalCondition SignalConditionArray[SIGNAL_NUM];
static const Condition TimeOutActionArray[TIMEOUT_NUM];
#endif /* CONDITION_H_ */
''')
Condition_File.close()

# 写.c文件
# 根据第三个sheet定义数组写入.c文件 其中每个数据结构包括阈值，符号，动作
Condition_File = open('../Condition/Condition.c', 'w+')
Signal = pd.read_excel('config.xlsx', sheet_name=0).iloc[:, 0]
n = 0
Condition_File.write('#include "EVT/Condition/Condition.h"\n\n')
df = pd.read_excel('config.xlsx', sheet_name=2)
for index in range(len(df)):
    if index == 0 or str(df.iloc[index, 0]) != str(Signal[n]):
        if index != 0:
            n += 1
            Condition_File.write('};\n\n')
        SignalLen = len(df[df.iloc[:, 0] == str(Signal[n])])
        Condition_File.write(
            'const Condition {name}[{len}] = {{'.format(name=str(df.iloc[index, 0]) + '_Condition', len=SignalLen))
    else:
        Condition_File.write(',')
    Condition_File.write('{{{threshold},{Symbol},&{action},{ConditionID}}}'.format(threshold=df.iloc[index, 2],
                                                                                   Symbol=df.iloc[index, 1],
                                                                                   action=df.iloc[index, 3],
                                                                                   ConditionID=df.iloc[index, 4]))
Condition_File.write('};\n\n')

# 信号数组，其中每个结构体包括信号条件个数，对应条件数组的指针
Signal = pd.read_excel('config.xlsx', sheet_name=0)
Condition_File.write('static const SignalCondition SignalConditionArray[{len}] = {{'.format(len='SIGNAL_NUM'))
for index in range(len(Signal)):
    Condition_File.write('{{{name},{len},&({pointer})'.format(name=Signal.iloc[index, 1],
                                                              len=len(df[df.iloc[:, 0] == str(Signal.iloc[index, 0])]),
                                                              pointer=Signal.iloc[index, 0] + '_Condition'))
    if index == len(Signal) - 1:
        Condition_File.write('}};')
    else:
        Condition_File.write('},\n')
Condition_File.write('\n\n')

# 超时执行动作数组
Signal = pd.read_excel('config.xlsx', sheet_name=3)
Condition_File.write('static const Condition TimeOutActionArray[{len}] = {{'.format(len='TIMEOUT_NUM'))
for index in range(len(Signal)):
    Condition_File.write('{{{threshold},{Symbol},&({action})'.format(threshold='1',
                                                                     Symbol='EQ',
                                                                     action=Signal.iloc[index, 2]))
    if index == len(Signal) - 1:
        Condition_File.write('}};')
    else:
        Condition_File.write('},\n')
Condition_File.write('\n\n\nEVT_FLAG* EVT_flag;')
Condition_File.close()

EVT_File = open('../EVT/EVT.h', 'w+')

print('按任意键继续')
input()
