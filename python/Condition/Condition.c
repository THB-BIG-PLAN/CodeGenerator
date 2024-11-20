#include "EVT/Condition/Condition.h"

const Condition BdcSeedsignal_Condition[3] = {{0,NEQ,&LGL_SEE_ON,BDCSEEDSIGNAL_NEQ_0},{0,CHANGETO,&LGL_SEE_REQ2NO,BDCSEEDSIGNAL_CHANGETO_0},{0,EQ,&LGL_Normal_OFF,BDCSEEDSIGNAL_EQ_0}};

const Condition BdcWlcmsignal_Condition[2] = {{0,NEQ,&LGL_WEL_ON,BDCWLCMSIGNAL_NEQ_0},{0,EQ,&LGL_Normal_OFF,BDCWLCMSIGNAL_EQ_0}};

const Condition DLC_u8TurnLightTwice_Condition[1] = {{0xff,CHANGE,&LGL_DLC_TUL_ON,DLC_U8TURNLIGHTTWICE_CHANGE_0XFF}};

const Condition EEP_LOGO_ENABLE_FLAG_Condition[3] = {{1,EQ,&LGL_PRM_EEP_ON,EEP_LOGO_ENABLE_FLAG_EQ_1},{0,CHANGETO,&LGL_EEP_ENABLE2DISABLE,EEP_LOGO_ENABLE_FLAG_CHANGETO_0},{0,EQ,&LGL_Normal_OFF,EEP_LOGO_ENABLE_FLAG_EQ_0}};

const Condition EspAutoHoldActvSts_Condition[3] = {{0,EQ,&LGL_Normal_OFF,ESPAUTOHOLDACTVSTS_EQ_0},{1,EQ,&LGL_ESP_POL_ON,ESPAUTOHOLDACTVSTS_EQ_1},{1,EQ,&LGL_ESP_LBL_ON,ESPAUTOHOLDACTVSTS_EQ_1}};

const Condition PLB_u8LBSts_Condition[3] = {{0,EQ,&LGL_Normal_OFF,PLB_U8LBSTS_EQ_0},{1,EQ,&LGL_VCU_LBL_ON,PLB_U8LBSTS_EQ_1},{1,EQ,&LGL_ESP_LBL_ON,PLB_U8LBSTS_EQ_1}};

const Condition PPL_boolPosnLampSts_Condition[3] = {{0,EQ,&LGL_Normal_OFF,PPL_BOOLPOSNLAMPSTS_EQ_0},{1,EQ,&LGL_ESP_POL_ON,PPL_BOOLPOSNLAMPSTS_EQ_1},{1,EQ,&LGL_VCU_POL_ON,PPL_BOOLPOSNLAMPSTS_EQ_1}};

const Condition PRM_u8PowerSts_Condition[4] = {{2,EQ,&LGL_PRM_EEP_ON,PRM_U8POWERSTS_EQ_2},{1,CHANGETO,&LGL_PRM_ON2NOTON,PRM_U8POWERSTS_CHANGETO_1},{0,CHANGETO,&LGL_PRM_ON2NOTON,PRM_U8POWERSTS_CHANGETO_0},{0,EQ,&LGL_Normal_OFF,PRM_U8POWERSTS_EQ_0}};

const Condition VcuGearPosn_Condition[3] = {{0,EQ,&LGL_Normal_OFF,VCUGEARPOSN_EQ_0},{1,EQ,&LGL_VCU_LBL_ON,VCUGEARPOSN_EQ_1},{1,EQ,&LGL_VCU_POL_ON,VCUGEARPOSN_EQ_1}};

static const SignalCondition SignalConditionArray[SIGNAL_NUM] = {
{BdcSeedsignal_SIGNALNUM,3,&BdcSeedsignal_Condition},
{BdcWlcmsignal_SIGNALNUM,2,&BdcWlcmsignal_Condition},
{DLC_u8TurnLightTwice_SIGNALNUM,1,&DLC_u8TurnLightTwice_Condition},
{EEP_LOGO_ENABLE_FLAG_SIGNALNUM,3,&EEP_LOGO_ENABLE_FLAG_Condition},
{EspAutoHoldActvSts_SIGNALNUM,3,&EspAutoHoldActvSts_Condition},
{PLB_u8LBSts_SIGNALNUM,3,&PLB_u8LBSts_Condition},
{PPL_boolPosnLampSts_SIGNALNUM,3,&PPL_boolPosnLampSts_Condition},
{PRM_u8PowerSts_SIGNALNUM,4,&PRM_u8PowerSts_Condition},
{VcuGearPosn_SIGNALNUM,3,&VcuGearPosn_Condition}};

static const Condition TimeOutActionArray[TIMEOUT_NUM] = {
{1, EQ, &LGL_SEE_OFF},
{1, EQ, &LGL_EEP_OFF},
{1, EQ, &LGL_PRM_OFF},
{1, EQ, &LGL_DLC_OFF}};


EVT_FLAG* EVT_flag;
