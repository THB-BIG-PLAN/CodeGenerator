import os
import re

import pandas as pd
import openpyxl
import warnings

# 忽略警告
warnings.simplefilter(action='ignore', category=UserWarning)

# EVT.h
df = pd.read_excel('config.xlsx', sheet_name=4).iloc[:, 0]
EVT_File = open('../EVT/EVT.h', 'w+')
EVT_File.write('''
#ifndef EVT_EVENT_EVT_
#define EVT_EVENT_EVT_\n\n\n
''')
for index in range(len(df)):
    EVT_File.write('extern void ' + str(df[index]) + '();\n')
EVT_File.write('\n#endif /* EVT_EVENT_EVT_ */')
EVT_File.close()

# EVT.c
df = pd.read_excel('config.xlsx', sheet_name=6)
EVT_File = open('../EVT/EVT.c', 'w+')
EVT_File.write('''
#include <Type_define.h>
#include <stdlib.h>
#include <string.h>
#include <sgn/signal_api.h>
#include "EVT/Timer/Timer.api.h"
#include "EVT/Event/EVT.h"
#include "EVT/Logic/Logic.h"
#include "EVT/Condition/Condition.h"\n\n\n\n
''')
for index in range(len(df)):
    EVT_File.write('#define ' + df.iloc[index, 0] + ' ' + str(df.iloc[index, 1]) + '\n')
EVT_File.write('\n\n\n')

# action
df = pd.read_excel('config.xlsx', sheet_name=7)
for i in range(len(df)):
    EVT_File.write('#define ' + df.iloc[i, 0] + ' {')
    for j in range(df.iloc[i].shape[0]):
        if not pd.isna(df.iloc[i, j]):
            EVT_File.write(df.iloc[i, j] + '; ')
    EVT_File.write('}\n')
EVT_File.write('\n\n\n')


df = pd.read_excel('config.xlsx', sheet_name=4)
for index in range(len(df)):
    EVT_File.write('void ' + df.iloc[index, 0] + '();\n')
EVT_File.write('\n\n\n')
EVT_File.write('''
void LGL_initialize()
{
	Conditon_Init();
}
''')
EVT_File.write('\n')

for i in range(len(df)):
    EVT_File.write('void ' + df.iloc[i, 0] + '()\n{\n')
    if pd.isna(df.iloc[i, 4]) or (re.match('2', df.iloc[i, 0]) is not None):
        for j in range(1, 3):
            if not pd.isna(df.iloc[i, j]):
                EVT_File.write('    ' + df.iloc[i, j] + ';\n')
    else:
        EVT_File.write('    if(')
        for j in range(3, df.shape[0] + 1):
            if not pd.isna(df.iloc[i, j]):
                if df.iloc[i, j] != 'AND':
                    EVT_File.write('EVT_Flag->ConditionFlag[{action}]'.format(action=df.iloc[i, j]))
                else:
                    EVT_File.write(' && \n       ')
        EVT_File.write(' )\n    {\n ')
        for j in range(1, 3):
            if not pd.isna(df.iloc[i, j]):
                EVT_File.write('        ' + df.iloc[i, j] + ';\n')

        EVT_File.write('\n    }\n')
    EVT_File.write('}\n\n\n')


EVT_File.close()
