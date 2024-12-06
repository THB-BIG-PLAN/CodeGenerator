import os
import warnings

import pandas as pd
import openpyxl
import re

warnings.simplefilter(action='ignore', category=UserWarning)
HAND_CONFIG_PATH = "ConfigByHand.xlsx"
InputSignal_DataFrame = pd.read_excel(HAND_CONFIG_PATH, sheet_name="InputSignal")
CONFIG_PATH = "Config.xlsx"
List_DataFrame = pd.read_excel(HAND_CONFIG_PATH, sheet_name="List")
Condition_DataFrame = pd.read_excel(HAND_CONFIG_PATH, sheet_name="Condition")
EVT_DataFrame = pd.read_excel(HAND_CONFIG_PATH, sheet_name="EVT")
TimeFlag_DataFrame = pd.read_excel(HAND_CONFIG_PATH, sheet_name="TimeFlag")
ConstMacro_DataFrame = pd.read_excel(HAND_CONFIG_PATH, sheet_name="ConstMacro")
OutputInitializer_DataFrame = pd.read_excel(HAND_CONFIG_PATH, sheet_name="OutputInitializer")
Action_DataFrame = pd.read_excel(HAND_CONFIG_PATH, sheet_name="Action")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def WriteInputSignalToExcel():
    NewSignal_DataFrame = InputSignal_DataFrame.copy()
    new_rows = []
    for i, row in InputSignal_DataFrame.iterrows():
        SignalPre_Name = row.loc['SignalName'] + "_Pre"
        new_rows.append({'SignalName': SignalPre_Name, 'Type': row.loc['Type']})
    NewSignal_DataFrame = pd.concat([NewSignal_DataFrame, pd.DataFrame(new_rows)], ignore_index=True)
    NewSignal_DataFrame['Macro'] = NewSignal_DataFrame['SignalName'] + '_SIGNALNUM'
    # order by Type
    NewSignal_DataFrame = NewSignal_DataFrame.sort_values(by=['Type', 'SignalName'])
    NewSignal_DataFrame.reset_index(drop=True, inplace=True)
    # write to excel
    if not os.path.exists(CONFIG_PATH):
        NewSignal_DataFrame.to_excel(CONFIG_PATH, sheet_name='InputSignal', index=False)
    else:
        with pd.ExcelWriter(CONFIG_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            NewSignal_DataFrame.to_excel(writer, sheet_name='InputSignal', index=False)


def WriteConditionToExcel():
    NewRowList = []
    NewRow = {}
    NewCondition_DataFrame = pd.DataFrame(
        columns=['SignalName', 'Symbol', 'Threshold', 'ThresholdType', 'EVT', 'Macro'])
    for i, row in Condition_DataFrame.iterrows():
        Signal_Name = row.loc['SignalName']
        if row.loc['Symbol'] == 'CHANGE':
            pattern = r'\((.*),(.*)\)'
            match = re.match(pattern, row.loc['Threshold'])
            a = match.group(1)
            b = match.group(2)
            if a == 'x' and b == 'x':
                NewRow = {
                    'SignalName': Signal_Name,
                    'Symbol': row.loc['Symbol'],
                    'Threshold': Signal_Name + '_Pre_SIGNALNUM',
                    'ThresholdType': 'CONDITION_TYPE_SIGNAL',
                    'EVT': row.loc['EVT'],
                    'Macro': Signal_Name.upper() + '_CHANGE_' + Signal_Name + '_PRE_SIGNALNUM'
                }
                NewRowList.append(NewRow)
            elif a != 'x' and b == 'x':
                NewRow = {
                    'SignalName': Signal_Name,
                    'Symbol': row.loc['Symbol'],
                    'Threshold': Signal_Name + '_Pre_SIGNALNUM',
                    'ThresholdType': 'CONDITION_TYPE_SIGNAL',
                    'EVT': row.loc['EVT'],
                    'Macro': Signal_Name.upper() + '_CHANGE_' + Signal_Name + '_PRE_SIGNALNUM'
                }
                NewRowList.append(NewRow)
                NewRow = {
                    'SignalName': Signal_Name + '_Pre',
                    'Symbol': 'EQ',
                    'Threshold': a,
                    'ThresholdType': 'CONDITION_TYPE_NUMBER',
                    'EVT': row.loc['EVT'],
                    'Macro': Signal_Name.upper() + '_PRE_EQ_' + a
                }
                NewRowList.append(NewRow)
            elif a == 'x' and b != 'x':
                NewRow = {
                    'SignalName': Signal_Name,
                    'Symbol': row.loc['Symbol'],
                    'Threshold': Signal_Name + '_Pre_SIGNALNUM',
                    'ThresholdType': 'CONDITION_TYPE_SIGNAL',
                    'EVT': row.loc['EVT'],
                    'Macro': Signal_Name.upper() + '_CHANGE_' + Signal_Name + '_PRE_SIGNALNUM'
                }
                NewRowList.append(NewRow)
                NewRow = {
                    'SignalName': Signal_Name,
                    'Symbol': 'EQ',
                    'Threshold': b,
                    'ThresholdType': 'CONDITION_TYPE_NUMBER',
                    'EVT': row.loc['EVT'],
                    'Macro': Signal_Name.upper() + '_EQ_' + b
                }
                NewRowList.append(NewRow)
            elif a != 'x' and b != 'x':

                NewRow = {
                    'SignalName': Signal_Name + '_Pre',
                    'Symbol': 'EQ',
                    'Threshold': a,
                    'ThresholdType': 'CONDITION_TYPE_NUMBER',
                    'EVT': row.loc['EVT'],
                    'Macro': Signal_Name.upper() + '_PRE_EQ_' + a
                }
                NewRowList.append(NewRow)
                NewRow = {
                    'SignalName': Signal_Name,
                    'Symbol': 'EQ',
                    'Threshold': b,
                    'ThresholdType': 'CONDITION_TYPE_NUMBER',
                    'EVT': row.loc['EVT'],
                    'Macro': Signal_Name.upper() + '_EQ_' + b
                }
                NewRowList.append(NewRow)
        else:
            if row.loc['ThresholdType'] == 'CONDITION_TYPE_SIGNAL':
                NewRow = {
                    'SignalName': Signal_Name,
                    'Symbol': row.loc['Symbol'],
                    'Threshold': row.loc['Threshold'] + '_SIGNALNUM',
                    'ThresholdType': row.loc['ThresholdType'],
                    'EVT': row.loc['EVT'],
                    'Macro': row.loc['Macro']
                }
            else:
                NewRow = {
                    'SignalName': Signal_Name,
                    'Symbol': row.loc['Symbol'],
                    'Threshold': row.loc['Threshold'],
                    'ThresholdType': row.loc['ThresholdType'],
                    'EVT': row.loc['EVT'],
                    'Macro': row.loc['Macro']
                }
            NewRowList.append(NewRow)
    NewCondition_DataFrame = pd.concat([NewCondition_DataFrame, pd.DataFrame(NewRowList)], ignore_index=True)
    # order by SignalName
    NewCondition_DataFrame = NewCondition_DataFrame.sort_values(by=['SignalName'])
    NewCondition_DataFrame.reset_index(drop=True, inplace=True)
    # write to excel
    if not os.path.exists(CONFIG_PATH):
        NewCondition_DataFrame.to_excel(CONFIG_PATH, sheet_name='Condition', index=False)
    else:
        with pd.ExcelWriter(CONFIG_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            NewCondition_DataFrame.to_excel(writer, sheet_name='Condition', index=False)


def WriteEVTToExcel():
    NewRowList = []
    NewRow = {}
    NewEVT_DataFrame = pd.DataFrame(
        columns=['EVTName', 'Action1', 'Action2', 'Description', 'Condition1',
                 'Condition2', 'Condition3', 'Condition4', 'Condition5', 'Condition6', 'Condition7', 'Condition8'])
    for i, row in EVT_DataFrame.iterrows():
        NewRow = {}
        ConditionNum = 0
        for j, col in enumerate(row):
            if j <= 2:
                NewRow[row.index[j]] = col
                continue
            if pd.notna(col) and col != 'AND':
                ConditionNum += 1
                col = str(col)
                pattern = r'^.*CHANGE.*\(([^)]+),([^)]+)\).*$'
                match = re.match(pattern, col)
                if match:
                    print("'CHANGE'")
                    print("a", match.group(1))
                    print("b", match.group(2))
                else:
                    NewRow[row.index[j]] = col
        print(NewRow)


# def WriteTimeFlagToExcel():
#
#
# def WriteConstMacroToExcel():
#
#
# def WriteOutputInitializerToExcel():
#
#
# def WriteActionToExcel():
#
#
# def WriteListToExcel():
def main():
    # WriteInputSignalToExcel()
    # WriteConditionToExcel()
    WriteEVTToExcel()
    # WriteTimeFlagToExcel()
    # WriteConstMacroToExcel()
    # WriteOutputInitializerToExcel()
    # WriteActionToExcel()
    # WriteListToExcel()


if __name__ == "__main__":
    main()
