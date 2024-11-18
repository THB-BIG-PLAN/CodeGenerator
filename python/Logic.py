# -*- coding: gbk -*-

import pandas as pd
import re
import warnings

# 忽略警告
warnings.simplefilter(action='ignore', category=UserWarning)

HEADER_FILE_PATH = 'Logic/Logic.h'
SOURCE_FILE_PATH = 'Logic/Logic.c'
CONFIG_FILE_PATH = 'config.xlsx'
HEADER_FILE_HEADER = '''
#ifndef EVT_EVENT_LOGIC_H_
#define EVT_EVENT_LOGIC_H_



extern void Condition_Init();
extern void Condition_Step();

#endif /* EVT_EVENT_LOGIC_H_ */
'''

Source_File_Header = '''
#pragma GCC push_options
#pragma GCC optimize ("O0")

#include <Type_define.h>
#include "EVT/Logic/Logic.h"
#include "EVT/EVT/EVT.h"
#include <sgn/signal_api.h>
#include "EVT/Condition/Condition.h"
#include <stdbool.h>



void Condition_Init()
{
	Init_Timer();
	EVT_flag = (EVT_FLAG*)malloc(sizeof(EVT_FLAG));
	memset(EVT_flag,0,sizeof(EVT_FLAG));
}

void Condition_Step()
{
'''


def WriteHeaderFile(file):
    file.write(HEADER_FILE_HEADER)


def WriteSourceFile(file):
    file.write(Source_File_Header)
    SignalDataFrame = pd.read_excel(CONFIG_FILE_PATH, sheet_name=0)
    SignalSyncString = ''
    for index, row in SignalDataFrame.iterrows():
        SignalSyncString += f"    EVT_flag->SignalNum[{row.iloc[1]}] = Get_{row.iloc[2]}_{row.iloc[1]}();\n"
    file.write(SignalSyncString)
    file.write('''	
    for(int i = 0; i < SIGNAL_NUM ; i++)
	{
		int length = SignalConditionArray[i].Len;
		for(int j = 0;j<length;j++)
		{
			judge(i,&SignalConditionArray[i].Condition[j]);
		}
	}
	for(int i = 0; i < TIMEOUT_NUM ; i++)
	{
		TimeOutjudge(i,&TimeOutActionArray[i]);
	}
	memset(EVT_flag->ConditionFlag,0,sizeof(EVT_flag->ConditionFlag));
}

void TimeOutjudge(T_u8 Signal,Condition* condition)
{
	if(condition->Symbol == EQ)
	{
		if(condition->Threshold == EVT_flag->TimeOutFlag[Signal])
			condition->EVT();
	}

}

void judge(T_u8 Signal,Condition* condition)
{

	if(condition->Symbol == EQ)
	{
		if(condition->Threshold == EVT_flag->SignalNum[Signal])
		{
			condition->EVT();
			EVT_flag->ConditionFlag[condition->ConditionID] = true;
		}
	}
	else if(condition->Symbol == NEQ)
	{
		if(condition->Threshold != EVT_flag->SignalNum[Signal])
		{
			condition->EVT();
			EVT_flag->ConditionFlag[condition->ConditionID] = true;
		}
	}
	else if(condition->Symbol == GREATER)
	{
		if(condition->Threshold > EVT_flag->SignalNum[Signal])
		{
			condition->EVT();
			EVT_flag->ConditionFlag[condition->ConditionID] = true;
		}
	}
	else if(condition->Symbol == GREATEROREQ)
	{
		if(condition->Threshold >= EVT_flag->SignalNum[Signal])
		{
			condition->EVT();
			EVT_flag->ConditionFlag[condition->ConditionID] = true;
		}
	}
	else if(condition->Symbol == LESS)
	{
		if(condition->Threshold < EVT_flag->SignalNum[Signal])
		{
			condition->EVT();
			EVT_flag->ConditionFlag[condition->ConditionID] = true;
		}
	}
	else if(condition->Symbol == LESSOREQ)
	{
		if(condition->Threshold <= EVT_flag->SignalNum[Signal])
		{
			condition->EVT();
			EVT_flag->ConditionFlag[condition->ConditionID] = true;
		}
	}
	else if(condition->Symbol == CHANGETO)
	{
		if(condition->Threshold == EVT_flag->SignalNum[Signal] && EVT_flag->SignalNum[Signal] != EVT_flag->SignalPreNum[Signal])
		{
			condition->EVT();
			EVT_flag->ConditionFlag[condition->ConditionID] = true;
		}
	}
	else if(condition->Symbol == CHANGE)
	{
		if(EVT_flag->SignalNum[Signal] != EVT_flag->SignalPreNum[Signal])
		{
			condition->EVT();
			EVT_flag->ConditionFlag[condition->ConditionID] = true;
		}
	}
}
#pragma GCC pop_options
''')


def main():
    with open(HEADER_FILE_PATH, 'w') as f:
        WriteHeaderFile(f)
    with open(SOURCE_FILE_PATH, 'w') as f:
        WriteSourceFile(f)
    print('Logic.h and Logic.c have been generated successfully.')
    print("Press any key to continue...")
    input()


if __name__ == '__main__':
    main()
