#include "EVT/Condition/Condition.h"

const BitCondition PPL_boolPosnLampSts_Conditions[3] = {{0, EQ, LGL_Normal_OFF, PPL_BOOLPOSNLAMPSTS_EQ_0} , {1, EQ, LGL_ESP_POL_ON, PPL_BOOLPOSNLAMPSTS_EQ_1} , {1, EQ, LGL_VCU_POL_ON, PPL_BOOLPOSNLAMPSTS_EQ_1}};
const BitCondition PPL_boolPosnLampSts_Pre_Conditions[0] = {};
const EEPROM_U8Condition EEP_LOGO_ENABLE_FLAG_Conditions[3] = {{1, EQ, LGL_PRM_EEP_ON, EEP_LOGO_ENABLE_FLAG_EQ_1} , {0, EQ, LGL_EEP_ENABLE2DISABLE, EEP_LOGO_ENABLE_FLAG_EQ_0} , {0, EQ, LGL_Normal_OFF, EEP_LOGO_ENABLE_FLAG_EQ_0}};
const EEPROM_U8Condition EEP_LOGO_ENABLE_FLAG_Pre_Conditions[0] = {};
const uint8Condition BdcSeedsignal_Conditions[3] = {{0, NEQ, LGL_SEE_ON, BDCSEEDSIGNAL_NEQ_0} , {0, EQ, LGL_SEE_REQ2NO, BDCSEEDSIGNAL_EQ_0} , {0, EQ, LGL_Normal_OFF, BDCSEEDSIGNAL_EQ_0}};
const uint8Condition BdcSeedsignal_Pre_Conditions[0] = {};
const uint8Condition BdcWlcmsignal_Conditions[2] = {{0, NEQ, LGL_WEL_ON, BDCWLCMSIGNAL_NEQ_0} , {0, EQ, LGL_Normal_OFF, BDCWLCMSIGNAL_EQ_0}};
const uint8Condition BdcWlcmsignal_Pre_Conditions[0] = {};
const uint8Condition DLC_u8TurnLightTwice_Conditions[0] = {};
const uint8Condition DLC_u8TurnLightTwice_Pre_Conditions[0] = {};
const uint8Condition EspAutoHoldActvSts_Conditions[3] = {{0, EQ, LGL_Normal_OFF, ESPAUTOHOLDACTVSTS_EQ_0} , {1, EQ, LGL_ESP_POL_ON, ESPAUTOHOLDACTVSTS_EQ_1} , {1, EQ, LGL_ESP_LBL_ON, ESPAUTOHOLDACTVSTS_EQ_1}};
const uint8Condition EspAutoHoldActvSts_Pre_Conditions[0] = {};
const uint8Condition PLB_u8LBSts_Conditions[3] = {{1, EQ, LGL_ESP_LBL_ON, PLB_U8LBSTS_EQ_1} , {0, EQ, LGL_Normal_OFF, PLB_U8LBSTS_EQ_0} , {1, EQ, LGL_VCU_LBL_ON, PLB_U8LBSTS_EQ_1}};
const uint8Condition PLB_u8LBSts_Pre_Conditions[0] = {};
const uint8Condition PRM_u8PowerSts_Conditions[2] = {{2, EQ, LGL_PRM_EEP_ON, PRM_U8POWERSTS_EQ_2} , {0, EQ, LGL_Normal_OFF, PRM_U8POWERSTS_EQ_0}};
const uint8Condition PRM_u8PowerSts_Pre_Conditions[1] = {{2, EQ, LGL_PRM_ON2NOTON, PRM_U8POWERSTS_PRE_EQ_2}};
const uint8Condition VcuGearPosn_Conditions[4] = {{0, EQ, LGL_Normal_OFF, VCUGEARPOSN_EQ_0} , {1, EQ, LGL_VCU_LBL_ON, VCUGEARPOSN_EQ_1} , {1, EQ, LGL_VCU_POL_ON, VCUGEARPOSN_EQ_1} , {3, EQ, LGL_Normal_OFF, VCUGEARPOSN_EQ_3}};
const uint8Condition VcuGearPosn_Pre_Conditions[1] = {{2, EQ, LGL_Normal_OFF, VCUGEARPOSN_PRE_EQ_2}};


const SignalCondition PPL_boolPosnLampSts_SignalConditions[0] = {};
const SignalCondition PPL_boolPosnLampSts_Pre_SignalConditions[0] = {};
const SignalCondition EEP_LOGO_ENABLE_FLAG_SignalConditions[1] = {{EEP_LOGO_ENABLE_FLAG_Pre_SIGNALNUM, CHANGE, &LGL_EEP_ENABLE2DISABLE, EEP_LOGO_ENABLE_FLAG_CHANGE_EEP_LOGO_ENABLE_FLAG_PRE}};
const SignalCondition EEP_LOGO_ENABLE_FLAG_Pre_SignalConditions[0] = {};
const SignalCondition BdcSeedsignal_SignalConditions[1] = {{BdcSeedsignal_Pre_SIGNALNUM, CHANGE, &LGL_SEE_REQ2NO, BDCSEEDSIGNAL_CHANGE_BDCSEEDSIGNAL_PRE}};
const SignalCondition BdcSeedsignal_Pre_SignalConditions[0] = {};
const SignalCondition BdcWlcmsignal_SignalConditions[0] = {};
const SignalCondition BdcWlcmsignal_Pre_SignalConditions[0] = {};
const SignalCondition DLC_u8TurnLightTwice_SignalConditions[1] = {{DLC_u8TurnLightTwice_Pre_SIGNALNUM, CHANGE, &LGL_DLC_TUL_ON, DLC_U8TURNLIGHTTWICE_CHANGE_DLC_U8TURNLIGHTTWICE_PRE}};
const SignalCondition DLC_u8TurnLightTwice_Pre_SignalConditions[0] = {};
const SignalCondition EspAutoHoldActvSts_SignalConditions[0] = {};
const SignalCondition EspAutoHoldActvSts_Pre_SignalConditions[0] = {};
const SignalCondition PLB_u8LBSts_SignalConditions[0] = {};
const SignalCondition PLB_u8LBSts_Pre_SignalConditions[0] = {};
const SignalCondition PRM_u8PowerSts_SignalConditions[1] = {{PRM_u8PowerSts_Pre_SIGNALNUM, CHANGE, &LGL_PRM_ON2NOTON, PRM_U8POWERSTS_CHANGE_PRM_U8POWERSTS_PRE}};
const SignalCondition PRM_u8PowerSts_Pre_SignalConditions[0] = {};
const SignalCondition VcuGearPosn_SignalConditions[1] = {{DLC_u8TurnLightTwice_SIGNALNUM, NEQ, &LGL_Normal_OFF, VCUGEARPOSN_NEQ_DLC_U8TURNLIGHTTWICE}};
const SignalCondition VcuGearPosn_Pre_SignalConditions[0] = {};


static const BitSignalConditionInfo BitConditionInfoArray[2] = {
{PPL_boolPosnLampSts_SIGNALNUM, 3, &PPL_boolPosnLampSts_Conditions} ,
{PPL_boolPosnLampSts_Pre_SIGNALNUM, 0, &PPL_boolPosnLampSts_Pre_Conditions} 
};

static const doubleSignalConditionInfo doubleConditionInfoArray[0] = {
 
};

static const EEPROM_U8SignalConditionInfo EEPROM_U8ConditionInfoArray[2] = {
{EEP_LOGO_ENABLE_FLAG_SIGNALNUM, 3, &EEP_LOGO_ENABLE_FLAG_Conditions} ,
{EEP_LOGO_ENABLE_FLAG_Pre_SIGNALNUM, 0, &EEP_LOGO_ENABLE_FLAG_Pre_Conditions} 
};

static const int16SignalConditionInfo int16ConditionInfoArray[0] = {
 
};

static const int32SignalConditionInfo int32ConditionInfoArray[0] = {
 
};

static const int64SignalConditionInfo int64ConditionInfoArray[0] = {
 
};

static const int8SignalConditionInfo int8ConditionInfoArray[0] = {
 
};

static const singleSignalConditionInfo singleConditionInfoArray[0] = {
 
};

static const uint16SignalConditionInfo uint16ConditionInfoArray[0] = {
 
};

static const uint32SignalConditionInfo uint32ConditionInfoArray[0] = {
 
};

static const uint64SignalConditionInfo uint64ConditionInfoArray[0] = {
 
};

static const uint8SignalConditionInfo uint8ConditionInfoArray[14] = {
{BdcSeedsignal_SIGNALNUM, 3, &BdcSeedsignal_Conditions} ,
{BdcSeedsignal_Pre_SIGNALNUM, 0, &BdcSeedsignal_Pre_Conditions} ,
{BdcWlcmsignal_SIGNALNUM, 2, &BdcWlcmsignal_Conditions} ,
{BdcWlcmsignal_Pre_SIGNALNUM, 0, &BdcWlcmsignal_Pre_Conditions} ,
{DLC_u8TurnLightTwice_SIGNALNUM, 0, &DLC_u8TurnLightTwice_Conditions} ,
{DLC_u8TurnLightTwice_Pre_SIGNALNUM, 0, &DLC_u8TurnLightTwice_Pre_Conditions} ,
{EspAutoHoldActvSts_SIGNALNUM, 3, &EspAutoHoldActvSts_Conditions} ,
{EspAutoHoldActvSts_Pre_SIGNALNUM, 0, &EspAutoHoldActvSts_Pre_Conditions} ,
{PLB_u8LBSts_SIGNALNUM, 3, &PLB_u8LBSts_Conditions} ,
{PLB_u8LBSts_Pre_SIGNALNUM, 0, &PLB_u8LBSts_Pre_Conditions} ,
{PRM_u8PowerSts_SIGNALNUM, 2, &PRM_u8PowerSts_Conditions} ,
{PRM_u8PowerSts_Pre_SIGNALNUM, 1, &PRM_u8PowerSts_Pre_Conditions} ,
{VcuGearPosn_SIGNALNUM, 4, &VcuGearPosn_Conditions} ,
{VcuGearPosn_Pre_SIGNALNUM, 1, &VcuGearPosn_Pre_Conditions} 
};

static const SignalConditionInfo BitSignalConditionInfoArray[2] = {
{PPL_boolPosnLampSts_SIGNALNUM, 0, &PPL_boolPosnLampSts_Conditions} ,
{PPL_boolPosnLampSts_Pre_SIGNALNUM, 0, &PPL_boolPosnLampSts_Pre_Conditions} 
};

static const SignalConditionInfo doubleSignalConditionInfoArray[0] = {
 
};

static const SignalConditionInfo EEPROM_U8SignalConditionInfoArray[2] = {
{EEP_LOGO_ENABLE_FLAG_SIGNALNUM, 1, &EEP_LOGO_ENABLE_FLAG_Conditions} ,
{EEP_LOGO_ENABLE_FLAG_Pre_SIGNALNUM, 0, &EEP_LOGO_ENABLE_FLAG_Pre_Conditions} 
};

static const SignalConditionInfo int16SignalConditionInfoArray[0] = {
 
};

static const SignalConditionInfo int32SignalConditionInfoArray[0] = {
 
};

static const SignalConditionInfo int64SignalConditionInfoArray[0] = {
 
};

static const SignalConditionInfo int8SignalConditionInfoArray[0] = {
 
};

static const SignalConditionInfo singleSignalConditionInfoArray[0] = {
 
};

static const SignalConditionInfo uint16SignalConditionInfoArray[0] = {
 
};

static const SignalConditionInfo uint32SignalConditionInfoArray[0] = {
 
};

static const SignalConditionInfo uint64SignalConditionInfoArray[0] = {
 
};

static const SignalConditionInfo uint8SignalConditionInfoArray[14] = {
{BdcSeedsignal_SIGNALNUM, 1, &BdcSeedsignal_Conditions} ,
{BdcSeedsignal_Pre_SIGNALNUM, 0, &BdcSeedsignal_Pre_Conditions} ,
{BdcWlcmsignal_SIGNALNUM, 0, &BdcWlcmsignal_Conditions} ,
{BdcWlcmsignal_Pre_SIGNALNUM, 0, &BdcWlcmsignal_Pre_Conditions} ,
{DLC_u8TurnLightTwice_SIGNALNUM, 1, &DLC_u8TurnLightTwice_Conditions} ,
{DLC_u8TurnLightTwice_Pre_SIGNALNUM, 0, &DLC_u8TurnLightTwice_Pre_Conditions} ,
{EspAutoHoldActvSts_SIGNALNUM, 0, &EspAutoHoldActvSts_Conditions} ,
{EspAutoHoldActvSts_Pre_SIGNALNUM, 0, &EspAutoHoldActvSts_Pre_Conditions} ,
{PLB_u8LBSts_SIGNALNUM, 0, &PLB_u8LBSts_Conditions} ,
{PLB_u8LBSts_Pre_SIGNALNUM, 0, &PLB_u8LBSts_Pre_Conditions} ,
{PRM_u8PowerSts_SIGNALNUM, 1, &PRM_u8PowerSts_Conditions} ,
{PRM_u8PowerSts_Pre_SIGNALNUM, 0, &PRM_u8PowerSts_Pre_Conditions} ,
{VcuGearPosn_SIGNALNUM, 1, &VcuGearPosn_Conditions} ,
{VcuGearPosn_Pre_SIGNALNUM, 0, &VcuGearPosn_Pre_Conditions} 
};

const TimeOutCondition TimeOutActionArray[4] = {
 {1, EQ, &LGL_SEE_OFF}, 
 {1, EQ, &LGL_EEP_OFF}, 
 {1, EQ, &LGL_PRM_OFF}, 
 {1, EQ, &LGL_DLC_OFF}, 
};

