import re
import pandas as pd

SignalDataFrame = pd.read_excel('Config.xlsx', sheet_name='InputSignal')
ConditionDataFrame = pd.read_excel('Config.xlsx', sheet_name='Condition')
not_in_condition = SignalDataFrame[~SignalDataFrame['SignalName'].isin(ConditionDataFrame['SignalName'])]
print(not_in_condition)