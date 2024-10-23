import pandas as pd
import re

df = pd.read_excel('config.xlsx', sheet_name=7)
for i in range(len(df)):
    print('#define ' + df.iloc[i, 0] + ' {', end='')
    for j in range(1, df.iloc[i].shape[0]):
        if not pd.isna(df.iloc[i, j]):
            print(df.iloc[i, j] + '; ', end='')
    print('}')



