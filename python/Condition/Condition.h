
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

#define CONDITION_TYPE_NUMBER 0
#define CONDITION_TYPE_SIGNAL 1

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
#define CONDITION_NUMBER 25

typedef struct Condition {
    Bit Type;
    uint8 Threshold;
    uint8 Symbol;
    void (*EVT)();
    uint8 ConditionID;
} Condition;

enum SignalType {
    Type_Bit,
    Type_double,
    Type_EEPROM_U8,
    Type_int16,
    Type_int32,
    Type_int64,
    Type_int8,
    Type_single,
    Type_uint16,
    Type_uint32,
    Type_uint64,
    Type_uint8,
};

typedef struct SignalCondition {
    uint8 Signal;
    enum SignalType Type;
    uint8 Len;
    const Condition* Condition;
} SignalCondition;

typedef struct EVT_FLAG {
    Bit Signal_Bit[2];
    EEPROM_U8 Signal_EEPROM_U8[2];
    uint8 Signal_uint8[14];
    uint8 TimeOutFlagNum;
    Bit TimeOutFlag[TIME_FLAG_NUMBER];
    Bit ConditionFlag[CONDITION_NUMBER];
} EVT_FLAG;

extern EVT_FLAG* EVT_flag;
static const SignalCondition SignalConditionArray[SIGNAL_NUMBER];
static const Condition TimeOutActionArray[TIME_FLAG_NUMBER];
#endif // CONDITION_H_
