import pandas as pd
from enum import Enum
import warnings


class Action(Enum):
    LGL_ON = 0
    LGL_OFF = 1


WEL_NO_REQ = 0x0
SEE_NO_REQ = 0x0
VCU_GEAR_P = 0x1
ESP_AUTO_HOLD = 0x1
POL_STS_ON = 0x1
POL_STS_OFF = 0x0
LBL_STS_ON = 0x1
LBL_STS_OFF = 0x0
PRM_PWR_ON = 0x2
EEP_LGL_ENABLE = 0x1
EEP_LGL_DISABLE = 0x0
PRM_PWR_OFF = 0x0


# 定义复杂规则类
class State:
    def __init__(self, BdcSeedsignal, BdcWlcmsignal, DLC_u8TurnLightTwice, EEP_LOGO_ENABLE_FLAG, EspAutoHoldActvSts,
                 PLB_u8LBSts, PPL_boolPosnLampSts, PRM_u8PowerSts, VcuGearPosn):
        self.current_state = {'BdcSeedsignal': BdcSeedsignal, 'BdcWlcmsignal': BdcWlcmsignal,
                              'DLC_u8TurnLightTwice': DLC_u8TurnLightTwice,
                              'EEP_LOGO_ENABLE_FLAG': EEP_LOGO_ENABLE_FLAG,
                              'EspAutoHoldActvSts': EspAutoHoldActvSts, 'PLB_u8LBSts': PLB_u8LBSts,
                              'PPL_boolPosnLampSts': PPL_boolPosnLampSts, 'PRM_u8PowerSts': PRM_u8PowerSts,
                              'VcuGearPosn': VcuGearPosn, 'LGL_TIMEFLAGNUM': 0, }
        self.previous_state = {k: 0 for k in self.current_state.keys()}  # 确保初始状态

        if self.current_state['DLC_u8TurnLightTwice'] != self.previous_state['DLC_u8TurnLightTwice']:
            self.current_state['LGL_TIMEFLAGNUM'] += 1
        if self.current_state['PRM_u8PowerSts'] != PRM_PWR_ON and self.previous_state['PRM_u8PowerSts'] == PRM_PWR_ON:
            self.current_state['LGL_TIMEFLAGNUM'] += 1
        if (self.current_state['EEP_LOGO_ENABLE_FLAG'] == EEP_LGL_DISABLE and
            self.previous_state['EEP_LOGO_ENABLE_FLAG'] == EEP_LGL_ENABLE):
            self.current_state['LGL_TIMEFLAGNUM'] += 1
        if self.current_state['BdcSeedsignal'] == SEE_NO_REQ and self.previous_state['BdcSeedsignal'] != SEE_NO_REQ:
            self.current_state['LGL_TIMEFLAGNUM'] += 1

    def update_state(self, BdcSeedsignal, BdcWlcmsignal, DLC_u8TurnLightTwice, EEP_LOGO_ENABLE_FLAG, EspAutoHoldActvSts,
                     PLB_u8LBSts, PPL_boolPosnLampSts, PRM_u8PowerSts, VcuGearPosn):
        self.previous_state = self.current_state.copy()
        self.current_state = {'BdcSeedsignal': BdcSeedsignal, 'BdcWlcmsignal': BdcWlcmsignal,
                              'DLC_u8TurnLightTwice': DLC_u8TurnLightTwice,
                              'EEP_LOGO_ENABLE_FLAG': EEP_LOGO_ENABLE_FLAG,
                              'EspAutoHoldActvSts': EspAutoHoldActvSts, 'PLB_u8LBSts': PLB_u8LBSts,
                              'PPL_boolPosnLampSts': PPL_boolPosnLampSts, 'PRM_u8PowerSts': PRM_u8PowerSts,
                              'VcuGearPosn': VcuGearPosn,
                              'LGL_TIMEFLAGNUM': 0}
        # 增量逻辑
        if self.current_state['DLC_u8TurnLightTwice'] != self.previous_state['DLC_u8TurnLightTwice']:
            self.current_state['LGL_TIMEFLAGNUM'] += 1
        if self.current_state['PRM_u8PowerSts'] != PRM_PWR_ON and self.previous_state['PRM_u8PowerSts'] == PRM_PWR_ON:
            self.current_state['LGL_TIMEFLAGNUM'] += 1
        if (self.current_state['EEP_LOGO_ENABLE_FLAG'] == EEP_LGL_DISABLE and
                self.previous_state['EEP_LOGO_ENABLE_FLAG'] == EEP_LGL_ENABLE):
            self.current_state['LGL_TIMEFLAGNUM'] += 1
        if self.current_state['BdcSeedsignal'] == SEE_NO_REQ and self.previous_state['BdcSeedsignal'] != SEE_NO_REQ:
            self.current_state['LGL_TIMEFLAGNUM'] += 1

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
        self.device_state = State(0, 0, 0, 0, 0, 0, 0, 0, 0)  # 初始化设备状态

    def detect_and_execute(self, BdcSeedsignal, BdcWlcmsignal, DLC_u8TurnLightTwice, EEP_LOGO_ENABLE_FLAG,
                           EspAutoHoldActvSts,
                           PLB_u8LBSts, PPL_boolPosnLampSts, PRM_u8PowerSts, VcuGearPosn):
        self.device_state.update_state(BdcSeedsignal, BdcWlcmsignal, DLC_u8TurnLightTwice, EEP_LOGO_ENABLE_FLAG,
                                       EspAutoHoldActvSts, PLB_u8LBSts, PPL_boolPosnLampSts, PRM_u8PowerSts,
                                       VcuGearPosn)
        applied_actions = self._get_applied_actions()
        if not applied_actions:
            print(f"BdcSeedsignal :{BdcSeedsignal}\n"
                  f"BdcWlcmsignal :{BdcWlcmsignal}\n"
                  f"DLC_u8TurnLightTwice :{DLC_u8TurnLightTwice}\n"
                  f"EEP_LOGO_ENABLE_FLAG: {EEP_LOGO_ENABLE_FLAG}\n"
                  f"EspAutoHoldActvSts :{EspAutoHoldActvSts}\n"
                  f"PLB_u8LBSts :{PLB_u8LBSts}\n"
                  f"PPL_boolPosnLampSts :{PPL_boolPosnLampSts}\n"
                  f"PRM_u8PowerSts :{PRM_u8PowerSts}\n"
                  f"VcuGearPosn :{VcuGearPosn}时，无规则适用\n")
            return False
        else:
            if self._has_conflict(applied_actions):
                print(f"BdcSeedsignal :{BdcSeedsignal}\n"
                      f"BdcWlcmsignal :{BdcWlcmsignal}\n "
                      f"DLC_u8TurnLightTwice :{DLC_u8TurnLightTwice}\n"
                      f"EEP_LOGO_ENABLE_FLAG: {EEP_LOGO_ENABLE_FLAG}\n"
                      f"EspAutoHoldActvSts :{EspAutoHoldActvSts}\n"
                      f"PLB_u8LBSts :{PLB_u8LBSts}\n"
                      f"PPL_boolPosnLampSts :{PPL_boolPosnLampSts}\n"
                      f"PRM_u8PowerSts :{PRM_u8PowerSts}\n"
                      f"VcuGearPosn :{VcuGearPosn}时，可能产生冲突\n")
                return True
            else:
                chosen_action = applied_actions[0][0]
                print(f"BdcSeedsignal :{BdcSeedsignal}\n"
                      f"BdcWlcmsignal :{BdcWlcmsignal}\n"
                      f"DLC_u8TurnLightTwice :{DLC_u8TurnLightTwice}\n"
                      f"EEP_LOGO_ENABLE_FLAG: {EEP_LOGO_ENABLE_FLAG}\n"
                      f"EspAutoHoldActvSts :{EspAutoHoldActvSts}\n"
                      f"PLB_u8LBSts :{PLB_u8LBSts}\n"
                      f"PPL_boolPosnLampSts :{PPL_boolPosnLampSts}\n"
                      f"PRM_u8PowerSts :{PRM_u8PowerSts}\n"
                      f"VcuGearPosn :{VcuGearPosn}时，执行{chosen_action.name}\n")
                return False

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
        return Action.LGL_ON in actions and Action.LGL_OFF in actions


def Event1(device_state):
    return device_state.get_current("BdcSeedsignal") != SEE_NO_REQ



def Event2(device_state):
    return device_state.get_current("BdcWlcmsignal") != WEL_NO_REQ


def Event3(device_state):
    return (device_state.get_current("VcuGearPosn") == VCU_GEAR_P and
            device_state.get_current("PPL_boolPosnLampSts") == POL_STS_ON)


def Event4(device_state):
    return (device_state.get_current("VcuGearPosn") == VCU_GEAR_P and
            device_state.get_current("PLB_u8LBSts") == LBL_STS_ON)


def Event5(device_state):
    return (device_state.get_current("EspAutoHoldActvSts") == ESP_AUTO_HOLD and
            device_state.get_current("PPL_boolPosnLampSts") == POL_STS_ON)


def Event6(device_state):
    return (device_state.get_current("EspAutoHoldActvSts") == ESP_AUTO_HOLD and
            device_state.get_current("PLB_u8LBSts") == LBL_STS_ON)


def Event7(device_state):
    return (device_state.get_current("PRM_u8PowerSts") == PRM_PWR_ON and
            device_state.get_current("EEP_LOGO_ENABLE_FLAG") == EEP_LGL_ENABLE)


def Event8(device_state):
    return (device_state.get_current("DLC_u8TurnLightTwice") !=
            device_state.get_previous("DLC_u8TurnLightTwice"))


def Event9(device_state):
    return (device_state.get_current("BdcSeedsignal") == SEE_NO_REQ and
            device_state.get_current("BdcWlcmsignal") == WEL_NO_REQ and
            device_state.get_current("VcuGearPosn") == 0 and
            device_state.get_current("PPL_boolPosnLampSts") == POL_STS_OFF and
            device_state.get_current("PLB_u8LBSts") == LBL_STS_OFF and
            device_state.get_current("EspAutoHoldActvSts") == 0 and
            device_state.get_current("EEP_LOGO_ENABLE_FLAG") == EEP_LGL_DISABLE and
            device_state.get_current("LGL_TIMEFLAGNUM") == 0)


def Event10(device_state):
    return (device_state.get_current("BdcSeedsignal") == SEE_NO_REQ and
            device_state.get_current("BdcWlcmsignal") == WEL_NO_REQ and
            device_state.get_current("VcuGearPosn") == 0 and
            device_state.get_current("PPL_boolPosnLampSts") == POL_STS_OFF and
            device_state.get_current("PLB_u8LBSts") == LBL_STS_OFF and
            device_state.get_current("EspAutoHoldActvSts") == 0 and
            device_state.get_current("PRM_u8PowerSts") == PRM_PWR_OFF and
            device_state.get_current("LGL_TIMEFLAGNUM") == 0)


rules = [
    ComplexRule(condition=Event1, action=Action.LGL_ON, priority=1),
    ComplexRule(condition=Event2, action=Action.LGL_ON, priority=2),
    ComplexRule(condition=Event3, action=Action.LGL_ON, priority=3),
    ComplexRule(condition=Event4, action=Action.LGL_ON, priority=4),
    ComplexRule(condition=Event5, action=Action.LGL_ON, priority=5),
    ComplexRule(condition=Event6, action=Action.LGL_ON, priority=6),
    ComplexRule(condition=Event7, action=Action.LGL_ON, priority=7),
    ComplexRule(condition=Event8, action=Action.LGL_ON, priority=8),
    ComplexRule(condition=Event9, action=Action.LGL_OFF, priority=9),
    ComplexRule(condition=Event10, action=Action.LGL_OFF, priority=10),
]

detector = ConflictDetector(rules)
detector.detect_and_execute(0, 0, 254, 0, 0, 0, 0, 0, 0)
detector.detect_and_execute(0, 0, 255, 2, 1, 2, 1, 1, 0)
detector.detect_and_execute(0, 0, 255, 0,0,0, 0,0,0)
