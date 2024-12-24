#!/usr/bin/python
# -*- coding: GBK -*-
import pandas as pd
import openpyxl



ON = 'ON'
OFF = 'OFF'

resultDataFrame = pd.DataFrame(columns=['BdcSeedsignal', 'BdcWlcmsignal', 'DLC_u8TurnLightTwice', 
'EEP_LOGO_ENABLE_FLAG', 'EspAutoHoldActvSts', 'PLB_u8LBSts', 
'PPL_boolPosnLampSts', 'PRM_u8PowerSts', 'VcuGearPosn', 
'result'])

signal_num = 10
class State:
	def __init__(self, states_tuple):
		keys = ['BdcSeedsignal', 'BdcWlcmsignal', 'DLC_u8TurnLightTwice', 'EEP_LOGO_ENABLE_FLAG', 'EspAutoHoldActvSts', 'PLB_u8LBSts', 'PPL_boolPosnLampSts', 'PRM_u8PowerSts', 'VcuGearPosn', 'TIMEFLAGNUM']
		self.BDCSEEDSIGNAL_NEQ_0 = None
		self.BDCSEEDSIGNAL_CHANGE_BDCSEEDSIGNAL_PRE = None
		self.BDCSEEDSIGNAL_EQ_0 = None
		self.BDCWLCMSIGNAL_NEQ_0 = None
		self.BDCWLCMSIGNAL_EQ_0 = None
		self.DLC_U8TURNLIGHTTWICE_CHANGE_DLC_U8TURNLIGHTTWICE_PRE = None
		self.EEP_LOGO_ENABLE_FLAG_EQ_1 = None
		self.EEP_LOGO_ENABLE_FLAG_CHANGE_EEP_LOGO_ENABLE_FLAG_PRE = None
		self.EEP_LOGO_ENABLE_FLAG_EQ_0 = None
		self.ESPAUTOHOLDACTVSTS_EQ_0 = None
		self.ESPAUTOHOLDACTVSTS_EQ_1 = None
		self.PLB_U8LBSTS_EQ_1 = None
		self.PLB_U8LBSTS_EQ_0 = None
		self.PPL_BOOLPOSNLAMPSTS_EQ_0 = None
		self.PPL_BOOLPOSNLAMPSTS_EQ_1 = None
		self.PRM_U8POWERSTS_EQ_2 = None
		self.PRM_U8POWERSTS_CHANGE_PRM_U8POWERSTS_PRE = None
		self.PRM_U8POWERSTS_EQ_0 = None
		self.PRM_U8POWERSTS_PRE_EQ_2 = None
		self.VCUGEARPOSN_EQ_0 = None
		self.VCUGEARPOSN_EQ_1 = None
		self.VCUGEARPOSN_NEQ_DLC_U8TURNLIGHTTWICE = None
		self.VCUGEARPOSN_EQ_3 = None
		self.VCUGEARPOSN_PRE_EQ_2 = None
		self.TIMEFLAGNUM_EQ_0 = None

		self.LGL_Set_Set = set()

		self.current_state = {key: None for key in keys}
		self.previous_state = {key: None for key in keys}
		self.update_state(states_tuple)

	def update_state(self, states_tuple):
		for k in self.current_state.keys():
			self.previous_state[k] = self.current_state[k]
		(self.current_state['BdcSeedsignal'], self.current_state['BdcWlcmsignal'], self.current_state['DLC_u8TurnLightTwice'], 
		 self.current_state['EEP_LOGO_ENABLE_FLAG'], self.current_state['EspAutoHoldActvSts'], self.current_state['PLB_u8LBSts'], 
		 self.current_state['PPL_boolPosnLampSts'], self.current_state['PRM_u8PowerSts'], self.current_state['VcuGearPosn']
		 ) = states_tuple[:9]

		self.current_state['TIMEFLAGNUM'] = 0
		self.calculate_flags()
		self.LGL_Set_Set = set()
	def LGL_Set(self, Status):
		self.LGL_Set_Set.add(Status)

	def calculate_flags(self):
		self.BDCSEEDSIGNAL_NEQ_0 = 1 if self.current_state['BdcSeedsignal'] != 0 else 0
		self.BDCSEEDSIGNAL_CHANGE_BDCSEEDSIGNAL_PRE = 1 if self.current_state['BdcSeedsignal'] != self.previous_state['BdcSeedsignal'] else 0
		self.BDCSEEDSIGNAL_EQ_0 = 1 if self.current_state['BdcSeedsignal'] == 0 else 0
		self.BDCSEEDSIGNAL_EQ_0 = 1 if self.current_state['BdcSeedsignal'] == 0 else 0
		self.BDCWLCMSIGNAL_NEQ_0 = 1 if self.current_state['BdcWlcmsignal'] != 0 else 0
		self.BDCWLCMSIGNAL_EQ_0 = 1 if self.current_state['BdcWlcmsignal'] == 0 else 0
		self.DLC_U8TURNLIGHTTWICE_CHANGE_DLC_U8TURNLIGHTTWICE_PRE = 1 if self.current_state['DLC_u8TurnLightTwice'] != self.previous_state['DLC_u8TurnLightTwice'] else 0
		self.EEP_LOGO_ENABLE_FLAG_EQ_1 = 1 if self.current_state['EEP_LOGO_ENABLE_FLAG'] == 1 else 0
		self.EEP_LOGO_ENABLE_FLAG_CHANGE_EEP_LOGO_ENABLE_FLAG_PRE = 1 if self.current_state['EEP_LOGO_ENABLE_FLAG'] != self.previous_state['EEP_LOGO_ENABLE_FLAG'] else 0
		self.EEP_LOGO_ENABLE_FLAG_EQ_0 = 1 if self.current_state['EEP_LOGO_ENABLE_FLAG'] == 0 else 0
		self.EEP_LOGO_ENABLE_FLAG_EQ_0 = 1 if self.current_state['EEP_LOGO_ENABLE_FLAG'] == 0 else 0
		self.ESPAUTOHOLDACTVSTS_EQ_0 = 1 if self.current_state['EspAutoHoldActvSts'] == 0 else 0
		self.ESPAUTOHOLDACTVSTS_EQ_1 = 1 if self.current_state['EspAutoHoldActvSts'] == 1 else 0
		self.ESPAUTOHOLDACTVSTS_EQ_1 = 1 if self.current_state['EspAutoHoldActvSts'] == 1 else 0
		self.PLB_U8LBSTS_EQ_1 = 1 if self.current_state['PLB_u8LBSts'] == 1 else 0
		self.PLB_U8LBSTS_EQ_0 = 1 if self.current_state['PLB_u8LBSts'] == 0 else 0
		self.PLB_U8LBSTS_EQ_1 = 1 if self.current_state['PLB_u8LBSts'] == 1 else 0
		self.PPL_BOOLPOSNLAMPSTS_EQ_0 = 1 if self.current_state['PPL_boolPosnLampSts'] == 0 else 0
		self.PPL_BOOLPOSNLAMPSTS_EQ_1 = 1 if self.current_state['PPL_boolPosnLampSts'] == 1 else 0
		self.PPL_BOOLPOSNLAMPSTS_EQ_1 = 1 if self.current_state['PPL_boolPosnLampSts'] == 1 else 0
		self.PRM_U8POWERSTS_EQ_2 = 1 if self.current_state['PRM_u8PowerSts'] == 2 else 0
		self.PRM_U8POWERSTS_CHANGE_PRM_U8POWERSTS_PRE = 1 if self.current_state['PRM_u8PowerSts'] != self.previous_state['PRM_u8PowerSts'] else 0
		self.PRM_U8POWERSTS_EQ_0 = 1 if self.current_state['PRM_u8PowerSts'] == 0 else 0
		self.PRM_U8POWERSTS_PRE_EQ_2 = 1 if self.previous_state['PRM_u8PowerSts']== 2 else 0
		self.VCUGEARPOSN_EQ_0 = 1 if self.current_state['VcuGearPosn'] == 0 else 0
		self.VCUGEARPOSN_EQ_1 = 1 if self.current_state['VcuGearPosn'] == 1 else 0
		self.VCUGEARPOSN_EQ_1 = 1 if self.current_state['VcuGearPosn'] == 1 else 0
		self.VCUGEARPOSN_NEQ_DLC_U8TURNLIGHTTWICE = 1 if self.current_state['VcuGearPosn'] != self.current_state['DLC_u8TurnLightTwice'] else 0
		self.VCUGEARPOSN_EQ_3 = 1 if self.current_state['VcuGearPosn'] == 3 else 0
		self.VCUGEARPOSN_PRE_EQ_2 = 1 if self.previous_state['VcuGearPosn']== 2 else 0

		if self.DLC_U8TURNLIGHTTWICE_CHANGE_DLC_U8TURNLIGHTTWICE_PRE:
			self.current_state['TIMEFLAGNUM'] += 1
		if self.PRM_U8POWERSTS_CHANGE_PRM_U8POWERSTS_PRE and self.PRM_U8POWERSTS_PRE_EQ_2:
			self.current_state['TIMEFLAGNUM'] += 1
		if self.PRM_U8POWERSTS_EQ_2 and self.EEP_LOGO_ENABLE_FLAG_CHANGE_EEP_LOGO_ENABLE_FLAG_PRE and self.EEP_LOGO_ENABLE_FLAG_EQ_0:
			self.current_state['TIMEFLAGNUM'] += 1
		if self.BDCSEEDSIGNAL_CHANGE_BDCSEEDSIGNAL_PRE and self.BDCSEEDSIGNAL_EQ_0:
			self.current_state['TIMEFLAGNUM'] += 1
		self.TIMEFLAGNUM_EQ_0 = 1 if self.current_state['TIMEFLAGNUM'] == 0 else 0

	def get_current_state(self, param):
		return self.current_state.get(param)

	def get_previous_state(self, param):
		return self.previous_state.get(param)


class ComplexRule:
    def __init__(self, condition):
        self.condition = condition

    def check_condition(self, state):
        try:
            self.condition(state)
        except Exception as e:
            print(f"执行规则时发生错误: {e}")

class ConflictDetector:
    def __init__(self, rules):
        self.rules = rules
        self.device_state = State(tuple(0 for _ in range(signal_num)))
    
    
    def detect_and_execute(self, states_tuple):
        result = ''
        self.device_state.update_state(states_tuple)
        for rule in self.rules:
            rule.check_condition(self.device_state)
        if len(self.device_state.LGL_Set_Set) > 1:
            result = 'Conflict'
        elif len(self.device_state.LGL_Set_Set) == 1:
            result = self.device_state.LGL_Set_Set.pop()
        elif len(self.device_state.LGL_Set_Set) == 0:
            result = 'No action needed'
        new_row = {**self.device_state.current_state, 'result': result}
        self.device_state.LGL_Set_Set.clear()

        return new_row

def EventLGL_SEE_ON(device_state):
	if (device_state.BDCSEEDSIGNAL_NEQ_0):
		device_state.LGL_Set(ON)


def EventLGL_WEL_ON(device_state):
	if (device_state.BDCWLCMSIGNAL_NEQ_0):
		device_state.LGL_Set(ON)


def EventLGL_VCU_POL_ON(device_state):
	if (device_state.VCUGEARPOSN_EQ_1 and device_state.PPL_BOOLPOSNLAMPSTS_EQ_1):
		device_state.LGL_Set(ON)


def EventLGL_VCU_LBL_ON(device_state):
	if (device_state.VCUGEARPOSN_EQ_1 and device_state.PLB_U8LBSTS_EQ_1):
		device_state.LGL_Set(ON)


def EventLGL_ESP_POL_ON(device_state):
	if (device_state.ESPAUTOHOLDACTVSTS_EQ_1 and device_state.PPL_BOOLPOSNLAMPSTS_EQ_1):
		device_state.LGL_Set(ON)


def EventLGL_ESP_LBL_ON(device_state):
	if (device_state.ESPAUTOHOLDACTVSTS_EQ_1 and device_state.PLB_U8LBSTS_EQ_1):
		device_state.LGL_Set(ON)


def EventLGL_PRM_EEP_ON(device_state):
	if (device_state.PRM_U8POWERSTS_EQ_2 and device_state.EEP_LOGO_ENABLE_FLAG_EQ_1):
		device_state.LGL_Set(ON)


def EventLGL_DLC_TUL_ON(device_state):
	if (device_state.DLC_U8TURNLIGHTTWICE_CHANGE_DLC_U8TURNLIGHTTWICE_PRE):
		device_state.LGL_Set(ON)


def EventLGL_Normal_OFF1(device_state):
	if (device_state.BDCSEEDSIGNAL_EQ_0 and device_state.BDCWLCMSIGNAL_EQ_0 and 
		device_state.VCUGEARPOSN_EQ_0 and device_state.PPL_BOOLPOSNLAMPSTS_EQ_0 and 
		device_state.PLB_U8LBSTS_EQ_0 and device_state.ESPAUTOHOLDACTVSTS_EQ_0 and 
		device_state.PRM_U8POWERSTS_EQ_0 and device_state.TIMEFLAGNUM_EQ_0):
		device_state.LGL_Set(OFF)


def EventLGL_Normal_OFF2(device_state):
	if (device_state.BDCSEEDSIGNAL_EQ_0 and device_state.BDCWLCMSIGNAL_EQ_0 and 
		device_state.VCUGEARPOSN_EQ_0 and device_state.PPL_BOOLPOSNLAMPSTS_EQ_0 and 
		device_state.PLB_U8LBSTS_EQ_0 and device_state.ESPAUTOHOLDACTVSTS_EQ_0 and 
		device_state.EEP_LOGO_ENABLE_FLAG_EQ_0 and device_state.TIMEFLAGNUM_EQ_0):
		device_state.LGL_Set(OFF)

rules = [
	ComplexRule(condition= EventLGL_SEE_ON),
	ComplexRule(condition= EventLGL_WEL_ON),
	ComplexRule(condition= EventLGL_VCU_POL_ON),
	ComplexRule(condition= EventLGL_VCU_LBL_ON),
	ComplexRule(condition= EventLGL_ESP_POL_ON),
	ComplexRule(condition= EventLGL_ESP_LBL_ON),
	ComplexRule(condition= EventLGL_PRM_EEP_ON),
	ComplexRule(condition= EventLGL_DLC_TUL_ON),
	ComplexRule(condition= EventLGL_Normal_OFF1),
	ComplexRule(condition= EventLGL_Normal_OFF2),
]
def main():
    detector = ConflictDetector(rules)
    ENVIRONMENT_FILE = 'CartesianProduct.xlsx'
    BATCH_SIZE = 100000
    skip_rows = 0
    new_rows = []
    while True:
        try:
            EnvironmentDataFrame = pd.read_excel(
                ENVIRONMENT_FILE, sheet_name=0, nrows=BATCH_SIZE, skiprows=skip_rows
            )
            if EnvironmentDataFrame.empty:
                break
            for index, row in EnvironmentDataFrame.iterrows():
                new_row = detector.detect_and_execute(tuple(row))
                new_rows.append(new_row)
            skip_rows += BATCH_SIZE
        except FileNotFoundError:
            print("文件不存在")
            break

    global resultDataFrame
    resultDataFrame = pd.concat([resultDataFrame, pd.DataFrame(new_rows)], ignore_index=True)
    with pd.ExcelWriter('result.xlsx', engine='openpyxl') as writer:
        resultDataFrame.to_excel(writer, index=False)

        # 获取工作表对象
        worksheet = writer.sheets['Sheet1']

        # 调整列宽
        for column in worksheet.columns:
            max_length = 0
            column = column[0].column_letter  # 获取列字母
            for cell in worksheet[column]:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)*1.3  # 增加一些额外的宽度
            worksheet.column_dimensions[column].width = adjusted_width

    print("Excel文件已生成，并且列宽已调整")


if __name__ == '__main__':
    main()
