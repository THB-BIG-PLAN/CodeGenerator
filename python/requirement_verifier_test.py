
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
