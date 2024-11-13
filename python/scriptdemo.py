import pandas as pd
from enum import Enum
import warnings
import re

warnings.simplefilter(action='ignore', category=UserWarning)

CONFIG_FILE = "config.xlsx"
WRITE_FILE = "requirement_verifier_test.py"
HEADER = '''
import pandas as pd
from enum import Enum
import warnings
import re

warnings.simplefilter(action='ignore', category=UserWarning)
'''

ActionDataFrame = pd.read_excel(CONFIG_FILE, sheet_name="Action")
RequirementVerifierFile = open(WRITE_FILE, "w")
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
SignalDataFrame = pd.read_excel(CONFIG_FILE, sheet_name=0)
rownum = 3
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

# 增加是否有TIMEFLAGNUM的判断
EventDataFrame = pd.read_excel(CONFIG_FILE, sheet_name=4)
ConditionDataFrame = pd.read_excel(CONFIG_FILE, sheet_name=2)
AddTimeString = ''
for i, row in EventDataFrame.iterrows():
    if (pd.notna(row.iloc[1]) and re.search('addTimer', row.iloc[1]) is not None) or (
            pd.notna(row.iloc[2]) and re.search('addTimer', str(row.iloc[2])) is not None):
        row_value = row.iloc[0]
        ConditionList = ConditionDataFrame[ConditionDataFrame.iloc[:, 3].astype(str) == str(row_value)].index.tolist()
        ConditionString = '        if(('
        for j in range(len(ConditionList)):
            ConditionSeries = ConditionDataFrame.iloc[ConditionList[j]]
            Symbol = ConditionSeries.iloc[1]
            ConditionString += f"(self.current_state['{ConditionSeries.iloc[0]}']"
            if Symbol == 'EQ':
                ConditionString += f" == {ConditionSeries.iloc[2]})"
            elif Symbol == 'NEQ':
                ConditionString += f"!= {ConditionSeries.iloc[2]})"
            elif Symbol == 'CHANGE':
                ConditionString += f"!= self.previous_state['{ConditionSeries.iloc[0]}'])"
            elif Symbol == 'CHANGETO':
                ConditionString += f"!= self.previous_state['{ConditionSeries.iloc[0]}']) and (self.current_state['{ConditionSeries.iloc[0]}'] == {ConditionSeries.iloc[2]})"
            elif Symbol == 'GREATER':
                ConditionString += f" > {ConditionSeries.iloc[2]})"
            elif Symbol == 'GREATEROREQ':
                ConditionString += f" >= {ConditionSeries.iloc[2]})"
            elif Symbol == 'LESS':
                ConditionString += f" < {ConditionSeries.iloc[2]})"
            elif Symbol == 'LESSOREQ':
                ConditionString += f" <= {ConditionSeries.iloc[2]})"
            if len(ConditionList) > 1 and j < len(ConditionList) - 1:
                ConditionString += 'or ('
        ConditionString += '))'
        if pd.notna(row.iloc[3]):
            ConditionString += ' and ('
        for j in range(3, row.shape[0]):
            if pd.notna(row.iloc[j]) and row.iloc[j] != 'AND':
                row_value = row.iloc[j]
                ConditionList = ConditionDataFrame[ConditionDataFrame.iloc[:, 4].astype(str) == str(row_value)].index.tolist()
                ConditionSeries = ConditionDataFrame.iloc[ConditionList[0]]
                Symbol = ConditionSeries.iloc[1]
                ConditionString += f"(self.current_state['{ConditionSeries.iloc[0]}']"
                if Symbol == 'EQ':
                    ConditionString += f" == {ConditionSeries.iloc[2]})"
                elif Symbol == 'NEQ':
                    ConditionString += f"!= {ConditionSeries.iloc[2]})"
                elif Symbol == 'CHANGE':
                    ConditionString += f"!= self.previous_state['{ConditionSeries.iloc[0]}'])"
                elif Symbol == 'CHANGETO':
                    ConditionString += f"!= self.previous_state['{ConditionSeries.iloc[0]}']) and (self.current_state['{ConditionSeries.iloc[0]}'] == {ConditionSeries.iloc[2]})"
                elif Symbol == 'GREATER':
                    ConditionString += f" > {ConditionSeries.iloc[2]})"
                elif Symbol == 'GREATEROREQ':
                    ConditionString += f" >= {ConditionSeries.iloc[2]})"
                elif Symbol == 'LESS':
                    ConditionString += f" < {ConditionSeries.iloc[2]})"
                elif Symbol == 'LESSOREQ':
                    ConditionString += f" <= {ConditionSeries.iloc[2]})"
        ConditionString += "):\n            self.current_state['TIMEFLAGNUM'] += 1\n"
        AddTimeString += ConditionString
RequirementVerifierFile.write(AddTimeString)
