import pandas as pd


class my_class:
    def __init__(self,num1,num2,num3,num4,num5,num6,num7,num8,num9):
        self.num1 = num1
        self.num2 = num2
        self.num3 = num3
        self.num4 = num4
        self.num5 = num5
        self.num6 = num6
        self.num7 = num7
        self.num8 = num8
        self.num9 = num9
    def __print__(self):
        print(self.num1,self.num2,self.num3,self.num4,self.num5,self.num6,self.num7,self.num8,self.num9)
ENVIRONMENT_FILE = 'CartesianProduct.xlsx'
BATCH_SIZE = 100
skip_rows = 0
times = 0
while times != 2:
    try:
        EnvironmentDataFrame = pd.read_excel(ENVIRONMENT_FILE, sheet_name=0, nrows=BATCH_SIZE, skiprows=skip_rows)
        if EnvironmentDataFrame.empty:
            break
        DataList = EnvironmentDataFrame.values.tolist()
        for List in DataList:
            my_class(List[0],List[1],List[2],List[3],List[4],List[5],List[6],List[7],List[8]).__print__()
        skip_rows += BATCH_SIZE
        times += 1
    except FileNotFoundError:
        print("文件不存在")
        break


