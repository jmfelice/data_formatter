import unittest
import pandas as pd
from src.data_formatter.pivot_tables import pivot_to
from src.data_formatter.util import move_df_level_to_front

df = pd.DataFrame({
            'Year': [2020, 2020, 2021, 2021],
            'Region': ['North', 'South', 'North', 'South'],
            'Product': ['A', 'B', 'A', 'B'],
            'Sales': [100, 150, 200, 250],
            'Profit': [20, 30, 40, 50]
        })

result = pivot_to(df, values=['Profit', 'Sales'], columns=['Region'], title='Testing Data')


if __name__ == '__main__':

    print(
        df,
        result,
        result.index,
        result.columns,
        result.columns.names,


        sep = "\n\n"
    )
