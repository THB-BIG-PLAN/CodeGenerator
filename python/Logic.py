# -*- coding: gbk -*-

import pandas as pd
import re
import warnings
import Exception

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

void SignalInit();
void judge();
void TimeOutjudge();


void Condition_Init()
{
	Init_Timer();
	EVT_flag = (EVT_FLAG*)malloc(sizeof(EVT_FLAG));
	memset(EVT_flag,0,sizeof(EVT_FLAG));
	SignalInit();
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
        if pd.isna(row.iloc[2]) or row.iloc[2] == '':
            raise Exception.EmptyTypeError(index,'SignalSheet')
        SignalSyncString += f"    EVT_flag->SignalNum[{row.iloc[1]}] = Get_{row.iloc[2]}_{row.iloc[1]}();\n"
    file.write(SignalSyncString)
    file.write('''	
    for (int i = 0 ; i< SIGNAL_NUM ; i++)
	{
	    EVT_flag->SignalPreNum[i] = EVT_flag->SignalNum[i];
	}
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
	{   if(condition->Type == CONDITION_TYPE_NUMBER)
		{
            if(EVT_flag->SignalNum[Signal] == condition->Threshold)
            {
                EVT_flag->ConditionFlag[condition->ConditionID] = true;
                condition->EVT();
            }
        }
        else
        {
            if(EVT_flag->SignalNum[Signal] == EVT_flag->SignalNum[condition->Threshold])
            {
                EVT_flag->ConditionFlag[condition->ConditionID] = true;
                condition->EVT();
            }
        }

	}
	else if(condition->Symbol == NEQ)
	{
		if(condition->Type == CONDITION_TYPE_NUMBER)
		{
            if(EVT_flag->SignalNum[Signal] != condition->Threshold)
            {
                EVT_flag->ConditionFlag[condition->ConditionID] = true;
                condition->EVT();
            }
        }
        else
        {
            if(EVT_flag->SignalNum[Signal] != EVT_flag->SignalNum[condition->Threshold])
            {
                EVT_flag->ConditionFlag[condition->ConditionID] = true;
                condition->EVT();
            }
        }
	}
	else if(condition->Symbol == GREATER)
	{
		if(condition->Type == CONDITION_TYPE_NUMBER)
		{
            if(EVT_flag->SignalNum[Signal] > condition->Threshold)
            {
                EVT_flag->ConditionFlag[condition->ConditionID] = true;
                condition->EVT();
            }
        }
        else
        {
            if(EVT_flag->SignalNum[Signal] > EVT_flag->SignalNum[condition->Threshold])
            {
                EVT_flag->ConditionFlag[condition->ConditionID] = true;
                condition->EVT();
            }
        }
	}
	else if(condition->Symbol == GREATEROREQ)
	{
		if(condition->Type == CONDITION_TYPE_NUMBER)
		{
            if(EVT_flag->SignalNum[Signal] >= condition->Threshold)
            {
                EVT_flag->ConditionFlag[condition->ConditionID] = true;
                condition->EVT();
            }
        }
        else
        {
            if(EVT_flag->SignalNum[Signal] >= EVT_flag->SignalNum[condition->Threshold])
            {
                EVT_flag->ConditionFlag[condition->ConditionID] = true;
                condition->EVT();
            }
        }
	}
	else if(condition->Symbol == LESS)
	{
		if(condition->Type == CONDITION_TYPE_NUMBER)
		{
            if(EVT_flag->SignalNum[Signal] < condition->Threshold)
            {
                EVT_flag->ConditionFlag[condition->ConditionID] = true;
                condition->EVT();
            }
        }
        else
        {
            if(EVT_flag->SignalNum[Signal] < EVT_flag->SignalNum[condition->Threshold])
            {
                EVT_flag->ConditionFlag[condition->ConditionID] = true;
                condition->EVT();
            }
        }
	}
	else if(condition->Symbol == LESSOREQ)
	{
		if(condition->Type == CONDITION_TYPE_NUMBER)
		{
            if(EVT_flag->SignalNum[Signal] <= condition->Threshold)
            {
                EVT_flag->ConditionFlag[condition->ConditionID] = true;
                condition->EVT();
            }
        }
        else
        {
            if(EVT_flag->SignalNum[Signal] <= EVT_flag->SignalNum[condition->Threshold])
            {
                EVT_flag->ConditionFlag[condition->ConditionID] = true;
                condition->EVT();
            }
        }
	}
	else if(condition->Symbol == CHANGETO)
	{
	    if(condition->Type == CONDITION_TYPE_NUMBER)
		{
            if(condition->Threshold == EVT_flag->SignalNum[Signal] && EVT_flag->SignalNum[Signal] != EVT_flag->SignalPreNum[Signal])
            {
                EVT_flag->ConditionFlag[condition->ConditionID] = true;
                condition->EVT();
            }
        }
        else
        {
            if(EVT_flag->SignalNum[Signal] == EVT_flag->SignalNum[condition->Threshold] && EVT_flag->SignalNum[Signal] != EVT_flag->SignalPreNum[Signal])
            {
                EVT_flag->ConditionFlag[condition->ConditionID] = true;
                condition->EVT();
            }
        }
	}
	else if(condition->Symbol == CHANGE)
	{
		if(EVT_flag->SignalNum[Signal] != EVT_flag->SignalPreNum[Signal])
		{
			EVT_flag->ConditionFlag[condition->ConditionID] = true;
            condition->EVT();
		}
	}
}
''')
    InitDataFrame = pd.read_excel('config.xlsx', sheet_name='Init')
    InitString = ''
    for index, row in InitDataFrame.iterrows():
        if pd.isna(row.loc['Type']) or row.loc['Type'] == '':
            raise Exception.EmptyTypeError(index,'InitSheet')
        if pd.isna(row.loc['Value']) or row.loc['Value'] == '':
            raise Exception.EmptyValueError(index)
        InitString += f"    Set_{row.loc['Type']}_{row.loc['SignalName']}({row.loc['Value']})\n"
    file.write(f'''
void SignalInit()
{{
{InitString}
}}
#pragma GCC pop_options
    ''')


def main():
    with open(HEADER_FILE_PATH, 'w') as f:
        WriteHeaderFile(f)
    with open(SOURCE_FILE_PATH, 'w') as f:
        WriteSourceFile(f)
    print('Logic.h and Logic.c have been generated successfully.')
    print("Press Enter to continue...")
    input()


if __name__ == '__main__':
    main()
