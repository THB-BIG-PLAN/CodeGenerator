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


def main():
    WriteInputSignalToExcel()


if __name__ == "__main__":
    main()
