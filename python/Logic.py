import pandas as pd
import re
import warnings
import Exception

warnings.simplefilter(action='ignore', category=UserWarning)
CONFIG_PATH = 'Config.xlsx'
LOGIC_HEADER_PATH = 'Logic.h'
LOGIC_SOURCE_PATH = 'Logic.c'
InputSignal_DataFrame = pd.read_excel(CONFIG_PATH, sheet_name='InputSignal')
OutputInitializer_DataFrame = pd.read_excel(CONFIG_PATH, sheet_name='OutputInitializer')



def main():
    pass


if __name__ == '__main__':
    main()
