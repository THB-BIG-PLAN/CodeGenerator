
#ifndef CONDITION_H_
#define CONDITION_H_
#include <Type_define.h>
#include "EVT/Event/EVT.h"
#include "EVT/Logic/Logic.h"
#include <sgn/signal_api.h>
#include <stdbool.h>
#include <stdint.h>

#define PPL_boolPosnLampSts_SIGNALNUM 0
#define PPL_boolPosnLampSts_Pre_SIGNALNUM 1
#define EEP_LOGO_ENABLE_FLAG_SIGNALNUM 0
#define EEP_LOGO_ENABLE_FLAG_Pre_SIGNALNUM 1
#define BdcSeedsignal_SIGNALNUM 0
#define BdcSeedsignal_Pre_SIGNALNUM 1
#define BdcWlcmsignal_SIGNALNUM 2
#define BdcWlcmsignal_Pre_SIGNALNUM 3
#define DLC_u8TurnLightTwice_SIGNALNUM 4
#define DLC_u8TurnLightTwice_Pre_SIGNALNUM 5
#define EspAutoHoldActvSts_SIGNALNUM 6
#define EspAutoHoldActvSts_Pre_SIGNALNUM 7
#define PLB_u8LBSts_SIGNALNUM 8
#define PLB_u8LBSts_Pre_SIGNALNUM 9
#define PRM_u8PowerSts_SIGNALNUM 10
#define PRM_u8PowerSts_Pre_SIGNALNUM 11
#define VcuGearPosn_SIGNALNUM 12
#define VcuGearPosn_Pre_SIGNALNUM 13


#define BIT_SIGNAL_NUMBER 2
#define DOUBLE_SIGNAL_NUMBER 0
#define EEPROM_U8_SIGNAL_NUMBER 2
#define INT16_SIGNAL_NUMBER 0
#define INT32_SIGNAL_NUMBER 0
#define INT64_SIGNAL_NUMBER 0
#define INT8_SIGNAL_NUMBER 0
#define SINGLE_SIGNAL_NUMBER 0
#define UINT16_SIGNAL_NUMBER 0
#define UINT32_SIGNAL_NUMBER 0
#define UINT64_SIGNAL_NUMBER 0
#define UINT8_SIGNAL_NUMBER 14


#define EQ 0
#define NEQ 1
#define GREATER 2
#define GREATEROREQ 3
#define LESS 4
#define LESSOREQ 5
#define CHANGE 6
#define INVALID 7


#define BDCSEEDSIGNAL_NEQ_0 0
#define BDCSEEDSIGNAL_CHANGE_BDCSEEDSIGNAL_PRE 1
#define BDCSEEDSIGNAL_EQ_0 2
#define BDCWLCMSIGNAL_NEQ_0 3
#define BDCWLCMSIGNAL_EQ_0 4
#define DLC_U8TURNLIGHTTWICE_CHANGE_DLC_U8TURNLIGHTTWICE_PRE 5
#define EEP_LOGO_ENABLE_FLAG_EQ_1 6
#define EEP_LOGO_ENABLE_FLAG_CHANGE_EEP_LOGO_ENABLE_FLAG_PRE 7
#define EEP_LOGO_ENABLE_FLAG_EQ_0 8
#define ESPAUTOHOLDACTVSTS_EQ_0 9
#define ESPAUTOHOLDACTVSTS_EQ_1 10
#define PLB_U8LBSTS_EQ_1 11
#define PLB_U8LBSTS_EQ_0 12
#define PPL_BOOLPOSNLAMPSTS_EQ_0 13
#define PPL_BOOLPOSNLAMPSTS_EQ_1 14
#define PRM_U8POWERSTS_EQ_2 15
#define PRM_U8POWERSTS_CHANGE_PRM_U8POWERSTS_PRE 16
#define PRM_U8POWERSTS_EQ_0 17
#define PRM_U8POWERSTS_PRE_EQ_2 18
#define VCUGEARPOSN_EQ_0 19
#define VCUGEARPOSN_EQ_1 20
#define VCUGEARPOSN_NEQ_DLC_U8TURNLIGHTTWICE 21
#define VCUGEARPOSN_EQ_3 22
#define VCUGEARPOSN_PRE_EQ_2 23
#define TIMEFLAGNUM_EQ_0 24


#define LGL_SEE_350ms_TimeOut 0
#define LGL_EEP_350ms_TimeOut 1
#define LGL_PRM_350ms_TimeOut 2
#define LGL_DLC_1500ms_TimeOut 3


#define TIME_FLAG_NUMBER 4
#define CONDITION_NUMBER 25
typedef struct 
{
	Bit Threshold;
	uint8 Symbol;
	void (*EVT)();
	uint8 ConditionIndex;
}BitCondition;

typedef struct 
{
	double Threshold;
	uint8 Symbol;
	void (*EVT)();
	uint8 ConditionIndex;
}doubleCondition;

typedef struct 
{
	EEPROM_U8 Threshold;
	uint8 Symbol;
	void (*EVT)();
	uint8 ConditionIndex;
}EEPROM_U8Condition;

typedef struct 
{
	int16 Threshold;
	uint8 Symbol;
	void (*EVT)();
	uint8 ConditionIndex;
}int16Condition;

typedef struct 
{
	int32 Threshold;
	uint8 Symbol;
	void (*EVT)();
	uint8 ConditionIndex;
}int32Condition;

typedef struct 
{
	int64 Threshold;
	uint8 Symbol;
	void (*EVT)();
	uint8 ConditionIndex;
}int64Condition;

typedef struct 
{
	int8 Threshold;
	uint8 Symbol;
	void (*EVT)();
	uint8 ConditionIndex;
}int8Condition;

typedef struct 
{
	single Threshold;
	uint8 Symbol;
	void (*EVT)();
	uint8 ConditionIndex;
}singleCondition;

typedef struct 
{
	uint16 Threshold;
	uint8 Symbol;
	void (*EVT)();
	uint8 ConditionIndex;
}uint16Condition;

typedef struct 
{
	uint32 Threshold;
	uint8 Symbol;
	void (*EVT)();
	uint8 ConditionIndex;
}uint32Condition;

typedef struct 
{
	uint64 Threshold;
	uint8 Symbol;
	void (*EVT)();
	uint8 ConditionIndex;
}uint64Condition;

typedef struct 
{
	uint8 Threshold;
	uint8 Symbol;
	void (*EVT)();
	uint8 ConditionIndex;
}uint8Condition;

typedef struct 
{
	uint8 SignalIndex;
	uint8 Symbol;
	void (*EVT)();
	uint8 ConditionIndex;
}SignalCondition;

typedef struct 
{
	Bit Threshold;
	uint8 Symbol;
	void (*EVT)();
	uint8 ConditionIndex;
}TimeOutCondition;

typedef struct 
{
	uint8 SignalIndex;
	uint8 length;
	BitCondition *Conditions;
}BitSignalConditionInfo;

typedef struct 
{
	uint8 SignalIndex;
	uint8 length;
	doubleCondition *Conditions;
}doubleSignalConditionInfo;

typedef struct 
{
	uint8 SignalIndex;
	uint8 length;
	EEPROM_U8Condition *Conditions;
}EEPROM_U8SignalConditionInfo;

typedef struct 
{
	uint8 SignalIndex;
	uint8 length;
	int16Condition *Conditions;
}int16SignalConditionInfo;

typedef struct 
{
	uint8 SignalIndex;
	uint8 length;
	int32Condition *Conditions;
}int32SignalConditionInfo;

typedef struct 
{
	uint8 SignalIndex;
	uint8 length;
	int64Condition *Conditions;
}int64SignalConditionInfo;

typedef struct 
{
	uint8 SignalIndex;
	uint8 length;
	int8Condition *Conditions;
}int8SignalConditionInfo;

typedef struct 
{
	uint8 SignalIndex;
	uint8 length;
	singleCondition *Conditions;
}singleSignalConditionInfo;

typedef struct 
{
	uint8 SignalIndex;
	uint8 length;
	uint16Condition *Conditions;
}uint16SignalConditionInfo;

typedef struct 
{
	uint8 SignalIndex;
	uint8 length;
	uint32Condition *Conditions;
}uint32SignalConditionInfo;

typedef struct 
{
	uint8 SignalIndex;
	uint8 length;
	uint64Condition *Conditions;
}uint64SignalConditionInfo;

typedef struct 
{
	uint8 SignalIndex;
	uint8 length;
	uint8Condition *Conditions;
}uint8SignalConditionInfo;

typedef struct 
{
	uint8 SignalIndex;
	uint8 length;
	SignalCondition *Conditions;
}SignalConditionInfo;

typedef struct 
{
	Bit Signal_Bit[BIT_SIGNAL_NUMBER];
	double Signal_double[DOUBLE_SIGNAL_NUMBER];
	EEPROM_U8 Signal_EEPROM_U8[EEPROM_U8_SIGNAL_NUMBER];
	int16 Signal_int16[INT16_SIGNAL_NUMBER];
	int32 Signal_int32[INT32_SIGNAL_NUMBER];
	int64 Signal_int64[INT64_SIGNAL_NUMBER];
	int8 Signal_int8[INT8_SIGNAL_NUMBER];
	single Signal_single[SINGLE_SIGNAL_NUMBER];
	uint16 Signal_uint16[UINT16_SIGNAL_NUMBER];
	uint32 Signal_uint32[UINT32_SIGNAL_NUMBER];
	uint64 Signal_uint64[UINT64_SIGNAL_NUMBER];
	uint8 Signal_uint8[UINT8_SIGNAL_NUMBER];

	uint8 TimeOutFlagNum;
	Bit TimeOutFlag[TIME_FLAG_NUMBER];
	Bit ConditionFlag[CONDITION_NUMBER];
}SignalsAndConditions;

static const BitSignalConditionInfo BitConditionInfoArray[BIT_SIGNAL_NUMBER];
static const doubleSignalConditionInfo doubleConditionInfoArray[DOUBLE_SIGNAL_NUMBER];
static const EEPROM_U8SignalConditionInfo EEPROM_U8ConditionInfoArray[EEPROM_U8_SIGNAL_NUMBER];
static const int16SignalConditionInfo int16ConditionInfoArray[INT16_SIGNAL_NUMBER];
static const int32SignalConditionInfo int32ConditionInfoArray[INT32_SIGNAL_NUMBER];
static const int64SignalConditionInfo int64ConditionInfoArray[INT64_SIGNAL_NUMBER];
static const int8SignalConditionInfo int8ConditionInfoArray[INT8_SIGNAL_NUMBER];
static const singleSignalConditionInfo singleConditionInfoArray[SINGLE_SIGNAL_NUMBER];
static const uint16SignalConditionInfo uint16ConditionInfoArray[UINT16_SIGNAL_NUMBER];
static const uint32SignalConditionInfo uint32ConditionInfoArray[UINT32_SIGNAL_NUMBER];
static const uint64SignalConditionInfo uint64ConditionInfoArray[UINT64_SIGNAL_NUMBER];
static const uint8SignalConditionInfo uint8ConditionInfoArray[UINT8_SIGNAL_NUMBER];


static const SignalConditionInfo BitSignalConditionInfoArray[BIT_SIGNAL_NUMBER];
static const SignalConditionInfo doubleSignalConditionInfoArray[DOUBLE_SIGNAL_NUMBER];
static const SignalConditionInfo EEPROM_U8SignalConditionInfoArray[EEPROM_U8_SIGNAL_NUMBER];
static const SignalConditionInfo int16SignalConditionInfoArray[INT16_SIGNAL_NUMBER];
static const SignalConditionInfo int32SignalConditionInfoArray[INT32_SIGNAL_NUMBER];
static const SignalConditionInfo int64SignalConditionInfoArray[INT64_SIGNAL_NUMBER];
static const SignalConditionInfo int8SignalConditionInfoArray[INT8_SIGNAL_NUMBER];
static const SignalConditionInfo singleSignalConditionInfoArray[SINGLE_SIGNAL_NUMBER];
static const SignalConditionInfo uint16SignalConditionInfoArray[UINT16_SIGNAL_NUMBER];
static const SignalConditionInfo uint32SignalConditionInfoArray[UINT32_SIGNAL_NUMBER];
static const SignalConditionInfo uint64SignalConditionInfoArray[UINT64_SIGNAL_NUMBER];
static const SignalConditionInfo uint8SignalConditionInfoArray[UINT8_SIGNAL_NUMBER];


static const TimeOutCondition TimeOutActionArray[TIME_FLAG_NUMBER];
extern SignalsAndConditions *P_SignalsAndConditions;
#endif
