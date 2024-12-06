import pandas as pd
from pandas.api.types import CategoricalDtype

List_df = pd.read_excel('ConfigByHand.xlsx',sheet_name='List')
df_order = []
InputSignal_df = pd.read_excel('ConfigByHand.xlsx',sheet_name='InputSignal')
for i,row in List_df.iterrows():
    if pd.notna(row.loc['VariableType']):
        df_order.append(row.loc['VariableType'])
InputSignal_df['Type'] = InputSignal_df['Type'].astype(CategoricalDtype(categories=df_order, ordered=True))
InputSignal_df = InputSignal_df.sort_values(by=['Type'])
InputSignal_df = InputSignal_df.reset_index(drop=True)
print(InputSignal_df)