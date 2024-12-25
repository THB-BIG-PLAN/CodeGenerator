#pragma once
#ifndef TIMER_API
#include "Type_define.h"
void delTimer(uint8 TimeFlagIndex);
void addTimer(uint8 TimeFlagIndex, uint16 Time);
void Init_Timer();
void del_point_by_TimeOutFlag(const bool* flag);
#endif
