import pandas as pd

# 示例DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [5, 6, 7, 8]
})

# 查找列A中值为3的行
result = df[df.iloc[:, 0] == 3].index.tolist()

print(result)