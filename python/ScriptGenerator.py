import pandas as pd
from enum import Enum
import warnings
import re


def main():
    warnings.simplefilter(action='ignore', category=UserWarning)
    CONFIG_FILE = "config.xlsx"
    WRITE_FILE = "requirement_verifier.py"
    ActionDataFrame = pd.read_excel(CONFIG_FILE, sheet_name="Action")
    SignalDataFrame = pd.read_excel(CONFIG_FILE, sheet_name=0)
    RequirementVerifierFile = open(WRITE_FILE, "w")
    HEADER = '''
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
Result = pd.DataFrame(columns=['''

    for i, row in SignalDataFrame.iterrows():
        HEADER += f"'{row.iloc[0]}', "

    HEADER += "'TIMEFLAGNUM', 'Action'])\n"

    RequirementVerifierFile.write(HEADER)
    ActionGroup = None
    ActionNumber = 0
    for i, row in ActionDataFrame.iterrows():
        if pd.notna(row.iloc[0]) and ActionGroup == row.iloc[0]:
            ActionString = re.sub(r'\(\)$', '', row.iloc[1])
            RequirementVerifierFile.write(f'    {ActionString} = {ActionNumber}\n')
            ActionNumber += 1
        if pd.notna(row.iloc[0]) and ActionGroup is None:
            RequirementVerifierFile.write(f'class Action{int(row.iloc[0])}(Enum):\n')
            ActionGroup = row.iloc[0]
            ActionString = re.sub(r'\(\)$', '', row.iloc[1])
            RequirementVerifierFile.write(f'    {ActionString} = {ActionNumber}\n')
            ActionNumber += 1
        if pd.notna(row.iloc[0]) and ActionGroup != row.iloc[0]:
            RequirementVerifierFile.write(f'class Action{int(row.iloc[0])}(Enum):\n')
            ActionGroup = row.iloc[0]
            ActionString = re.sub(r'\(\)$', '', row.iloc[1])
            RequirementVerifierFile.write(f'    {ActionString} = {ActionNumber}\n')
            ActionNumber += 1

    SignalString = ''  # SignalString = 'Signal1, Signal2, Signal3'
    StateString = ''  # StateString = "'Signal1' :Signal1, 'Signal2' :Signal2, 'Signal3' :Signal3"
    EventDataFrame = pd.read_excel(CONFIG_FILE, sheet_name=4)
    ConditionDataFrame = pd.read_excel(CONFIG_FILE, sheet_name=2)
    rownum = 3
    SignalNumber = len(SignalDataFrame)
    for i, row in SignalDataFrame.iterrows():
        if i != 0 and i % rownum == 0:
            SignalString += '\n                '
            StateString += '\n                '
        SignalString += (f'{row.iloc[0]}' + (', ' if i != len(SignalDataFrame) - 1 else ''))
        StateString += (f"'{row.iloc[0]}': {row.iloc[0]}" + ', ')
    StateString += "'TIMEFLAGNUM': 0"
    RequirementVerifierFile.write(f'''
class State:
    def __init__(self, {SignalString}):
        self.current_state = {{{StateString}}}
        self.previous_state = {{k: 0 for k in self.current_state.keys()}}
''')

    # 条件宏清零
    ConditionMacroDataFrame = pd.read_excel(CONFIG_FILE, sheet_name=5)
    ConditionMacroString = ''
    for i, row in ConditionMacroDataFrame.iterrows():
        ConditionMacroString += f'        self.{row.iloc[0]} = 0 \n'
    RequirementVerifierFile.write(ConditionMacroString)
    RequirementVerifierFile.write('\n')
    # 条件宏赋值
    ConditionString = ''
    for i, row in ConditionDataFrame.iterrows():
        ConditionString += f'        if '
        if row.iloc[1] == 'EQ':
            if row.iloc[3] == 'CONDITION_TYPE_NUMBER':
                ConditionString += f"self.current_state['{row.iloc[0]}'] == {row.iloc[2]}:\n"
                ConditionString += f'            self.{row.iloc[5]} = 1\n'
            else:
                ThresholdSignal = re.sub(r'_SIGNALNUM$', '', row.iloc[2])
                ConditionString += f"self.current_state['{row.iloc[0]}'] == self.current_state['{ThresholdSignal}']:\n"
                ConditionString += f"            self.{row.iloc[5]} = 1\n"
        elif row.iloc[1] == 'NEQ':
            if row.iloc[3] == 'CONDITION_TYPE_NUMBER':
                ConditionString += f"self.current_state['{row.iloc[0]}'] != {row.iloc[2]}:\n"
                ConditionString += f'            self.{row.iloc[5]} = 1\n'
            else:
                ThresholdSignal = re.sub(r'_SIGNALNUM$', '', row.iloc[2])
                ConditionString += f"self.current_state['{row.iloc[0]}'] != self.current_state['{ThresholdSignal}']:\n"
                ConditionString += f"            self.{row.iloc[5]} = 1\n"
        elif row.iloc[1] == 'GREATER':
            if row.iloc[3] == 'CONDITION_TYPE_NUMBER':
                ConditionString += f"self.current_state['{row.iloc[0]}'] > {row.iloc[2]}:\n"
                ConditionString += f'            self.{row.iloc[5]} = 1\n'
            else:
                ThresholdSignal = re.sub(r'_SIGNALNUM$', '', row.iloc[2])
                ConditionString += f"self.current_state['{row.iloc[0]}'] > self.current_state['{ThresholdSignal}']:\n"
                ConditionString += f"            self.{row.iloc[5]} = 1\n"
        elif row.iloc[1] == 'GREATEROREQ':
            if row.iloc[3] == 'CONDITION_TYPE_NUMBER':
                ConditionString += f"self.current_state['{row.iloc[0]}'] >= {row.iloc[2]}:\n"
                ConditionString += f'            self.{row.iloc[5]} = 1\n'
            else:
                ThresholdSignal = re.sub(r'_SIGNALNUM$', '', row.iloc[2])
                ConditionString += f"self.current_state['{row.iloc[0]}'] >= self.current_state['{ThresholdSignal}']:\n"
                ConditionString += f"            self.{row.iloc[5]} = 1\n"
        elif row.iloc[1] == 'LESS':
            if row.iloc[3] == 'CONDITION_TYPE_NUMBER':
                ConditionString += f"self.current_state['{row.iloc[0]}'] < {row.iloc[2]}:\n"
                ConditionString += f'            self.{row.iloc[5]} = 1\n'
            else:
                ThresholdSignal = re.sub(r'_SIGNALNUM$', '', row.iloc[2])
                ConditionString += f"self.current_state['{row.iloc[0]}'] < self.current_state['{ThresholdSignal}']:\n"
                ConditionString += f"            self.{row.iloc[5]} = 1\n"
        elif row.iloc[1] == 'LESSOREQ':
            if row.iloc[3] == 'CONDITION_TYPE_NUMBER':
                ConditionString += f"self.current_state['{row.iloc[0]}'] <= {row.iloc[2]}:\n"
                ConditionString += f'            self.{row.iloc[5]} = 1\n'
            else:
                ThresholdSignal = re.sub(r'_SIGNALNUM$', '', row.iloc[2])
                ConditionString += f"self.current_state['{row.iloc[0]}'] <= self.current_state['{ThresholdSignal}']:\n"
                ConditionString += f"            self.{row.iloc[5]} = 1\n"
        elif row.iloc[1] == 'CHANGE':
            ConditionString += f"self.current_state['{row.iloc[0]}'] != self.previous_state['{row.iloc[0]}']:\n"
            ConditionString += f'            self.{row.iloc[5]} = 1\n'
        elif row.iloc[1] == 'CHANGETO':
            if row.iloc[3] == 'CONDITION_TYPE_NUMBER':
                ConditionString += f"self.current_state['{row.iloc[0]}'] != self.previous_state['{row.iloc[0]}'] and self.current_state['{row.iloc[0]}'] == {row.iloc[2]}:\n"
                ConditionString += f'            self.{row.iloc[5]} = 1\n'
            else:
                ThresholdSignal = re.sub(r'_SIGNALNUM$', '', row.iloc[2])
                ConditionString += f"self.current_state['{row.iloc[0]}] != self.previous_state['{row.iloc[0]}'] and self.current_state['{row.iloc[0]}'] == self.current_state['{ThresholdSignal}']:\n"
                ConditionString += f"        self.{row.iloc[5]} = 1\n"
    RequirementVerifierFile.write(ConditionString)
    RequirementVerifierFile.write('\n')

    # 增加是否有TIMEFLAGNUM的判断
    AddTimeString = ''
    for i, row in EventDataFrame.iterrows():
        if (pd.notna(row.iloc[1]) and re.search('addTimer', row.iloc[1]) is not None) or (
                pd.notna(row.iloc[2]) and re.search('addTimer', str(row.iloc[2])) is not None):
            row_value = row.iloc[0]
            ConditionList = ConditionDataFrame[
                ConditionDataFrame.iloc[:, 4].astype(str) == str(row_value)].index.tolist()
            AddTimeString += f'        if('
            for j in range(len(ConditionList)):
                AddTimeString += f"(self.{ConditionDataFrame.iloc[ConditionList[j], 5]} == 1)"
                if j != len(ConditionList) - 1:
                    AddTimeString += ' or '
            AddTimeString += f') '
            if pd.notna(row.iloc[3]):
                AddTimeString += 'and ('
                for k in range(3, len(row)):
                    if pd.notna(row.iloc[k]):
                        AddTimeString += f"(self.{row.iloc[k]} == 1)"
                        if k != len(row) - 1 and pd.notna(row.iloc[k + 1]):
                            AddTimeString += 'and '
                AddTimeString += '):\n '
                AddTimeString += f'            self.current_state["TIMEFLAGNUM"] += 1\n'
    AddTimeString += '        if self.current_state["TIMEFLAGNUM"] == 0:\n            self.TIMEFLAGNUM_EQ_0 = 1 \n'
    RequirementVerifierFile.write(AddTimeString)

    ActionConflictString = ''
    ActionGroup = None
    for i, row in ActionDataFrame.iterrows():
        if pd.notna(row.iloc[0]) and ActionGroup == row.iloc[0]:
            ActionName = re.sub(r"\(\)$", "", row.iloc[1])
            ActionConflictString += f' and Action{int(row.iloc[0])}.{ActionName} in actions'
        if pd.notna(row.iloc[0]) and ActionGroup is None:
            ActionName = re.sub(r"\(\)$", "", row.iloc[1])
            ActionGroup = row.iloc[0]
            ActionConflictString += f'(Action{int(row.iloc[0])}.{ActionName} in actions'
        if pd.notna(row.iloc[0]) and ActionGroup != row.iloc[0]:
            ActionName = re.sub(r"\(\)$", "", row.iloc[1])
            ActionGroup = row.iloc[0]
            ActionConflictString += f') or (Action{int(row.iloc[0])}.{ActionName} in actions'
    ActionConflictString += ')\n'

    SignalInitString = ''.join(map(str, (lambda: ["0, " for _ in range(SignalNumber - 1)] + [0])()))
    RequirementVerifierFile.write(f'''

    def update_state(self,{SignalString}):
        self.previous_state = self.current_state.copy()
        self.current_state = {{{StateString}}}

{ConditionMacroString}

{ConditionString}

{AddTimeString}
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
        self.device_state = State({SignalInitString})

    def detect_and_execute(self,data_tuple):
        ({SignalString}) = data_tuple
        self.device_state.update_state({SignalString})
        applied_actions = self._get_applied_actions()
        ResultDict = self.device_state.current_state.copy()
        if not applied_actions:
            ResultDict['Result'] = '无规则适用'
        else:
            if self._has_conflict(applied_actions):
                ErrorDict = {{}}
                for key, value in self.device_state.current_state.items():
                    ErrorDict[f'{{key}}'] = value
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
        actions = {{action for action, _ in applied_actions}}
        return {ActionConflictString}
        ''')

    EventFunctionString = ''
    rowlen = EventDataFrame.shape[1]
    for i, row in EventDataFrame.iterrows():
        TimerCount = 0
        if pd.notna(row.iloc[1]) and re.search('Timer', str(row.iloc[1])) is not None:
            TimerCount += 1
        if pd.notna(row.iloc[2]) and re.search('Timer', str(row.iloc[2])) is not None:
            TimerCount += 1
        if (TimerCount <= 1 and pd.notna(row.iloc[1]) and pd.notna(row.iloc[2])) or (TimerCount == 0):
            EventFunctionString += f'\ndef Event_{row.iloc[0]}(device_state):\n    return('
            for j in range(3, rowlen):
                if pd.notna(row.iloc[j]) and row.iloc[j] != 'AND':
                    EventFunctionString += (
                            ('' if j == 3 else ' and\n           ') + f'(device_state.{row.iloc[j]} == 1)')
            EventFunctionString += ')\n'
    RequirementVerifierFile.write(EventFunctionString)

    # rules_list
    RuleString = ''
    ConflictActionList = []
    ActionGroup = None
    for i, row in ActionDataFrame.iterrows():
        if pd.notna(row.iloc[0]) and ActionGroup == row.iloc[0]:
            ActionName = re.sub(r"\(\)$", "", row.iloc[1])
            ConflictActionList[ActionGroup].append(ActionName)
        if pd.notna(row.iloc[0]) and ActionGroup is None:
            ActionGroup = int(row.iloc[0])
            ActionName = re.sub(r"\(\)$", "", row.iloc[1])
            ConflictActionList.append([ActionName])
        if pd.notna(row.iloc[0]) and ActionGroup != row.iloc[0]:
            ActionGroup = int(row.iloc[0])
            ActionName = re.sub(r"\(\)$", "", row.iloc[1])
            ConflictActionList.append([ActionName])

    Priority = 0
    for i, row in EventDataFrame.iterrows():
        Action1 = re.sub(r"\(\)$", "", str(row.iloc[1]))
        Action2 = re.sub(r"\(\)$", "", str(row.iloc[2]))
        for j, List in enumerate(ConflictActionList):
            if Action1 in List:
                RuleString += f'    ComplexRule(condition=Event_{row.iloc[0]},action=Action{j}.{Action1},priority={Priority}),\n'
                Priority += 1
            if Action2 in List:
                RuleString += f'    ComplexRule(condition=Event_{row.iloc[0]},action=Action{j}.{Action2},priority={Priority}),\n'
                Priority += 1

    RequirementVerifierFile.write(f'''
rules = [
{RuleString}
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
''')
    RequirementVerifierFile.close()
    print("requirement_verifier.py generated successfully.")
    print("Press any key to continue...")
    input()


if __name__ == '__main__':
    main()
