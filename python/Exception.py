import pandas as pd


class EmptyTypeError(Exception):
    def __init__(self, row_index, SheetName):
        self.row_index = row_index
        super().__init__(f"Row {row_index} has empty type in sheet {SheetName}.")


class EmptyValueError(Exception):
    def __init__(self, row_index):
        self.row_index = row_index
        super().__init__(f"Row {row_index} has empty values.")
