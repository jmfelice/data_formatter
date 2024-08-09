import numpy as np
from .dataframe_find import find_common_columns


def add_calculated_column(df, func, *column_names, new_column_name = None):
    """
    Add a new column to the DataFrame by applying a function to one or more existing columns.

    Args:
        df (pandas.DataFrame): The input DataFrame.
        func (callable): The function to apply to the columns.
        *column_names (str): One or more column names to use as input for the function.
        new_column_name (str): Name of the new column.

    Returns:
        pandas.DataFrame: The modified DataFrame with the new column added.
    """
    # Get the actual column data from the DataFrame
    columns = [np.array(df[col_name]) for col_name in column_names]

    # Apply the function to the columns
    new_column = func(*columns)

    # Add the new column to the DataFrame
    if new_column_name is None:
        new_column_name = f"new_column_{len(df.columns)}"

    pos = max([df.columns.get_loc(x) for x in column_names]) + 1
    df.insert(pos, new_column_name, new_column)
    return df


def add_calculated_row(df, func, *row_names, new_row_name = None):
    x = add_calculated_column(df.T, func, *row_names, new_column_name = new_row_name)
    return x.T


def add_calculated_columns(df, func, *column_names, new_column_name = None):
    common_cols = find_common_columns(df, *column_names)
    common_cols = list(set([i[:-1] for i in common_cols]))

    for i in common_cols:
        x = []
        for col in column_names:
            x.append(i + (col,))

        df = add_calculated_column(df, func, *x, new_column_name = i + (new_column_name, ))

    return df


def add_calculated_rows(df, func, *row_names, new_row_name = None):
    df2 = df.T
    common_cols = find_common_columns(df2, *row_names)
    common_cols = list(set([i[:-1] for i in common_cols]))

    for i in common_cols:
        x = []
        for col in row_names:
            x.append(i + (col,))

        df = add_calculated_row(df, func, *x, new_row_name = i + (new_row_name, ))

    return df
