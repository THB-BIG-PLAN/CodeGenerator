#pragma GCC push_options
#pragma GCC optimize ("O0")
/*
 * EVT.c
 *
 *  Created on: 2024锟斤拷7锟斤拷5锟斤拷
 *      Author: ADM
 */
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
	EVT_flag->SignalNum[BdcSeedsignal_SIGNALNUM] = Get_uint8_BdcSeedsignal();
	EVT_flag->SignalNum[BdcWlcmsignal_SIGNALNUM] = Get_uint8_BdcWlcmsignal();
	EVT_flag->SignalNum[DLC_u8TurnLightTwice_SIGNALNUM] = Get_uint8_DLC_u8TurnLightTwice();
	EVT_flag->SignalNum[EEP_LOGO_ENABLE_FLAG_SIGNALNUM] = Get_EEPROM_U8_EEP_LOGO_ENABLE_FLAG();
	EVT_flag->SignalNum[EspAutoHoldActvSts_SIGNALNUM] = Get_uint8_EspAutoHoldActvSts();
	EVT_flag->SignalNum[PLB_u8LBSts_SIGNALNUM] = Get_uint8_PLB_u8LBSts();
	EVT_flag->SignalNum[PPL_boolPosnLampSts_SIGNALNUM] = Get_Bit_PPL_boolPosnLampSts();
	EVT_flag->SignalNum[PRM_u8PowerSts_SIGNALNUM] = Get_uint8_PRM_u8PowerSts();
	EVT_flag->SignalNum[VcuGearPosn_SIGNALNUM] = Get_uint8_VcuGearPosn();
	for(int i = 0; i < SIGNAL_NUM ; i++)
	{
		int length = SignalConditionArray[i].Len;
		for(int j=0;j<length;i++)
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
