
import pandas as pd
from enum import Enum
import warnings
import re

warnings.simplefilter(action='ignore', category=UserWarning)
class Action1(Enum):
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
        if(((self.current_state['DLC_u8TurnLightTwice']!= self.previous_state['DLC_u8TurnLightTwice']))) and ((self.current_state['DLC_u8TurnLightTwice']!= self.previous_state['DLC_u8TurnLightTwice'])):
            self.current_state['TIMEFLAGNUM'] += 1
        if(((self.current_state['PRM_u8PowerSts']!= self.previous_state['PRM_u8PowerSts']) and (self.current_state['PRM_u8PowerSts'] == 1)or ((self.current_state['PRM_u8PowerSts']!= self.previous_state['PRM_u8PowerSts']) and (self.current_state['PRM_u8PowerSts'] == 0))) and ((self.current_state['EEP_LOGO_ENABLE_FLAG'] == 1)):
            self.current_state['TIMEFLAGNUM'] += 1
        if(((self.current_state['EEP_LOGO_ENABLE_FLAG']!= self.previous_state['EEP_LOGO_ENABLE_FLAG']) and (self.current_state['EEP_LOGO_ENABLE_FLAG'] == 0))) and ((self.current_state['PRM_u8PowerSts'] == 2)):
            self.current_state['TIMEFLAGNUM'] += 1
        if(((self.current_state['BdcSeedsignal']!= self.previous_state['BdcSeedsignal']) and (self.current_state['BdcSeedsignal'] == 0))) and ((self.current_state['BdcSeedsignal']!= self.previous_state['BdcSeedsignal']) and (self.current_state['BdcSeedsignal'] == 0)):
            self.current_state['TIMEFLAGNUM'] += 1
