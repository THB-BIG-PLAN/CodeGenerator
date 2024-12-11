
#ifndef CONDITION_H_
#define CONDITION_H_
#include <Type_define.h>
#include "EVT/Event/EVT.h"
#include "EVT/Logic/Logic.h"
#include <sgn/signal_api.h>
#include <stdbool.h>

#define PPL_boolPosnLampSts 0
#define PPL_boolPosnLampSts_Pre 1
#define EEP_LOGO_ENABLE_FLAG 2
#define EEP_LOGO_ENABLE_FLAG_Pre 3
#define BdcSeedsignal 4
#define BdcSeedsignal_Pre 5
#define BdcWlcmsignal 6
#define BdcWlcmsignal_Pre 7
#define DLC_u8TurnLightTwice 8
#define DLC_u8TurnLightTwice_Pre 9
#define EspAutoHoldActvSts 10
#define EspAutoHoldActvSts_Pre 11
#define PLB_u8LBSts 12
#define PLB_u8LBSts_Pre 13
#define PRM_u8PowerSts 14
#define PRM_u8PowerSts_Pre 15
#define VcuGearPosn 16
#define VcuGearPosn_Pre 17

#define CONDITION_TYPE_NUMBER 0
#define CONDITION_TYPE_SIGNAL 1

#define BDCSEEDSIGNAL_NEQ_0 0
#define BDCSEEDSIGNAL_CHANGE_BdcSeedsignal_PRE 1
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

#define EQ 0
#define NEQ 1
#define GREATER 2
#define GREATEROREQ 3
#define LESS 4
#define LESSOREQ 5
#define CHANGE 6
#define INVALID 7

#define LGL_SEE_350ms_TimeOut 0
#define LGL_EEP_350ms_TimeOut 1
#define LGL_PRM_350ms_TimeOut 2
#define LGL_DLC_1500ms_TimeOut 3

#define SIGNAL_NUMBER 18
#define TIME_FLAG_NUMBER 4
#define CONDITION_NUMBER 22

typedef struct Condition {
bool Type;
T_u8 Threshold;
T_u8 Symbol;
void (*EVT)();
T_u8 ConditionID;
} Condition;

typedef struct SignalCondition {
    T_u8 Signal;
    T_u8 Len;
    const Condition* Condition;
} SignalCondition;

typedef struct EVT_FLAG {
    T_u8 SignalNum[SIGNAL_NUM];
    T_u8 SignalPreNum[SIGNAL_NUM];
    T_u8 LGL_TimeOutFlagNum;
    T_bit TimeOutFlag[TIMEOUT_NUM];
    T_bit ConditionFlag[CONDITION_NUM];
} EVT_FLAG;

extern EVT_FLAG* EVT_flag;
static const SignalCondition SignalConditionArray[SIGNAL_NUM];
static const Condition TimeOutActionArray[TIMEOUT_NUM];
#endif /*CONDITION_H_*/
