
#pragma GCC push_options
#pragma GCC optimize ("O0")

#include <Type_define.h>
#include "EVT/Logic/Logic.h"
#include "EVT/EVT/EVT.h"
#include <sgn/signal_api.h>
#include "EVT/Condition/Condition.h"
#include <stdbool.h>

#define FLOAT_EPS 1e-6
#define DOUBLE_EPS 1e-12

void SignalInit();
void SignalUpdate();
void TimeOut_Condition_Judge(uint8 SignalIndex);

void Bit_Number_Condition_Judgement(uint8 SignalIndex, int len, BitCondition* conditions);
void double_Number_Condition_Judgement(uint8 SignalIndex, int len, doubleCondition* conditions);
void EEPROM_U8_Number_Condition_Judgement(uint8 SignalIndex, int len, EEPROM_U8Condition* conditions);
void int16_Number_Condition_Judgement(uint8 SignalIndex, int len, int16Condition* conditions);
void int32_Number_Condition_Judgement(uint8 SignalIndex, int len, int32Condition* conditions);
void int64_Number_Condition_Judgement(uint8 SignalIndex, int len, int64Condition* conditions);
void int8_Number_Condition_Judgement(uint8 SignalIndex, int len, int8Condition* conditions);
void single_Number_Condition_Judgement(uint8 SignalIndex, int len, singleCondition* conditions);
void uint16_Number_Condition_Judgement(uint8 SignalIndex, int len, uint16Condition* conditions);
void uint32_Number_Condition_Judgement(uint8 SignalIndex, int len, uint32Condition* conditions);
void uint64_Number_Condition_Judgement(uint8 SignalIndex, int len, uint64Condition* conditions);
void uint8_Number_Condition_Judgement(uint8 SignalIndex, int len, uint8Condition* conditions);

void Bit_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions);
void double_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions);
void EEPROM_U8_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions);
void int16_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions);
void int32_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions);
void int64_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions);
void int8_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions);
void single_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions);
void uint16_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions);
void uint32_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions);
void uint64_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions);
void uint8_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions);


void Number_Condition_Judgement(ConditionType Type, void* P_SignalValue, void* P_Threshold, uint8 Symbol, void (*EVT)(), uint8 ConditionIndex);
void Condition_Init()
{
	Init_Timer();
	P_SignalsAndConditions = (SignalsAndConditions*)malloc(sizeof(SignalsAndConditions));
	memset(P_SignalsAndConditions, 0, sizeof(SignalsAndConditions));
	SignalInit();
}

void SignalInit()
{
	Set_EEPROM_U8_output1(5);
	Set_uint8_output2(3);
	Set_uint16_output3(16);
	Set_single_output4(5.4);
	Set_Bit_output5(false);
	Set_double_output6(10233333);
	Set_t_output7(45);

}

void SignalUpdate()
{
	P_SignalsAndConditions->Signal_Bit[PPL_boolPosnLampSts_SIGNALNUM] = Get_Bit_PPL_boolPosnLampSts();
	P_SignalsAndConditions->Signal_EEPROM_U8[EEP_LOGO_ENABLE_FLAG_SIGNALNUM] = Get_EEPROM_U8_EEP_LOGO_ENABLE_FLAG();
	P_SignalsAndConditions->Signal_uint8[BdcSeedsignal_SIGNALNUM] = Get_uint8_BdcSeedsignal();
	P_SignalsAndConditions->Signal_uint8[BdcWlcmsignal_SIGNALNUM] = Get_uint8_BdcWlcmsignal();
	P_SignalsAndConditions->Signal_uint8[DLC_u8TurnLightTwice_SIGNALNUM] = Get_uint8_DLC_u8TurnLightTwice();
	P_SignalsAndConditions->Signal_uint8[EspAutoHoldActvSts_SIGNALNUM] = Get_uint8_EspAutoHoldActvSts();
	P_SignalsAndConditions->Signal_uint8[PLB_u8LBSts_SIGNALNUM] = Get_uint8_PLB_u8LBSts();
	P_SignalsAndConditions->Signal_uint8[PRM_u8PowerSts_SIGNALNUM] = Get_uint8_PRM_u8PowerSts();
	P_SignalsAndConditions->Signal_uint8[VcuGearPosn_SIGNALNUM] = Get_uint8_VcuGearPosn();
}

    
void Condition_Step()
{
	SignalUpdate();
	for (int i = 0 ;i<BIT_SIGNAL_NUMBER;i++)
	{
		Bit_Number_Condition_Judgement(BitConditionInfoArray[i].SignalIndex, BitConditionInfoArray[i].length, BitConditionInfoArray[i].Conditions);
		Bit_Signal_Condition_Judgement(BitSignalConditionInfoArray[i].SignalIndex, BitSignalConditionInfoArray[i].length, BitSignalConditionInfoArray[i].Conditions);
	}

	for (int i = 0 ;i<DOUBLE_SIGNAL_NUMBER;i++)
	{
		double_Number_Condition_Judgement(doubleConditionInfoArray[i].SignalIndex, doubleConditionInfoArray[i].length, doubleConditionInfoArray[i].Conditions);
		double_Signal_Condition_Judgement(doubleSignalConditionInfoArray[i].SignalIndex, doubleSignalConditionInfoArray[i].length, doubleSignalConditionInfoArray[i].Conditions);
	}

	for (int i = 0; i < EEPROM_U8_SIGNAL_NUMBER; i++)
	{
		EEPROM_U8_Number_Condition_Judgement(EEPROM_U8ConditionInfoArray[i].SignalIndex, EEPROM_U8ConditionInfoArray[i].length, EEPROM_U8ConditionInfoArray[i].Conditions);
		EEPROM_U8_Signal_Condition_Judgement(EEPROM_U8SignalConditionInfoArray[i].SignalIndex, EEPROM_U8SignalConditionInfoArray[i].length, EEPROM_U8SignalConditionInfoArray[i].Conditions);

	}

	for (int i = 0; i < INT16_SIGNAL_NUMBER; i++)
	{
		int16_Number_Condition_Judgement(int16ConditionInfoArray[i].SignalIndex, int16ConditionInfoArray[i].length, int16ConditionInfoArray[i].Conditions);
		int16_Signal_Condition_Judgement(int16SignalConditionInfoArray[i].SignalIndex, int16SignalConditionInfoArray[i].length, int16SignalConditionInfoArray[i].Conditions);

	}

	for (int i = 0; i < INT32_SIGNAL_NUMBER; i++)
	{
		int32_Number_Condition_Judgement(int32ConditionInfoArray[i].SignalIndex, int32ConditionInfoArray[i].length, int32ConditionInfoArray[i].Conditions);
		int32_Signal_Condition_Judgement(int32SignalConditionInfoArray[i].SignalIndex, int32SignalConditionInfoArray[i].length, int32SignalConditionInfoArray[i].Conditions);

	}

	for (int i = 0; i < INT64_SIGNAL_NUMBER; i++)
	{
		int64_Number_Condition_Judgement(int64ConditionInfoArray[i].SignalIndex, int64ConditionInfoArray[i].length, int64ConditionInfoArray[i].Conditions);
		int64_Signal_Condition_Judgement(int64SignalConditionInfoArray[i].SignalIndex, int64SignalConditionInfoArray[i].length, int64SignalConditionInfoArray[i].Conditions);
	}

	for (int i = 0; i < INT8_SIGNAL_NUMBER; i++)
	{
		int8_Number_Condition_Judgement(int8ConditionInfoArray[i].SignalIndex, int8ConditionInfoArray[i].length, int8ConditionInfoArray[i].Conditions);
		int8_Signal_Condition_Judgement(int8SignalConditionInfoArray[i].SignalIndex, int8SignalConditionInfoArray[i].length, int8SignalConditionInfoArray[i].Conditions);
	}

	for (int i = 0; i < SINGLE_SIGNAL_NUMBER; i++)
	{
		single_Number_Condition_Judgement(singleConditionInfoArray[i].SignalIndex, singleConditionInfoArray[i].length, singleConditionInfoArray[i].Conditions);
		single_Signal_Condition_Judgement(singleSignalConditionInfoArray[i].SignalIndex, singleSignalConditionInfoArray[i].length, singleSignalConditionInfoArray[i].Conditions);
	}

	for (int i = 0; i < UINT16_SIGNAL_NUMBER; i++)
	{
		uint16_Number_Condition_Judgement(uint16ConditionInfoArray[i].SignalIndex, uint16ConditionInfoArray[i].length, uint16ConditionInfoArray[i].Conditions);
		uint16_Signal_Condition_Judgement(uint16SignalConditionInfoArray[i].SignalIndex, uint16SignalConditionInfoArray[i].length, uint16SignalConditionInfoArray[i].Conditions);
	}

	for (int i = 0; i < UINT32_SIGNAL_NUMBER; i++)
	{
		uint32_Number_Condition_Judgement(uint32ConditionInfoArray[i].SignalIndex, uint32ConditionInfoArray[i].length, uint32ConditionInfoArray[i].Conditions);
		uint32_Signal_Condition_Judgement(uint32SignalConditionInfoArray[i].SignalIndex, uint32SignalConditionInfoArray[i].length, uint32SignalConditionInfoArray[i].Conditions);
	}

	for (int i = 0; i < UINT64_SIGNAL_NUMBER; i++)
	{
		uint64_Number_Condition_Judgement(uint64ConditionInfoArray[i].SignalIndex, uint64ConditionInfoArray[i].length, uint64ConditionInfoArray[i].Conditions);
		uint64_Signal_Condition_Judgement(uint64SignalConditionInfoArray[i].SignalIndex, uint64SignalConditionInfoArray[i].length, uint64SignalConditionInfoArray[i].Conditions);
	}

	for (int i = 0; i < UINT8_SIGNAL_NUMBER; i++)
	{
		uint8_Number_Condition_Judgement(uint8ConditionInfoArray[i].SignalIndex, uint8ConditionInfoArray[i].length, uint8ConditionInfoArray[i].Conditions);
		uint8_Signal_Condition_Judgement(uint8SignalConditionInfoArray[i].SignalIndex, uint8SignalConditionInfoArray[i].length, uint8SignalConditionInfoArray[i].Conditions);
	}
	for (int i = 0 ;i < TIME_FLAG_NUMBER; i++)
	{
		TimeOut_Condition_Judge(i);
	}

	for (int i = 1 ; i<BIT_SIGNAL_NUMBER ; i+=2)
	{
		P_SignalsAndConditions->Signal_Bit[i] = P_SignalsAndConditions->Signal_Bit[i - 1];
	}
	for (int i = 1 ; i<EEPROM_U8_SIGNAL_NUMBER ; i+=2)
	{
		P_SignalsAndConditions->Signal_EEPROM_U8[i] = P_SignalsAndConditions->Signal_EEPROM_U8[i - 1];
	}
	for (int i = 1 ; i<DOUBLE_SIGNAL_NUMBER ; i+=2)
	{
		P_SignalsAndConditions->Signal_double[i] = P_SignalsAndConditions->Signal_double[i - 1];
	}
	for (int i = 1 ; i<INT16_SIGNAL_NUMBER ; i+=2)
	{
		P_SignalsAndConditions->Signal_int16[i] = P_SignalsAndConditions->Signal_int16[i - 1];
	}
	for (int i = 1 ; i<INT32_SIGNAL_NUMBER ; i+=2)
	{
		P_SignalsAndConditions->Signal_int32[i] = P_SignalsAndConditions->Signal_int32[i - 1];
	}
	for (int i = 1 ; i<INT64_SIGNAL_NUMBER ; i+=2)
	{
		P_SignalsAndConditions->Signal_int64[i] = P_SignalsAndConditions->Signal_int64[i - 1];
	}
	for (int i = 1 ; i<INT8_SIGNAL_NUMBER ; i+=2)
	{
		P_SignalsAndConditions->Signal_int8[i] = P_SignalsAndConditions->Signal_int8[i - 1];
	}
	for (int i = 1 ; i<SINGLE_SIGNAL_NUMBER ; i+=2)
	{
		P_SignalsAndConditions->Signal_single[i] = P_SignalsAndConditions->Signal_single[i - 1];
	}
	for (int i = 1 ; i<UINT16_SIGNAL_NUMBER ; i+=2)
	{
		P_SignalsAndConditions->Signal_uint16[i] = P_SignalsAndConditions->Signal_uint16[i - 1];
	}
	for (int i = 1 ; i<UINT32_SIGNAL_NUMBER ; i+=2)
	{
		P_SignalsAndConditions->Signal_uint32[i] = P_SignalsAndConditions->Signal_uint32[i - 1];
	}
	for (int i = 1 ; i<UINT64_SIGNAL_NUMBER ; i+=2)
	{
		P_SignalsAndConditions->Signal_uint64[i] = P_SignalsAndConditions->Signal_uint64[i - 1];
	}
	for (int i = 1 ; i<UINT8_SIGNAL_NUMBER ; i+=2)
	{
		P_SignalsAndConditions->Signal_uint8[i] = P_SignalsAndConditions->Signal_uint8[i - 1];
	}

	memset(P_SignalsAndConditions->ConditionFlag, 0, sizeof(P_SignalsAndConditions->ConditionFlag));
}




void Bit_Number_Condition_Judgement(uint8 SignalIndex,int len,BitCondition* conditions)
{
	Bit SignalValue = P_SignalsAndConditions->Signal_Bit[SignalIndex];
	for (int i = 0; i<len ;i++)
	{
		Number_Condition_Judgement(BIT_CONDITION,&SignalValue,&conditions[i].Threshold,conditions[i].Symbol, conditions[i].EVT,conditions[i].ConditionIndex);
	}
}

void double_Number_Condition_Judgement(uint8 SignalIndex, int len, doubleCondition* conditions)
{
	double SignalValue = P_SignalsAndConditions->Signal_double[SignalIndex];
	for (int i = 0; i<len ;i++)
	{
		Number_Condition_Judgement(DOUBLE_CONDITION,&SignalValue,&conditions[i].Threshold,conditions[i].Symbol, conditions[i].EVT,conditions[i].ConditionIndex);
	}
}

void EEPROM_U8_Number_Condition_Judgement(uint8 SignalIndex, int len, EEPROM_U8Condition* conditions)
{
	uint8 SignalValue = P_SignalsAndConditions->Signal_EEPROM_U8[SignalIndex];
	for (int i = 0; i<len ;i++)
	{
		Number_Condition_Judgement(EEPROM_U8_CONDITION,&SignalValue,&conditions[i].Threshold,conditions[i].Symbol, conditions[i].EVT,conditions[i].ConditionIndex);
	}
}

void int16_Number_Condition_Judgement(uint8 SignalIndex, int len, int16Condition* conditions)
{
	int16 SignalValue = P_SignalsAndConditions->Signal_int16[SignalIndex];
	for (int i = 0; i<len ;i++)
	{
		Number_Condition_Judgement(INT16_CONDITION,&SignalValue,&conditions[i].Threshold,conditions[i].Symbol, conditions[i].EVT,conditions[i].ConditionIndex);
	}
}

void int32_Number_Condition_Judgement(uint8 SignalIndex, int len, int32Condition* conditions)
{
	int32 SignalValue = P_SignalsAndConditions->Signal_int32[SignalIndex];
	for (int i = 0; i<len ;i++)
	{
		Number_Condition_Judgement(INT32_CONDITION,&SignalValue,&conditions[i].Threshold,conditions[i].Symbol, conditions[i].EVT,conditions[i].ConditionIndex);
	}
}

void int64_Number_Condition_Judgement(uint8 SignalIndex, int len, int64Condition* conditions)
{
	int64 SignalValue = P_SignalsAndConditions->Signal_int64[SignalIndex];
	for (int i = 0; i<len ;i++)
	{
		Number_Condition_Judgement(INT64_CONDITION,&SignalValue,&conditions[i].Threshold,conditions[i].Symbol, conditions[i].EVT,conditions[i].ConditionIndex);
	}
}

void int8_Number_Condition_Judgement(uint8 SignalIndex, int len, int8Condition* conditions)
{
	int8 SignalValue = P_SignalsAndConditions->Signal_int8[SignalIndex];
	for (int i = 0; i<len ;i++)
	{
		Number_Condition_Judgement(INT8_CONDITION,&SignalValue,&conditions[i].Threshold,conditions[i].Symbol, conditions[i].EVT,conditions[i].ConditionIndex);
	}
}

void single_Number_Condition_Judgement(uint8 SignalIndex, int len, singleCondition* conditions)
{
	float SignalValue = P_SignalsAndConditions->Signal_single[SignalIndex];
	for (int i = 0; i<len ;i++)
	{
		Number_Condition_Judgement(SINGLE_CONDITION,&SignalValue,&conditions[i].Threshold,conditions[i].Symbol, conditions[i].EVT,conditions[i].ConditionIndex);
	}
}

void uint16_Number_Condition_Judgement(uint8 SignalIndex, int len, uint16Condition* conditions)
{
	uint16 SignalValue = P_SignalsAndConditions->Signal_uint16[SignalIndex];
	for (int i = 0; i<len ;i++)
	{
		Number_Condition_Judgement(UINT16_CONDITION,&SignalValue,&conditions[i].Threshold,conditions[i].Symbol, conditions[i].EVT,conditions[i].ConditionIndex);
	}
}

void uint32_Number_Condition_Judgement(uint8 SignalIndex, int len, uint32Condition* conditions)
{
	uint32 SignalValue = P_SignalsAndConditions->Signal_uint32[SignalIndex];
	for (int i = 0; i<len ;i++)
	{
		Number_Condition_Judgement(UINT32_CONDITION,&SignalValue,&conditions[i].Threshold,conditions[i].Symbol, conditions[i].EVT,conditions[i].ConditionIndex);
	}
}

void uint64_Number_Condition_Judgement(uint8 SignalIndex, int len, uint64Condition* conditions)
{
	uint64 SignalValue = P_SignalsAndConditions->Signal_uint64[SignalIndex];
	for (int i = 0; i<len ;i++)
	{
		Number_Condition_Judgement(UINT64_CONDITION,&SignalValue,&conditions[i].Threshold,conditions[i].Symbol, conditions[i].EVT,conditions[i].ConditionIndex);
	}
}

void uint8_Number_Condition_Judgement(uint8 SignalIndex, int len, uint8Condition* conditions)
{
	uint8 SignalValue = P_SignalsAndConditions->Signal_uint8[SignalIndex];
	for (int i = 0; i<len ;i++)
	{
		Number_Condition_Judgement(UINT8_CONDITION,&SignalValue,&conditions[i].Threshold,conditions[i].Symbol, conditions[i].EVT,conditions[i].ConditionIndex);
	}
}







void Bit_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions)
{
	Bit SignalValue = P_SignalsAndConditions->Signal_Bit[SignalIndex];
	Bit ThresholdValue = P_SignalsAndConditions->Signal_Bit[conditions[0].SignalIndex];
	for (int i = 0; i < len; i++)
	{
		Number_Condition_Judgement(BIT_CONDITION, &SignalValue, &ThresholdValue, conditions[i].Symbol, conditions[i].EVT, conditions[i].ConditionIndex);
	}
}

void double_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions)
{
	double SignalValue = P_SignalsAndConditions->Signal_double[SignalIndex];
	for (int i = 0; i < len; i++)
	{
		Number_Condition_Judgement(DOUBLE_CONDITION, &SignalValue, &conditions[i].SignalIndex, conditions[i].Symbol, conditions[i].EVT, conditions[i].ConditionIndex);
	}
}

void EEPROM_U8_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions)
{
	uint8 SignalValue = P_SignalsAndConditions->Signal_EEPROM_U8[SignalIndex];
	for (int i = 0; i < len; i++)
	{
		Number_Condition_Judgement(EEPROM_U8_CONDITION, &SignalValue, &conditions[i].SignalIndex, conditions[i].Symbol, conditions[i].EVT, conditions[i].ConditionIndex);
	}
}

void int16_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions)
{
	int16 SignalValue = P_SignalsAndConditions->Signal_int16[SignalIndex];
	for (int i = 0; i < len; i++)
	{
		Number_Condition_Judgement(INT16_CONDITION, &SignalValue, &conditions[i].SignalIndex, conditions[i].Symbol, conditions[i].EVT, conditions[i].ConditionIndex);
	}
}

void int32_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions)
{
	int32 SignalValue = P_SignalsAndConditions->Signal_int32[SignalIndex];
	for (int i = 0; i < len; i++)
	{
		Number_Condition_Judgement(INT32_CONDITION, &SignalValue, &conditions[i].SignalIndex, conditions[i].Symbol, conditions[i].EVT, conditions[i].ConditionIndex);
	}
}

void int64_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions)
{
	int64 SignalValue = P_SignalsAndConditions->Signal_int64[SignalIndex];
	for (int i = 0; i < len; i++)
	{
		Number_Condition_Judgement(INT64_CONDITION, &SignalValue, &conditions[i].SignalIndex, conditions[i].Symbol, conditions[i].EVT, conditions[i].ConditionIndex);
	}
}

void int8_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions)
{
	int8 SignalValue = P_SignalsAndConditions->Signal_int8[SignalIndex];
	for (int i = 0; i < len; i++)
	{
		Number_Condition_Judgement(INT8_CONDITION, &SignalValue, &conditions[i].SignalIndex, conditions[i].Symbol, conditions[i].EVT, conditions[i].ConditionIndex);
	}
}

void single_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions)
{
	float SignalValue = P_SignalsAndConditions->Signal_single[SignalIndex];
	for (int i = 0; i < len; i++)
	{
		Number_Condition_Judgement(SINGLE_CONDITION, &SignalValue, &conditions[i].SignalIndex, conditions[i].Symbol, conditions[i].EVT, conditions[i].ConditionIndex);
	}
}

void uint16_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions)
{
	uint16 SignalValue = P_SignalsAndConditions->Signal_uint16[SignalIndex];
	for (int i = 0; i < len; i++)
	{
		Number_Condition_Judgement(UINT16_CONDITION, &SignalValue, &conditions[i].SignalIndex, conditions[i].Symbol, conditions[i].EVT, conditions[i].ConditionIndex);
	}
}

void uint32_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions)
{
	uint32 SignalValue = P_SignalsAndConditions->Signal_uint32[SignalIndex];
	for (int i = 0; i < len; i++)
	{
		Number_Condition_Judgement(UINT32_CONDITION, &SignalValue, &conditions[i].SignalIndex, conditions[i].Symbol, conditions[i].EVT, conditions[i].ConditionIndex);
	}
}

void uint64_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions)
{
	uint64 SignalValue = P_SignalsAndConditions->Signal_uint64[SignalIndex];
	for (int i = 0; i < len; i++)
	{
		Number_Condition_Judgement(UINT64_CONDITION, &SignalValue, &conditions[i].SignalIndex, conditions[i].Symbol, conditions[i].EVT, conditions[i].ConditionIndex);
	}
}

void uint8_Signal_Condition_Judgement(uint8 SignalIndex, int len, SignalCondition* conditions)
{
	uint8 SignalValue = P_SignalsAndConditions->Signal_uint8[SignalIndex];
	for (int i = 0; i < len; i++)
	{
		Number_Condition_Judgement(UINT8_CONDITION, &SignalValue, &conditions[i].SignalIndex, conditions[i].Symbol, conditions[i].EVT, conditions[i].ConditionIndex);
	}
}










void Number_Condition_Judgement(ConditionType Type, void* P_SignalValue, void* P_Threshold, uint8 Symbol, void (*EVT)(), uint8 ConditionIndex)
{
	if (Type == BIT_CONDITION)
	{
		if (Symbol == EQ)
		{
			if (*(bool*)P_SignalValue == *(bool*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == NEQ)
		{
			if (*(bool*)P_SignalValue!= *(bool*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATER)
		{
			if (*(bool*)P_SignalValue > *(bool*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESS)
		{
			if (*(bool*)P_SignalValue < *(bool*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATEROREQ)
		{
			if (*(bool*)P_SignalValue >= *(bool*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESSOREQ)
		{
			if (*(bool*)P_SignalValue <= *(bool*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
	}
	else if (Type == DOUBLE_CONDITION)
	{
		if (Symbol == EQ)
		{
			if ((*(double*)P_SignalValue - *(double*)P_Threshold) < DOUBLE_EPS)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == NEQ)
		{
			if ((*(double*)P_SignalValue - *(double*)P_Threshold) > DOUBLE_EPS)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATER)
		{
			if (*(double*)P_SignalValue > *(double*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESS)
		{
			if (*(double*)P_SignalValue < *(double*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATEROREQ)
		{
			if (*(double*)P_SignalValue >= *(double*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESSOREQ)
		{
			if (*(double*)P_SignalValue <= *(double*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
	}

	else if (Type == EEPROM_U8_CONDITION)
	{
		if (Symbol == EQ)
		{
			if (*(uint8*)P_SignalValue == *(uint8*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == NEQ)
		{
			if (*(uint8*)P_SignalValue!= *(uint8*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATER)
		{
			if (*(uint8*)P_SignalValue > *(uint8*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESS)
		{
			if (*(uint8*)P_SignalValue < *(uint8*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATEROREQ)
		{
			if (*(uint8*)P_SignalValue >= *(uint8*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESSOREQ)
		{
			if (*(uint8*)P_SignalValue <= *(uint8*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
	}

	else if (Type == INT16_CONDITION)
	{
		if (Symbol == EQ)
		{
			if (*(int16*)P_SignalValue == *(int16*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == NEQ)
		{
			if (*(int16*)P_SignalValue != *(int16*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATER)
		{
			if (*(int16*)P_SignalValue > *(int16*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESS)
		{
			if (*(int16*)P_SignalValue < *(int16*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATEROREQ)
		{
			if (*(int16*)P_SignalValue >= *(int16*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESSOREQ)
		{
			if (*(int16*)P_SignalValue <= *(int16*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
	}

	else if (Type == INT32_CONDITION)
	{
		if (Symbol == EQ)
		{
			if (*(int32*)P_SignalValue == *(int32*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == NEQ)
		{
			if (*(int32*)P_SignalValue != *(int32*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATER)
		{
			if (*(int32*)P_SignalValue > *(int32*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESS)
		{
			if (*(int32*)P_SignalValue < *(int32*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATEROREQ)
		{
			if (*(int32*)P_SignalValue >= *(int32*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESSOREQ)
		{
			if (*(int32*)P_SignalValue <= *(int32*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
	}

	else if (Type == INT64_CONDITION)
	{
		if (Symbol == EQ)
		{
			if (*(int64*)P_SignalValue == *(int64*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == NEQ)
		{
			if (*(int64*)P_SignalValue != *(int64*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATER)
		{
			if (*(int64*)P_SignalValue > *(int64*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESS)
		{
			if (*(int64*)P_SignalValue < *(int64*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATEROREQ)
		{
			if (*(int64*)P_SignalValue >= *(int64*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESSOREQ)
		{
			if (*(int64*)P_SignalValue <= *(int64*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
	}

	else if (Type == INT8_CONDITION)
	{
		if (Symbol == EQ)
		{
			if (*(int8*)P_SignalValue == *(int8*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == NEQ)
		{
			if (*(int8*)P_SignalValue != *(int8*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATER)
		{
			if (*(int8*)P_SignalValue > *(int8*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESS)
		{
			if (*(int8*)P_SignalValue < *(int8*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATEROREQ)
		{
			if (*(int8*)P_SignalValue >= *(int8*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESSOREQ)
		{
			if (*(int8*)P_SignalValue <= *(int8*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
	}

	else if (Type == SINGLE_CONDITION)
	{
		if (Symbol == EQ)
		{
			if ((*(single*)P_SignalValue - *(single*)P_Threshold) < FLOAT_EPS)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == NEQ)
		{
			if ((*(single*)P_SignalValue - *(single*)P_Threshold)> FLOAT_EPS)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATER)
		{
			if (*(single*)P_SignalValue > *(single*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESS)
		{
			if (*(single*)P_SignalValue < *(single*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATEROREQ)
		{
			if (*(single*)P_SignalValue >= *(single*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESSOREQ)
		{
			if (*(single*)P_SignalValue <= *(single*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
	}

	else if (Type == UINT16_CONDITION)
	{
		if (Symbol == EQ)
		{
			if (*(uint16*)P_SignalValue == *(uint16*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == NEQ)
		{
			if (*(uint16*)P_SignalValue != *(uint16*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATER)
		{
			if (*(uint16*)P_SignalValue > *(uint16*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESS)
		{
			if (*(uint16*)P_SignalValue < *(uint16*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATEROREQ)
		{
			if (*(uint16*)P_SignalValue >= *(uint16*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESSOREQ)
		{
			if (*(uint16*)P_SignalValue <= *(uint16*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		}

	else if (Type == UINT32_CONDITION)
	{
		if (Symbol == EQ)
		{
			if (*(uint32*)P_SignalValue == *(uint32*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == NEQ)
		{
			if (*(uint32*)P_SignalValue != *(uint32*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATER)
		{
			if (*(uint32*)P_SignalValue > *(uint32*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESS)
		{
			if (*(uint32*)P_SignalValue < *(uint32*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATEROREQ)
		{
			if (*(uint32*)P_SignalValue >= *(uint32*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESSOREQ)
		{
			if (*(uint32*)P_SignalValue <= *(uint32*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		}

	else if (Type == INT64_CONDITION)
	{
		if (Symbol == EQ)
		{
			if (*(uint64*)P_SignalValue == *(uint64*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == NEQ)
		{
			if (*(uint64*)P_SignalValue != *(uint64*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATER)
		{
			if (*(uint64*)P_SignalValue > *(uint64*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESS)
		{
			if (*(uint64*)P_SignalValue < *(uint64*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATEROREQ)
		{
			if (*(uint64*)P_SignalValue >= *(uint64*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESSOREQ)
		{
			if (*(uint64*)P_SignalValue <= *(uint64*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		}

	else if (Type == UINT8_CONDITION)
	{
		if (Symbol == EQ)
		{
			if (*(uint8*)P_SignalValue == *(uint8*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == NEQ)
		{
			if (*(uint8*)P_SignalValue != *(uint8*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATER)
		{
			if (*(uint8*)P_SignalValue > *(uint8*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESS)
		{
			if (*(uint8*)P_SignalValue < *(uint8*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == GREATEROREQ)
		{
			if (*(uint8*)P_SignalValue >= *(uint8*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
		else if (Symbol == LESSOREQ)
		{
			if (*(uint8*)P_SignalValue <= *(uint8*)P_Threshold)
			{
				P_SignalsAndConditions->ConditionFlag[ConditionIndex] = true;
				EVT();
			}
		}
	}

}
	
void TimeOut_Condition_Judge(uint8 SignalIndex)
{
	if (P_SignalsAndConditions->TimeOutFlag[SignalIndex] == true)
	{
		TimeOutActionArray[SignalIndex].EVT();
	}
}

