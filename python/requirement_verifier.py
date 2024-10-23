import re

import pandas as pd
import openpyxl
import warnings
from enum import Enum


class Action(Enum):
    LGL_ON = 1
    LGL_OFF = 2


# 忽略警告
warnings.simplefilter(action='ignore', category=UserWarning)

pd.read_excel('config.xlsx', sheet_name=2)
