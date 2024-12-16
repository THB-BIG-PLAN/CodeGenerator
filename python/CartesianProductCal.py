import numpy as np
import pandas as pd
import warnings
from itertools import product

# 忽略警告
warnings.simplefilter(action='ignore', category=UserWarning)

CONFIG_PATH = 'Config.xlsx'


def read_config():
    df = pd.read_excel(CONFIG_PATH, sheet_name='Condition')
    return df


def get_signal_name_list(df):
    signal_name_list = []
    SignalName = None
    for index, row in df.iterrows():
        if row.loc['SignalName'].endswith('Pre'):
            continue
        if SignalName is None:
            SignalName = row.loc['SignalName']
            signal_name_list.append(SignalName)
        if row.loc['SignalName'] != SignalName:
            signal_name_list.append(row.loc['SignalName'])
            SignalName = row.loc['SignalName']
        if index == len(df) - 1:
            signal_name_list.append(row.loc['SignalName'])

    # print(signal_name_list)
    return signal_name_list
    pass


def extract_signals(df):
    signal_list = []
    current_signal_set = set()
    for index, row in df.iterrows():
        if row.loc['SignalName'].endswith('Pre'):
            continue
        if index == 0:
            current_signal_set = set()
        else:
            if df.iloc[index - 1, 0] != df.iloc[index, 0]:
                signal_list.append(current_signal_set)
                current_signal_set = set()
        threshold_value = pd.to_numeric(row.loc['Threshold'], errors='coerce')
        if not np.isnan(threshold_value):
            if threshold_value == 0:
                current_signal_set.update({0, 1, 2})
            elif threshold_value == 0xff:
                current_signal_set.update({255, 254})
            else:
                current_signal_set.update({int(threshold_value - 1), int(threshold_value), int(threshold_value + 1)})
        elif not current_signal_set:
            current_signal_set.update({255, 254})
    signal_list.append(current_signal_set)
    print(signal_list)
    return signal_list
    pass


def compute_cartesian_product(signal_list):
    cartesian_product_result = list(product(*signal_list))
    return cartesian_product_result


def main():
    df = read_config()
    signal_name_list = get_signal_name_list(df)
    signal_list = extract_signals(df)
    answer_list = compute_cartesian_product(signal_list)
    df_answer = pd.DataFrame(answer_list, columns=signal_name_list)
    df_answer.to_excel('CartesianProduct.xlsx', index=False)
    pass


if __name__ == '__main__':
    main()
