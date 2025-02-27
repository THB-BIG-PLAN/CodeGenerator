
#include <Type_define.h>
#include <stdlib.h>
#include <string.h>
#include "EVT/Timer/Timer.api.h"
#include "EVT/Event/EVT.h"
#include "EVT/Logic/Logic.h"
#include "EVT/Condition/Condition.h"


#define WEL_NO_REQ 0x0
#define SEE_NO_REQ 0x0
#define VCU_GEAR_P 0x1
#define ESP_AUTO_HOLD 0x1
#define POL_STS_ON 0x1
#define POL_STS_OFF 0x0
#define LBL_STS_ON 0x1
#define LBL_STS_OFF 0x0
#define PRM_PWR_ON 0x2
#define EEP_LGL_ENABLE 0x1
#define EEP_LGL_DISABLE 0x0
#define ON 0x1
#define OFF 0x0
#define Counter1500ms 150U
#define Counter350ms 35U
#define PRM_PWR_OFF 0x0


void LGL_SEE_ON();
void LGL_WEL_ON();
void LGL_VCU_POL_ON();
void LGL_VCU_LBL_ON();
void LGL_ESP_POL_ON();
void LGL_ESP_LBL_ON();
void LGL_PRM_EEP_ON();
void LGL_DLC_TUL_ON();
void LGL_PRM_ON2NOTON();
void LGL_EEP_ENABLE2DISABLE();
void LGL_SEE_REQ2NO();
void LGL_DLC_TIMEOUT();
void LGL_PRM_TIMEOUT();
void LGL_EEP_TIMEOUT();
void LGL_SEE_TIMEOUT();
void LGL_Normal_OFF();
void LGL_Normal_OFF1();
void LGL_Normal_OFF2();
void TestFun();
void TestAction();


void LGL_SEE_ON()
{
    LGL_Set(ON)
}

void LGL_WEL_ON()
{
    LGL_Set(ON)
}

void LGL_VCU_POL_ON()
{
    if (P_SignalsAndConditions->ConditionFlag[PPL_BOOLPOSNLAMPSTS_EQ_1])
    {
        LGL_Set(ON)
    }
}

void LGL_VCU_LBL_ON()
{
    if (P_SignalsAndConditions->ConditionFlag[PLB_U8LBSTS_EQ_1])
    {
        LGL_Set(ON)
    }
}

void LGL_ESP_POL_ON()
{
    if (P_SignalsAndConditions->ConditionFlag[PPL_BOOLPOSNLAMPSTS_EQ_1])
    {
        LGL_Set(ON)
    }
}

void LGL_ESP_LBL_ON()
{
    if (P_SignalsAndConditions->ConditionFlag[PLB_U8LBSTS_EQ_1])
    {
        LGL_Set(ON)
    }
}

void LGL_PRM_EEP_ON()
{
    if (P_SignalsAndConditions->ConditionFlag[EEP_LOGO_ENABLE_FLAG_EQ_1])
    {
        LGL_Set(ON)
    }
}

void LGL_DLC_TUL_ON()
{
    LGL_Set(ON)
    addTimer(LGL_DLC_1500ms_TimeOut, Counter1500ms)
}

void LGL_PRM_ON2NOTON()
{
    if (P_SignalsAndConditions->ConditionFlag[PRM_U8POWERSTS_PRE_EQ_2])
    {
        addTimer(LGL_PRM_350ms_TimeOut, Counter350ms)
    }
}

void LGL_EEP_ENABLE2DISABLE()
{
    if (P_SignalsAndConditions->ConditionFlag[EEP_LOGO_ENABLE_FLAG_CHANGE_EEP_LOGO_ENABLE_FLAG_PRE] && 
        P_SignalsAndConditions->ConditionFlag[EEP_LOGO_ENABLE_FLAG_EQ_0])
    {
        addTimer(LGL_EEP_350ms_TimeOut, Counter350ms)
    }
}

void LGL_SEE_REQ2NO()
{
    if (P_SignalsAndConditions->ConditionFlag[BDCSEEDSIGNAL_EQ_0])
    {
        addTimer(LGL_SEE_350ms_TimeOut, Counter350ms)
    }
}

void LGL_DLC_TIMEOUT()
{
    delTimer(LGL_DLC_1500ms_TimeOut)
}

void LGL_PRM_TIMEOUT()
{
    delTimer(LGL_PRM_350ms_TimeOut)
}

void LGL_EEP_TIMEOUT()
{
    delTimer(LGL_EEP_350ms_TimeOut)
}

void LGL_SEE_TIMEOUT()
{
    delTimer(LGL_SEE_350ms_TimeOut)
}

void LGL_Normal_OFF()
{
    LGL_Normal_OFF1()
    LGL_Normal_OFF2()
}

void LGL_Normal_OFF1()
{
    if (P_SignalsAndConditions->ConditionFlag[BDCWLCMSIGNAL_EQ_0] && 
        P_SignalsAndConditions->ConditionFlag[VCUGEARPOSN_EQ_0] && 
        P_SignalsAndConditions->ConditionFlag[PPL_BOOLPOSNLAMPSTS_EQ_0] && 
        P_SignalsAndConditions->ConditionFlag[PLB_U8LBSTS_EQ_0] && 
        P_SignalsAndConditions->ConditionFlag[ESPAUTOHOLDACTVSTS_EQ_0] && 
        P_SignalsAndConditions->ConditionFlag[PRM_U8POWERSTS_EQ_0] && 
        P_SignalsAndConditions->ConditionFlag[TIMEFLAGNUM_EQ_0])
    {
        LGL_Set(OFF)
    }
}

void LGL_Normal_OFF2()
{
    if (P_SignalsAndConditions->ConditionFlag[BDCWLCMSIGNAL_EQ_0] && 
        P_SignalsAndConditions->ConditionFlag[VCUGEARPOSN_EQ_0] && 
        P_SignalsAndConditions->ConditionFlag[PPL_BOOLPOSNLAMPSTS_EQ_0] && 
        P_SignalsAndConditions->ConditionFlag[PLB_U8LBSTS_EQ_0] && 
        P_SignalsAndConditions->ConditionFlag[ESPAUTOHOLDACTVSTS_EQ_0] && 
        P_SignalsAndConditions->ConditionFlag[EEP_LOGO_ENABLE_FLAG_EQ_0] && 
        P_SignalsAndConditions->ConditionFlag[TIMEFLAGNUM_EQ_0])
    {
        LGL_Set(OFF)
    }
}

void TestFun()
{
    TestAction()
}

void TestAction()
{
    SetNum(P_SignalsAndConditions->Signal_uint8[PRM_u8PowerSts_SIGNALNUM], 2)
    SetNum(P_SignalsAndConditions->Signal_uint8[PLB_u8LBSts_SIGNALNUM], 3)
    SetNum(P_SignalsAndConditions->Signal_uint8[BdcSeedsignal_SIGNALNUM], 3)
}

