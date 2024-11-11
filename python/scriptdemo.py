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
    if re.search('addTimer',row.iloc[1]) is not None or re.search('addTimer',row.iloc[2]) is not None:


