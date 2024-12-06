import pandas as pd
import warnings
import itertools

# 忽略警告
warnings.simplefilter(action='ignore', category=UserWarning)

CONFIG_PATH = 'ConfigByHand.xlsx'


def read_data(config_path, sheet_index):
    """读取Excel数据"""
    return pd.read_excel(config_path, sheet_name=sheet_index)


def extract_signal_names(df):
    """提取信号名称"""
    Signal_Name_list = []
    for i, row in df.iterrows():
        if i == 0:
            Signal_Name_list.append(row.iloc[0])
        elif df.iloc[i - 1, 0] != df.iloc[i, 0]:
            Signal_Name_list.append(df.iloc[i, 0])
    return Signal_Name_list


def extract_signals(df):
    """提取信号集"""
    Signal_list = []
    Current_SignalSet = set()

    for i, row in df.iterrows():
        if i == 0:
            Current_SignalSet = set()
        else:
            if df.iloc[i - 1, 0] != df.iloc[i, 0]:
                Signal_list.append(Current_SignalSet)
                Current_SignalSet = set()
        if row.iloc[2] == 0:  # 阈值为0就取0，1
            Current_SignalSet.update({0, 1})
        elif row.iloc[2] == '0xff':  # 阈值为255就取254，255
            Current_SignalSet.update({254, 255})
        else:  # 阈值大于0小于255就取阈值的左右边界
            if str(row.iloc[2]).isdigit():
                Current_SignalSet.update({row.iloc[2] - 1, row.iloc[2], row.iloc[2] + 1})

    Signal_list.append(Current_SignalSet)
    return Signal_list


def compute_cartesian_product(signal_list):
    """计算笛卡尔积"""
    return list(itertools.product(*signal_list))


def save_to_excel(answer_list, signal_name_list, file_name, sheet_name):
    """保存结果到Excel"""
    df = pd.DataFrame(answer_list, columns=signal_name_list)
    df.to_excel(file_name, sheet_name=sheet_name, index=False)
    print("Cartesian Product saved to Excel successfully!")
    print("Press Enter to Continue...")
    input()


def main():
    df = read_data(CONFIG_PATH, 2)
    signal_name_list = extract_signal_names(df)
    signal_list = extract_signals(df)
    answer_list = compute_cartesian_product(signal_list)
    save_to_excel(answer_list, signal_name_list, "CartesianProduct.xlsx", "CartesianProduct")


if __name__ == '__main__':
    main()
