
#include "EVT/Condition/Condition.h"


const Condition BdcSeedsignal_Condition [4] = {{CONDITION_TYPE_NUMBER, 0, NEQ, &LGL_SEE_ON, BDCSEEDSIGNAL_NEQ_0},{CONDITION_TYPE_SIGNAL, BdcSeedsignal_Pre_SIGNALNUM, CHANGE, &LGL_SEE_REQ2NO, BDCSEEDSIGNAL_CHANGE_BdcSeedsignal_PRE},{CONDITION_TYPE_NUMBER, 0, EQ, &LGL_SEE_REQ2NO, BDCSEEDSIGNAL_EQ_0},{CONDITION_TYPE_NUMBER, 0, EQ, &LGL_Normal_OFF, BDCSEEDSIGNAL_EQ_0}};
const Condition BdcWlcmsignal_Condition [2] = {{CONDITION_TYPE_NUMBER, 0, NEQ, &LGL_WEL_ON, BDCWLCMSIGNAL_NEQ_0},{CONDITION_TYPE_NUMBER, 0, EQ, &LGL_Normal_OFF, BDCWLCMSIGNAL_EQ_0}};
const Condition DLC_u8TurnLightTwice_Condition [1] = {{CONDITION_TYPE_SIGNAL, DLC_u8TurnLightTwice_Pre_SIGNALNUM, CHANGE, &LGL_DLC_TUL_ON, DLC_U8TURNLIGHTTWICE_CHANGE_DLC_U8TURNLIGHTTWICE_PRE}};
const Condition EEP_LOGO_ENABLE_FLAG_Condition [4] = {{CONDITION_TYPE_NUMBER, 1, EQ, &LGL_PRM_EEP_ON, EEP_LOGO_ENABLE_FLAG_EQ_1},{CONDITION_TYPE_SIGNAL, EEP_LOGO_ENABLE_FLAG_Pre_SIGNALNUM, CHANGE, &LGL_EEP_ENABLE2DISABLE, EEP_LOGO_ENABLE_FLAG_CHANGE_EEP_LOGO_ENABLE_FLAG_PRE},{CONDITION_TYPE_NUMBER, 0, EQ, &LGL_EEP_ENABLE2DISABLE, EEP_LOGO_ENABLE_FLAG_EQ_0},{CONDITION_TYPE_NUMBER, 0, EQ, &LGL_Normal_OFF, EEP_LOGO_ENABLE_FLAG_EQ_0}};
const Condition EspAutoHoldActvSts_Condition [3] = {{CONDITION_TYPE_NUMBER, 0, EQ, &LGL_Normal_OFF, ESPAUTOHOLDACTVSTS_EQ_0},{CONDITION_TYPE_NUMBER, 1, EQ, &LGL_ESP_POL_ON, ESPAUTOHOLDACTVSTS_EQ_1},{CONDITION_TYPE_NUMBER, 1, EQ, &LGL_ESP_LBL_ON, ESPAUTOHOLDACTVSTS_EQ_1}};
const Condition PLB_u8LBSts_Condition [3] = {{CONDITION_TYPE_NUMBER, 1, EQ, &LGL_ESP_LBL_ON, PLB_U8LBSTS_EQ_1},{CONDITION_TYPE_NUMBER, 0, EQ, &LGL_Normal_OFF, PLB_U8LBSTS_EQ_0},{CONDITION_TYPE_NUMBER, 1, EQ, &LGL_VCU_LBL_ON, PLB_U8LBSTS_EQ_1}};
const Condition PPL_boolPosnLampSts_Condition [3] = {{CONDITION_TYPE_NUMBER, 0, EQ, &LGL_Normal_OFF, PPL_BOOLPOSNLAMPSTS_EQ_0},{CONDITION_TYPE_NUMBER, 1, EQ, &LGL_ESP_POL_ON, PPL_BOOLPOSNLAMPSTS_EQ_1},{CONDITION_TYPE_NUMBER, 1, EQ, &LGL_VCU_POL_ON, PPL_BOOLPOSNLAMPSTS_EQ_1}};
const Condition PRM_u8PowerSts_Condition [3] = {{CONDITION_TYPE_NUMBER, 2, EQ, &LGL_PRM_EEP_ON, PRM_U8POWERSTS_EQ_2},{CONDITION_TYPE_SIGNAL, PRM_u8PowerSts_Pre_SIGNALNUM, CHANGE, &LGL_PRM_ON2NOTON, PRM_U8POWERSTS_CHANGE_PRM_U8POWERSTS_PRE},{CONDITION_TYPE_NUMBER, 0, EQ, &LGL_Normal_OFF, PRM_U8POWERSTS_EQ_0}};
const Condition PRM_u8PowerSts_Pre_Condition [1] = {{CONDITION_TYPE_NUMBER, 2, EQ, &LGL_PRM_ON2NOTON, PRM_U8POWERSTS_PRE_EQ_2}};
const Condition VcuGearPosn_Condition [5] = {{CONDITION_TYPE_NUMBER, 0, EQ, &LGL_Normal_OFF, VCUGEARPOSN_EQ_0},{CONDITION_TYPE_NUMBER, 1, EQ, &LGL_VCU_LBL_ON, VCUGEARPOSN_EQ_1},{CONDITION_TYPE_NUMBER, 1, EQ, &LGL_VCU_POL_ON, VCUGEARPOSN_EQ_1},{CONDITION_TYPE_SIGNAL, DLC_u8TurnLightTwice_SIGNALNUM, NEQ, &LGL_Normal_OFF, VCUGEARPOSN_NEQ_DLC_U8TURNLIGHTTWICE},{CONDITION_TYPE_NUMBER, 3, EQ, &LGL_Normal_OFF, VCUGEARPOSN_EQ_3}};
const Condition VcuGearPosn_Pre_Condition [1] = {{CONDITION_TYPE_NUMBER, 2, EQ, &LGL_Normal_OFF, VCUGEARPOSN_PRE_EQ_2}};

static const SignalCondition SignalConditionArray[SIGNAL_NUM] = {
{BdcSeedsignal_SIGNALNUM, Type_uint8 , 4 , &BdcSeedsignal_Condition},
{BdcWlcmsignal_SIGNALNUM, Type_uint8 , 2 , &BdcWlcmsignal_Condition},
{DLC_u8TurnLightTwice_SIGNALNUM, Type_uint8 , 1 , &DLC_u8TurnLightTwice_Condition},
{EEP_LOGO_ENABLE_FLAG_SIGNALNUM, Type_EEPROM_U8 , 4 , &EEP_LOGO_ENABLE_FLAG_Condition},
{EspAutoHoldActvSts_SIGNALNUM, Type_uint8 , 3 , &EspAutoHoldActvSts_Condition},
{PLB_u8LBSts_SIGNALNUM, Type_uint8 , 3 , &PLB_u8LBSts_Condition},
{PPL_boolPosnLampSts_SIGNALNUM, Type_Bit , 3 , &PPL_boolPosnLampSts_Condition},
{PRM_u8PowerSts_SIGNALNUM, Type_uint8 , 3 , &PRM_u8PowerSts_Condition},
{PRM_u8PowerSts_Pre_SIGNALNUM, Type_uint8 , 1 , &PRM_u8PowerSts_Pre_Condition},
{VcuGearPosn_SIGNALNUM, Type_uint8 , 5 , &VcuGearPosn_Condition},
{VcuGearPosn_Pre_SIGNALNUM, Type_uint8, 1 , &VcuGearPosn_Pre_Condition}};

const Condition TimeOutActionArray[TIMEOUT_NUM] = {
{1,EQ,LGL_SEE_350ms_TimeOut,0}
{1,EQ,LGL_EEP_350ms_TimeOut,0}
{1,EQ,LGL_PRM_350ms_TimeOut,0}
{1,EQ,LGL_DLC_1500ms_TimeOut,0}
};

