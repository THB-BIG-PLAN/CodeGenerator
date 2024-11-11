#include <Type_define.h>
#include <stdlib.h>
#include <string.h>
#include <sgn/signal_api.h>
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


#define LGL_ON() { Set_Bit_BDC_FrntLogLampCmd(ON); Set_uint8_FrntLogLamp(ON) ;}
#define LGL_OFF() { Set_Bit_BDC_FrntLogLampCmd(OFF); Set_uint8_FrntLogLamp(OFF) ;}
#define addTimer(Flag,Time) { Add_Timer(Time, &EVT_flag->TimeOutFlag[Flag]); EVT_flag->LGL_TimeOutFlagNum++ ;}
#define delTime(Flag) { EVT_flag->LGL_TimeOutFlagNum--; EVT_flag->TimeOutFlag[Flag] = false ;}


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
void LGL_Normal_OFF1();
void LGL_Normal_OFF2();


void LGL_initialize() {
    Condition_Init();
}

void LGL_SEE_ON() 
{
    if (EVT_Flag->ConditionFlag[BDCSEEDSIGNAL_NEQ_0]) 
    {
        LGL_ON();
    }
}

void LGL_WEL_ON() 
{
    if (EVT_Flag->ConditionFlag[BDCWLCMSIGNAL_NEQ_0]) 
    {
        LGL_ON();
    }
}

void LGL_VCU_POL_ON() 
{
    if (EVT_Flag->ConditionFlag[VCUGEARPOSN_EQ_1] && 
        EVT_Flag->ConditionFlag[PPL_BOOLPOSNLAMPSTS_EQ_1]) 
    {
        LGL_ON();
    }
}

void LGL_VCU_LBL_ON() 
{
    if (EVT_Flag->ConditionFlag[VCUGEARPOSN_EQ_1] && 
        EVT_Flag->ConditionFlag[PLB_U8LBSTS_EQ_1]) 
    {
        LGL_ON();
    }
}

void LGL_ESP_POL_ON() 
{
    if (EVT_Flag->ConditionFlag[ESPAUTOHOLDACTVSTS_EQ_1] && 
        EVT_Flag->ConditionFlag[PPL_BOOLPOSNLAMPSTS_EQ_1]) 
    {
        LGL_ON();
    }
}

void LGL_ESP_LBL_ON() 
{
    if (EVT_Flag->ConditionFlag[ESPAUTOHOLDACTVSTS_EQ_1] && 
        EVT_Flag->ConditionFlag[PLB_U8LBSTS_EQ_1]) 
    {
        LGL_ON();
    }
}

void LGL_PRM_EEP_ON() 
{
    if (EVT_Flag->ConditionFlag[PRM_U8POWERSTS_EQ_2] && 
        EVT_Flag->ConditionFlag[EEP_LOGO_ENABLE_FLAG_EQ_1]) 
    {
        LGL_ON();
    }
}

void LGL_DLC_TUL_ON() 
{
    if (EVT_Flag->ConditionFlag[DLC_U8TURNLIGHTTWICE_CHANGE_0XFF]) 
    {
        LGL_ON();
        addTimer(LGL_DLC_1500ms_TimeOut,Counter1500ms);
    }
}

void LGL_PRM_ON2NOTON() 
{
    if (EVT_Flag->ConditionFlag[EEP_LOGO_ENABLE_FLAG_EQ_1]) 
    {
        addTimer(LGL_PRM_350ms_TimeOut,Counter350ms);
    }
}

void LGL_EEP_ENABLE2DISABLE() 
{
    if (EVT_Flag->ConditionFlag[PRM_U8POWERSTS_EQ_2]) 
    {
        addTimer(LGL_EEP_350ms_TimeOut,Counter350ms);
    }
}

void LGL_SEE_REQ2NO() 
{
    if (EVT_Flag->ConditionFlag[BDCSEEDSIGNAL_CHANGETO_0]) 
    {
        addTimer(LGL_SEE_350ms_TimeOut,Counter350ms);
    }
}

void LGL_DLC_TIMEOUT() 
{
    delTime(LGL_DLC_1500ms_TimeOut);
}

void LGL_PRM_TIMEOUT() 
{
    delTime(LGL_PRM_350ms_TimeOut);
}

void LGL_EEP_TIMEOUT() 
{
    delTime(LGL_EEP_350ms_TimeOut);
}

void LGL_SEE_TIMEOUT() 
{
    delTime(LGL_SEE_350ms_TimeOut);
}

void LGL_Normal_OFF1() 
{
    if (EVT_Flag->ConditionFlag[BDCSEEDSIGNAL_EQ_0] && 
        EVT_Flag->ConditionFlag[BDCWLCMSIGNAL_EQ_0] && 
        EVT_Flag->ConditionFlag[VCUGEARPOSN_EQ_0] && 
        EVT_Flag->ConditionFlag[PPL_BOOLPOSNLAMPSTS_EQ_0] && 
        EVT_Flag->ConditionFlag[PLB_U8LBSTS_EQ_1] && 
        EVT_Flag->ConditionFlag[ESPAUTOHOLDACTVSTS_EQ_0] && 
        EVT_Flag->ConditionFlag[PRM_U8POWERSTS_CHANGETO_0] && 
        EVT_Flag->ConditionFlag[LGL_TIMEFLAGNUM_EQ_0]) 
    {
        LGL_OFF();
    }
}

void LGL_Normal_OFF2() 
{
    if (EVT_Flag->ConditionFlag[BDCSEEDSIGNAL_EQ_0] && 
        EVT_Flag->ConditionFlag[BDCWLCMSIGNAL_EQ_0] && 
        EVT_Flag->ConditionFlag[VCUGEARPOSN_EQ_0] && 
        EVT_Flag->ConditionFlag[PPL_BOOLPOSNLAMPSTS_EQ_0] && 
        EVT_Flag->ConditionFlag[PLB_U8LBSTS_EQ_1] && 
        EVT_Flag->ConditionFlag[ESPAUTOHOLDACTVSTS_EQ_0] && 
        EVT_Flag->ConditionFlag[EEP_LOGO_ENABLE_FLAG_EQ_0] && 
        EVT_Flag->ConditionFlag[LGL_TIMEFLAGNUM_EQ_0]) 
    {
        LGL_OFF();
    }
}

