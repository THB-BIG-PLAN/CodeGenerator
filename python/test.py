import pandas as pd
import Exception


def main():
    InitDataFrame = pd.read_excel('config.xlsx', sheet_name='Init')
    InitString = ''
    for index, row in InitDataFrame.iterrows():
        if pd.isna(row.loc['Type']) or row.loc['Type'] == '':
            raise Exception.EmptyTypeError(index)
        if pd.isna(row.loc['Value']) or row.loc['Value'] == '':
            raise Exception.EmptyValueError(index)
        InitString += f"    Set_{row.loc['Type']}_{row.loc['SignalName']}({row.loc['Value']})\n"
    print(InitString)


if __name__ == '__main__':
    main()
