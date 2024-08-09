import pandas as pd
from typing import List, Optional, Union
from src.data_formatter.util import move_df_level_to_front


def pivot_to(
    df: pd.DataFrame,
    values: List[str],
    columns: List[str],
    title: Optional[str] = None,
    func: Union[str, List[str]] = 'sum',
    margins: bool = False,
    margins_name: str = 'Total'
) -> pd.DataFrame:
    """
    Pivot a DataFrame based on specified values and columns, automatically determining the index.

    Args:
        df (pd.DataFrame): The input DataFrame.
        values (List[str]): The column names to use as values in the pivot table.
        columns (List[str]): The column names to use as columns in the pivot table.
        title (Optional[str]): An optional title to add as a column in the DataFrame.
        func (Union[str, List[str]]): The aggregation function(s) to apply. Defaults to 'sum'.
        margins (bool): Whether to add margins (subtotals) to the pivot table. Defaults to False.
        margins_name (str): The name to use for the margins row/column. Defaults to 'Total'.

    Returns:
        pd.DataFrame: The pivoted DataFrame.

    Example:
        pivot_to(df, values=['Sales'], columns=['Region'], title='Year', func='sum')
    """
    if title is not None:
        df.insert(0, title, title)
        columns = [title] + columns

    data_index = [x for x in df.columns if x not in values and x not in columns]

    df_pivot = df.pivot_table(
        index=data_index,
        columns=columns,
        values=values,
        aggfunc=func,
        fill_value=0,
        margins=margins,
        margins_name=margins_name,
        sort=False
    )

    if title is not None:
        df_pivot = move_df_level_to_front(df_pivot, "Testing Data", axis = 1)
    return df_pivot


def pivot_to_standard_format(df, title = None):
    data_values = ['amount']
    data_cols = ['duration', 'annum']
    return pivot_to(df, data_values, data_cols, title = title)


def pivot_to_series_format(df, title = None):
    data_values = ['amount']
    data_cols = ['duration', 'period_ending']
    return pivot_to(df, data_values, data_cols, title = title)
