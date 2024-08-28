
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





#define BdcSeedsignal_SIGNALNUM 0
#define BdcWlcmsignal_SIGNALNUM 1
#define DLC_u8TurnLightTwice_SIGNALNUM 2
#define EEP_LOGO_ENABLE_FLAG_SIGNALNUM 3
#define EspAutoHoldActvSts_SIGNALNUM 4
#define PLB_u8LBSts_SIGNALNUM 5
#define PPL_boolPosnLampSts_SIGNALNUM 6
#define PRM_u8PowerSts_SIGNALNUM 7
#define VcuGearPosn_SIGNALNUM 8



#define BDCSEEDSIGNAL_NEQ_0 0
#define BDCSEEDSIGNAL_CHANGETO_0 1
#define BDCSEEDSIGNAL_EQ_0 2
#define BDCWLCMSIGNAL_NEQ_0 3
#define BDCWLCMSIGNAL_EQ_0 4
#define DLC_U8TURNLIGHTTWICE_CHANGE_0XFF 5
#define EEP_LOGO_ENABLE_FLAG_EQ_1 6
#define EEP_LOGO_ENABLE_FLAG_CHANGETO_0 7
#define EEP_LOGO_ENABLE_FLAG_EQ_0 8
#define ESPAUTOHOLDACTVSTS_EQ_0 9
#define ESPAUTOHOLDACTVSTS_EQ_1 10
#define PLB_U8LBSTS_EQ_0 11
#define PLB_U8LBSTS_EQ_1 12
#define PPL_BOOLPOSNLAMPSTS_EQ_0 13
#define PPL_BOOLPOSNLAMPSTS_EQ_1 14
#define PRM_U8POWERSTS_EQ_2 15
#define PRM_U8POWERSTS_CHANGETO_1 16
#define PRM_U8POWERSTS_CHANGETO_0 17
#define PRM_U8POWERSTS_EQ_0 18
#define VCUGEARPOSN_EQ_0 19
#define VCUGEARPOSN_EQ_1 20
#define LGL_TIMEFLAGNUM_EQ_0 21



#define LGL_SEE_350ms_TimeOut 0
#define LGL_EEP_350ms_TimeOut 1
#define LGL_PRM_350ms_TimeOut 2
#define LGL_DLC_1500ms_TimeOut 3



#define SIGNAL_NUM 9
#define TIMEOUT_NUM 4
#define CONDITION_NUM 22



typedef struct Condition{
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
