import pandas as pd
import re
import warnings
import itertools

# 忽略警告
warnings.simplefilter(action='ignore', category=UserWarning)

CONFIG_PATH = '../config.xlsx'

# 读取数据
df = pd.read_excel(CONFIG_PATH, sheet_name=2)
Signal_list = []
Signal_Name_list = []
Current_SignalSet = set()

for i, row in df.iterrows():
    if i == 0:
        Signal_Name_list.append(row.iloc[0])
    elif df.iloc[i - 1, 0] != df.iloc[i, 0]:
        Signal_Name_list.append(df.iloc[i, 0])
print(Signal_Name_list)

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
        Current_SignalSet.update({row.iloc[2] - 1, row.iloc[2], row.iloc[2] + 1})
Signal_list.append(Current_SignalSet)
print(Signal_list)


# 笛卡尔积
answer_list = list(itertools.product(*Signal_list))

# 输出结果
