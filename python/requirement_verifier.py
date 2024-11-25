
# -*- coding: gbk -*-
import pandas as pd
from enum import Enum
import warnings
import openpyxl
import re
warnings.simplefilter(action='ignore', category=UserWarning)
from openpyxl import Workbook
ResultList = []
ErrorList = []
Result = pd.DataFrame(columns=['BdcSeedsignal', 'BdcWlcmsignal', 'DLC_u8TurnLightTwice', 'EEP_LOGO_ENABLE_FLAG', 'EspAutoHoldActvSts', 'PLB_u8LBSts', 'PPL_boolPosnLampSts', 'PRM_u8PowerSts', 'VcuGearPosn', 'TIMEFLAGNUM', 'Action'])
class Action0(Enum):
    LGL_ON = 0
    LGL_OFF = 1

class State:
    def __init__(self, BdcSeedsignal, BdcWlcmsignal, DLC_u8TurnLightTwice, 
                EEP_LOGO_ENABLE_FLAG, EspAutoHoldActvSts, PLB_u8LBSts, 
                PPL_boolPosnLampSts, PRM_u8PowerSts, VcuGearPosn):
        self.current_state = {'BdcSeedsignal': BdcSeedsignal, 'BdcWlcmsignal': BdcWlcmsignal, 'DLC_u8TurnLightTwice': DLC_u8TurnLightTwice, 
                'EEP_LOGO_ENABLE_FLAG': EEP_LOGO_ENABLE_FLAG, 'EspAutoHoldActvSts': EspAutoHoldActvSts, 'PLB_u8LBSts': PLB_u8LBSts, 
                'PPL_boolPosnLampSts': PPL_boolPosnLampSts, 'PRM_u8PowerSts': PRM_u8PowerSts, 'VcuGearPosn': VcuGearPosn, 'TIMEFLAGNUM': 0}
        self.previous_state = {k: 0 for k in self.current_state.keys()}
        self.BDCSEEDSIGNAL_NEQ_0 = 0 
        self.BDCSEEDSIGNAL_CHANGETO_0 = 0 
        self.BDCSEEDSIGNAL_EQ_0 = 0 
        self.BDCWLCMSIGNAL_NEQ_0 = 0 
        self.BDCWLCMSIGNAL_EQ_0 = 0 
        self.DLC_U8TURNLIGHTTWICE_CHANGE_0XFF = 0 
        self.EEP_LOGO_ENABLE_FLAG_EQ_1 = 0 
        self.EEP_LOGO_ENABLE_FLAG_CHANGETO_0 = 0 
        self.EEP_LOGO_ENABLE_FLAG_EQ_0 = 0 
        self.ESPAUTOHOLDACTVSTS_EQ_0 = 0 
        self.ESPAUTOHOLDACTVSTS_EQ_1 = 0 
        self.PLB_U8LBSTS_EQ_0 = 0 
        self.PLB_U8LBSTS_EQ_1 = 0 
        self.PPL_BOOLPOSNLAMPSTS_EQ_0 = 0 
        self.PPL_BOOLPOSNLAMPSTS_EQ_1 = 0 
        self.PRM_U8POWERSTS_EQ_2 = 0 
        self.PRM_U8POWERSTS_CHANGETO_1 = 0 
        self.PRM_U8POWERSTS_CHANGETO_0 = 0 
        self.PRM_U8POWERSTS_EQ_0 = 0 
        self.VCUGEARPOSN_EQ_0 = 0 
        self.VCUGEARPOSN_EQ_1 = 0 
        self.TIMEFLAGNUM_EQ_0 = 0 
        self.VCUGEARPOSN_NEQ_DLC_U8TURNLIGHTTWICE_SIGNALNUM = 0 

        if self.current_state['BdcSeedsignal'] != 0:
            self.BDCSEEDSIGNAL_NEQ_0 = 1
        if self.current_state['BdcSeedsignal'] != self.previous_state['BdcSeedsignal'] and self.current_state['BdcSeedsignal'] == 0:
            self.BDCSEEDSIGNAL_CHANGETO_0 = 1
        if self.current_state['BdcSeedsignal'] == 0:
            self.BDCSEEDSIGNAL_EQ_0 = 1
        if self.current_state['BdcWlcmsignal'] != 0:
            self.BDCWLCMSIGNAL_NEQ_0 = 1
        if self.current_state['BdcWlcmsignal'] == 0:
            self.BDCWLCMSIGNAL_EQ_0 = 1
        if self.current_state['DLC_u8TurnLightTwice'] != self.previous_state['DLC_u8TurnLightTwice']:
            self.DLC_U8TURNLIGHTTWICE_CHANGE_0XFF = 1
        if self.current_state['EEP_LOGO_ENABLE_FLAG'] == 1:
            self.EEP_LOGO_ENABLE_FLAG_EQ_1 = 1
        if self.current_state['EEP_LOGO_ENABLE_FLAG'] != self.previous_state['EEP_LOGO_ENABLE_FLAG'] and self.current_state['EEP_LOGO_ENABLE_FLAG'] == 0:
            self.EEP_LOGO_ENABLE_FLAG_CHANGETO_0 = 1
        if self.current_state['EEP_LOGO_ENABLE_FLAG'] == 0:
            self.EEP_LOGO_ENABLE_FLAG_EQ_0 = 1
        if self.current_state['EspAutoHoldActvSts'] == 0:
            self.ESPAUTOHOLDACTVSTS_EQ_0 = 1
        if self.current_state['EspAutoHoldActvSts'] == 1:
            self.ESPAUTOHOLDACTVSTS_EQ_1 = 1
        if self.current_state['EspAutoHoldActvSts'] == 1:
            self.ESPAUTOHOLDACTVSTS_EQ_1 = 1
        if self.current_state['PLB_u8LBSts'] == 0:
            self.PLB_U8LBSTS_EQ_0 = 1
        if self.current_state['PLB_u8LBSts'] == 1:
            self.PLB_U8LBSTS_EQ_1 = 1
        if self.current_state['PLB_u8LBSts'] == 1:
            self.PLB_U8LBSTS_EQ_1 = 1
        if self.current_state['PPL_boolPosnLampSts'] == 0:
            self.PPL_BOOLPOSNLAMPSTS_EQ_0 = 1
        if self.current_state['PPL_boolPosnLampSts'] == 1:
            self.PPL_BOOLPOSNLAMPSTS_EQ_1 = 1
        if self.current_state['PPL_boolPosnLampSts'] == 1:
            self.PPL_BOOLPOSNLAMPSTS_EQ_1 = 1
        if self.current_state['PRM_u8PowerSts'] == 2:
            self.PRM_U8POWERSTS_EQ_2 = 1
        if self.current_state['PRM_u8PowerSts'] != self.previous_state['PRM_u8PowerSts'] and self.current_state['PRM_u8PowerSts'] == 1:
            self.PRM_U8POWERSTS_CHANGETO_1 = 1
        if self.current_state['PRM_u8PowerSts'] != self.previous_state['PRM_u8PowerSts'] and self.current_state['PRM_u8PowerSts'] == 0:
            self.PRM_U8POWERSTS_CHANGETO_0 = 1
        if self.current_state['PRM_u8PowerSts'] == 0:
            self.PRM_U8POWERSTS_EQ_0 = 1
        if self.current_state['VcuGearPosn'] == 0:
            self.VCUGEARPOSN_EQ_0 = 1
        if self.current_state['VcuGearPosn'] == 1:
            self.VCUGEARPOSN_EQ_1 = 1
        if self.current_state['VcuGearPosn'] == 1:
            self.VCUGEARPOSN_EQ_1 = 1
        if self.current_state['VcuGearPosn'] != self.current_state['DLC_u8TurnLightTwice']:
            self.VCUGEARPOSN_NEQ_DLC_U8TURNLIGHTTWICE_SIGNALNUM = 1

        if((self.DLC_U8TURNLIGHTTWICE_CHANGE_0XFF == 1)) and ((self.DLC_U8TURNLIGHTTWICE_CHANGE_0XFF == 1)):
             self.current_state["TIMEFLAGNUM"] += 1
        if((self.PRM_U8POWERSTS_CHANGETO_1 == 1) or (self.PRM_U8POWERSTS_CHANGETO_0 == 1)) and ((self.EEP_LOGO_ENABLE_FLAG_EQ_1 == 1)):
             self.current_state["TIMEFLAGNUM"] += 1
        if((self.EEP_LOGO_ENABLE_FLAG_CHANGETO_0 == 1)) and ((self.PRM_U8POWERSTS_EQ_2 == 1)):
             self.current_state["TIMEFLAGNUM"] += 1
        if((self.BDCSEEDSIGNAL_CHANGETO_0 == 1)) and ((self.BDCSEEDSIGNAL_CHANGETO_0 == 1)):
             self.current_state["TIMEFLAGNUM"] += 1
        if self.current_state["TIMEFLAGNUM"] == 0:
            self.TIMEFLAGNUM_EQ_0 = 1 


    def update_state(self,BdcSeedsignal, BdcWlcmsignal, DLC_u8TurnLightTwice, 
                EEP_LOGO_ENABLE_FLAG, EspAutoHoldActvSts, PLB_u8LBSts, 
                PPL_boolPosnLampSts, PRM_u8PowerSts, VcuGearPosn):
        self.previous_state = self.current_state.copy()
        self.current_state = {'BdcSeedsignal': BdcSeedsignal, 'BdcWlcmsignal': BdcWlcmsignal, 'DLC_u8TurnLightTwice': DLC_u8TurnLightTwice, 
                'EEP_LOGO_ENABLE_FLAG': EEP_LOGO_ENABLE_FLAG, 'EspAutoHoldActvSts': EspAutoHoldActvSts, 'PLB_u8LBSts': PLB_u8LBSts, 
                'PPL_boolPosnLampSts': PPL_boolPosnLampSts, 'PRM_u8PowerSts': PRM_u8PowerSts, 'VcuGearPosn': VcuGearPosn, 'TIMEFLAGNUM': 0}

        self.BDCSEEDSIGNAL_NEQ_0 = 0 
        self.BDCSEEDSIGNAL_CHANGETO_0 = 0 
        self.BDCSEEDSIGNAL_EQ_0 = 0 
        self.BDCWLCMSIGNAL_NEQ_0 = 0 
        self.BDCWLCMSIGNAL_EQ_0 = 0 
        self.DLC_U8TURNLIGHTTWICE_CHANGE_0XFF = 0 
        self.EEP_LOGO_ENABLE_FLAG_EQ_1 = 0 
        self.EEP_LOGO_ENABLE_FLAG_CHANGETO_0 = 0 
        self.EEP_LOGO_ENABLE_FLAG_EQ_0 = 0 
        self.ESPAUTOHOLDACTVSTS_EQ_0 = 0 
        self.ESPAUTOHOLDACTVSTS_EQ_1 = 0 
        self.PLB_U8LBSTS_EQ_0 = 0 
        self.PLB_U8LBSTS_EQ_1 = 0 
        self.PPL_BOOLPOSNLAMPSTS_EQ_0 = 0 
        self.PPL_BOOLPOSNLAMPSTS_EQ_1 = 0 
        self.PRM_U8POWERSTS_EQ_2 = 0 
        self.PRM_U8POWERSTS_CHANGETO_1 = 0 
        self.PRM_U8POWERSTS_CHANGETO_0 = 0 
        self.PRM_U8POWERSTS_EQ_0 = 0 
        self.VCUGEARPOSN_EQ_0 = 0 
        self.VCUGEARPOSN_EQ_1 = 0 
        self.TIMEFLAGNUM_EQ_0 = 0 
        self.VCUGEARPOSN_NEQ_DLC_U8TURNLIGHTTWICE_SIGNALNUM = 0 


        if self.current_state['BdcSeedsignal'] != 0:
            self.BDCSEEDSIGNAL_NEQ_0 = 1
        if self.current_state['BdcSeedsignal'] != self.previous_state['BdcSeedsignal'] and self.current_state['BdcSeedsignal'] == 0:
            self.BDCSEEDSIGNAL_CHANGETO_0 = 1
        if self.current_state['BdcSeedsignal'] == 0:
            self.BDCSEEDSIGNAL_EQ_0 = 1
        if self.current_state['BdcWlcmsignal'] != 0:
            self.BDCWLCMSIGNAL_NEQ_0 = 1
        if self.current_state['BdcWlcmsignal'] == 0:
            self.BDCWLCMSIGNAL_EQ_0 = 1
        if self.current_state['DLC_u8TurnLightTwice'] != self.previous_state['DLC_u8TurnLightTwice']:
            self.DLC_U8TURNLIGHTTWICE_CHANGE_0XFF = 1
        if self.current_state['EEP_LOGO_ENABLE_FLAG'] == 1:
            self.EEP_LOGO_ENABLE_FLAG_EQ_1 = 1
        if self.current_state['EEP_LOGO_ENABLE_FLAG'] != self.previous_state['EEP_LOGO_ENABLE_FLAG'] and self.current_state['EEP_LOGO_ENABLE_FLAG'] == 0:
            self.EEP_LOGO_ENABLE_FLAG_CHANGETO_0 = 1
        if self.current_state['EEP_LOGO_ENABLE_FLAG'] == 0:
            self.EEP_LOGO_ENABLE_FLAG_EQ_0 = 1
        if self.current_state['EspAutoHoldActvSts'] == 0:
            self.ESPAUTOHOLDACTVSTS_EQ_0 = 1
        if self.current_state['EspAutoHoldActvSts'] == 1:
            self.ESPAUTOHOLDACTVSTS_EQ_1 = 1
        if self.current_state['EspAutoHoldActvSts'] == 1:
            self.ESPAUTOHOLDACTVSTS_EQ_1 = 1
        if self.current_state['PLB_u8LBSts'] == 0:
            self.PLB_U8LBSTS_EQ_0 = 1
        if self.current_state['PLB_u8LBSts'] == 1:
            self.PLB_U8LBSTS_EQ_1 = 1
        if self.current_state['PLB_u8LBSts'] == 1:
            self.PLB_U8LBSTS_EQ_1 = 1
        if self.current_state['PPL_boolPosnLampSts'] == 0:
            self.PPL_BOOLPOSNLAMPSTS_EQ_0 = 1
        if self.current_state['PPL_boolPosnLampSts'] == 1:
            self.PPL_BOOLPOSNLAMPSTS_EQ_1 = 1
        if self.current_state['PPL_boolPosnLampSts'] == 1:
            self.PPL_BOOLPOSNLAMPSTS_EQ_1 = 1
        if self.current_state['PRM_u8PowerSts'] == 2:
            self.PRM_U8POWERSTS_EQ_2 = 1
        if self.current_state['PRM_u8PowerSts'] != self.previous_state['PRM_u8PowerSts'] and self.current_state['PRM_u8PowerSts'] == 1:
            self.PRM_U8POWERSTS_CHANGETO_1 = 1
        if self.current_state['PRM_u8PowerSts'] != self.previous_state['PRM_u8PowerSts'] and self.current_state['PRM_u8PowerSts'] == 0:
            self.PRM_U8POWERSTS_CHANGETO_0 = 1
        if self.current_state['PRM_u8PowerSts'] == 0:
            self.PRM_U8POWERSTS_EQ_0 = 1
        if self.current_state['VcuGearPosn'] == 0:
            self.VCUGEARPOSN_EQ_0 = 1
        if self.current_state['VcuGearPosn'] == 1:
            self.VCUGEARPOSN_EQ_1 = 1
        if self.current_state['VcuGearPosn'] == 1:
            self.VCUGEARPOSN_EQ_1 = 1
        if self.current_state['VcuGearPosn'] != self.current_state['DLC_u8TurnLightTwice']:
            self.VCUGEARPOSN_NEQ_DLC_U8TURNLIGHTTWICE_SIGNALNUM = 1


        if((self.DLC_U8TURNLIGHTTWICE_CHANGE_0XFF == 1)) and ((self.DLC_U8TURNLIGHTTWICE_CHANGE_0XFF == 1)):
             self.current_state["TIMEFLAGNUM"] += 1
        if((self.PRM_U8POWERSTS_CHANGETO_1 == 1) or (self.PRM_U8POWERSTS_CHANGETO_0 == 1)) and ((self.EEP_LOGO_ENABLE_FLAG_EQ_1 == 1)):
             self.current_state["TIMEFLAGNUM"] += 1
        if((self.EEP_LOGO_ENABLE_FLAG_CHANGETO_0 == 1)) and ((self.PRM_U8POWERSTS_EQ_2 == 1)):
             self.current_state["TIMEFLAGNUM"] += 1
        if((self.BDCSEEDSIGNAL_CHANGETO_0 == 1)) and ((self.BDCSEEDSIGNAL_CHANGETO_0 == 1)):
             self.current_state["TIMEFLAGNUM"] += 1
        if self.current_state["TIMEFLAGNUM"] == 0:
            self.TIMEFLAGNUM_EQ_0 = 1 

    def get_current(self, param):
        """获取当前状态值"""
        return self.current_state.get(param)

    def get_previous(self, param):
        """获取前态状态值"""
        return self.previous_state.get(param)



class ComplexRule:
    def __init__(self, condition, action, priority=0):
        """
        :param condition: 用于检查是否满足条件的函数
        :param action: 动作（ACTION_ON 或 ACTION_OFF）
        :param priority: 优先级，数值越小优先级越高
        """
        self.condition = condition
        self.action = action
        self.priority = priority

    def applies_to(self, state):
        """判断规则是否适用于当前的设备状态"""
        return self.condition(state)


class ConflictDetector:
    def __init__(self, rules):
        self.rules = rules
        self.device_state = State(0, 0, 0, 0, 0, 0, 0, 0, 0)

    def detect_and_execute(self,data_tuple):
        (BdcSeedsignal, BdcWlcmsignal, DLC_u8TurnLightTwice, 
                EEP_LOGO_ENABLE_FLAG, EspAutoHoldActvSts, PLB_u8LBSts, 
                PPL_boolPosnLampSts, PRM_u8PowerSts, VcuGearPosn) = data_tuple
        self.device_state.update_state(BdcSeedsignal, BdcWlcmsignal, DLC_u8TurnLightTwice, 
                EEP_LOGO_ENABLE_FLAG, EspAutoHoldActvSts, PLB_u8LBSts, 
                PPL_boolPosnLampSts, PRM_u8PowerSts, VcuGearPosn)
        applied_actions = self._get_applied_actions()
        ResultDict = self.device_state.current_state.copy()
        if not applied_actions:
            ResultDict['Result'] = '无规则适用'
        else:
            if self._has_conflict(applied_actions):
                ErrorDict = {}
                for key, value in self.device_state.current_state.items():
                    ErrorDict[f'{key}'] = value
                ResultDict['Result'] = '可能产生冲突'
                ErrorDict['Result'] = '可能产生冲突'
                ErrorList.append(ErrorDict)
            else:
                chosen_action = applied_actions[0][0]
                ResultDict['Result'] = chosen_action
        self.Result_Add_To_List(ResultDict)

    def Result_Add_To_List(self, ResultDict):
        row = []
        for col_num, (cell_key, cell_value) in enumerate(ResultDict.items()):
            row.append(cell_value)
        ResultList.append(row)
    def _get_applied_actions(self):
        """根据条件筛选适用的规则，并按优先级排序"""
        applied_actions = [
            (rule.action, rule.priority)
            for rule in self.rules
            if rule.applies_to(self.device_state)
        ]
        return sorted(applied_actions, key=lambda x: x[1])

    def _has_conflict(self, applied_actions):
        """检查是否存在开灯和关灯操作冲突"""
        actions = {action for action, _ in applied_actions}
        return (Action0.LGL_ON in actions and Action0.LGL_OFF in actions)

        
def Event_LGL_SEE_ON(device_state):
    return((device_state.BDCSEEDSIGNAL_NEQ_0 == 1))

def Event_LGL_WEL_ON(device_state):
    return((device_state.BDCWLCMSIGNAL_NEQ_0 == 1))

def Event_LGL_VCU_POL_ON(device_state):
    return((device_state.VCUGEARPOSN_EQ_1 == 1) and
           (device_state.PPL_BOOLPOSNLAMPSTS_EQ_1 == 1))

def Event_LGL_VCU_LBL_ON(device_state):
    return((device_state.VCUGEARPOSN_EQ_1 == 1) and
           (device_state.PLB_U8LBSTS_EQ_1 == 1))

def Event_LGL_ESP_POL_ON(device_state):
    return((device_state.ESPAUTOHOLDACTVSTS_EQ_1 == 1) and
           (device_state.PPL_BOOLPOSNLAMPSTS_EQ_1 == 1))

def Event_LGL_ESP_LBL_ON(device_state):
    return((device_state.ESPAUTOHOLDACTVSTS_EQ_1 == 1) and
           (device_state.PLB_U8LBSTS_EQ_1 == 1))

def Event_LGL_PRM_EEP_ON(device_state):
    return((device_state.PRM_U8POWERSTS_EQ_2 == 1) and
           (device_state.EEP_LOGO_ENABLE_FLAG_EQ_1 == 1))

def Event_LGL_DLC_TUL_ON(device_state):
    return((device_state.DLC_U8TURNLIGHTTWICE_CHANGE_0XFF == 1))

def Event_LGL_Normal_OFF(device_state):
    return()

def Event_LGL_Normal_OFF1(device_state):
    return((device_state.BDCSEEDSIGNAL_EQ_0 == 1) and
           (device_state.BDCWLCMSIGNAL_EQ_0 == 1) and
           (device_state.VCUGEARPOSN_EQ_0 == 1) and
           (device_state.PPL_BOOLPOSNLAMPSTS_EQ_0 == 1) and
           (device_state.PLB_U8LBSTS_EQ_0 == 1) and
           (device_state.ESPAUTOHOLDACTVSTS_EQ_0 == 1) and
           (device_state.PRM_U8POWERSTS_CHANGETO_0 == 1) and
           (device_state.TIMEFLAGNUM_EQ_0 == 1))

def Event_LGL_Normal_OFF2(device_state):
    return((device_state.BDCSEEDSIGNAL_EQ_0 == 1) and
           (device_state.BDCWLCMSIGNAL_EQ_0 == 1) and
           (device_state.VCUGEARPOSN_EQ_0 == 1) and
           (device_state.PPL_BOOLPOSNLAMPSTS_EQ_0 == 1) and
           (device_state.PLB_U8LBSTS_EQ_0 == 1) and
           (device_state.ESPAUTOHOLDACTVSTS_EQ_0 == 1) and
           (device_state.EEP_LOGO_ENABLE_FLAG_EQ_0 == 1) and
           (device_state.TIMEFLAGNUM_EQ_0 == 1))

rules = [
    ComplexRule(condition=Event_LGL_SEE_ON,action=Action0.LGL_ON,priority=0),
    ComplexRule(condition=Event_LGL_WEL_ON,action=Action0.LGL_ON,priority=1),
    ComplexRule(condition=Event_LGL_VCU_POL_ON,action=Action0.LGL_ON,priority=2),
    ComplexRule(condition=Event_LGL_VCU_LBL_ON,action=Action0.LGL_ON,priority=3),
    ComplexRule(condition=Event_LGL_ESP_POL_ON,action=Action0.LGL_ON,priority=4),
    ComplexRule(condition=Event_LGL_ESP_LBL_ON,action=Action0.LGL_ON,priority=5),
    ComplexRule(condition=Event_LGL_PRM_EEP_ON,action=Action0.LGL_ON,priority=6),
    ComplexRule(condition=Event_LGL_DLC_TUL_ON,action=Action0.LGL_ON,priority=7),
    ComplexRule(condition=Event_LGL_Normal_OFF1,action=Action0.LGL_OFF,priority=8),
    ComplexRule(condition=Event_LGL_Normal_OFF2,action=Action0.LGL_OFF,priority=9),

]
def Save_Result():
    ResultDataFrame = pd.DataFrame(ResultList, columns=['BdcSeedsignal', 'BdcWlcmsignal', 'DLC_u8TurnLightTwice', 'EEP_LOGO_ENABLE_FLAG', 'EspAutoHoldActvSts', 'PLB_u8LBSts', 'PPL_boolPosnLampSts', 'PRM_u8PowerSts', 'VcuGearPosn', 'TIMEFLAGNUM', 'Result'])
    ResultDataFrame.to_excel('Result.xlsx', sheet_name='Result', index=False)
def main():
    detector = ConflictDetector(rules)
    ENVIRONMENT_FILE = 'CartesianProduct.xlsx'
    BATCH_SIZE = 10000
    skip_rows = 0
    times = 0
    while True:
        try:
            if times != 0:
                EnvironmentDataFrame = pd.read_excel(ENVIRONMENT_FILE, sheet_name=0, nrows=BATCH_SIZE, skiprows=skip_rows , header=None)
            else:
                EnvironmentDataFrame = pd.read_excel(ENVIRONMENT_FILE, sheet_name=0, nrows=BATCH_SIZE, skiprows=skip_rows)
            if EnvironmentDataFrame.empty:
                break
            for index, row in EnvironmentDataFrame.iterrows():
                detector.detect_and_execute(tuple(row))
            skip_rows += BATCH_SIZE
            times += 1
        except FileNotFoundError:
            print("文件不存在")
            break
    Save_Result()
    if not ErrorList:
        print("No errors")
    else:
        for ErrorDict in ErrorList:
            print(ErrorDict)


if __name__ == '__main__':
    main()
