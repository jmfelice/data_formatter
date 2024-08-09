import pandas as pd
from src.data_formatter.validate import *
from typing import List, Tuple, Union


def find_columns(df: pd.DataFrame, column_name: str, lvl: Optional[int] = None) -> List[Union[str, Tuple]]:
    """
    Find columns in a DataFrame that match a given name.

    Args:
        df (pandas.DataFrame): The DataFrame to search.
        column_name (str): The name to search for.
        lvl (Optional[int]): The level in the MultiIndex to search. If None, search all levels.

    Returns:
        List[Union[str, Tuple]]: A list of column names or tuples that match the criteria.
    """
    # validate
    validate_dataframe_not_empty(df)
    validate_value_is_string(column_name)

    if isinstance(df.columns, pd.MultiIndex):
        if lvl is None:
            return [col for col in df.columns if column_name in col]
        else:
            return [col for col in df.columns if col[lvl] == column_name]
    else:
        return [col for col in df.columns if col == column_name]


def find_rows(df, row_name: str, lvl = None):
    return find_columns(df.T, row_name, lvl)


def find_column_positions(df: pd.DataFrame, column_name: str, lvl: Optional[int] = None) -> List[int]:
    """
    Find the positions of columns in a DataFrame that match a given column name.

    This function works with both single-level and MultiIndex DataFrames.

    Args:
        df (pandas.DataFrame): The DataFrame to search within.
        column_name (str): The name of the columns to find.
        lvl (Optional[int]): The level of the columns to consider if the DataFrame
                             has a MultiIndex. Defaults to None.

    Returns:
        List[int]: A list of positions (indices) of columns that match the criteria.

    Raises:
        ValueError: If the DataFrame is empty.
        TypeError: If the column name is not a string.
    """
    # Validate inputs
    validate_dataframe_not_empty(df)
    validate_value_is_string(column_name)

    # Use the find_columns function to get the list of requested columns
    requested_cols = find_columns(df, column_name, lvl)

    # Convert all columns to a list for easy enumeration
    all_cols = df.columns.tolist()

    # Initialize a list to store the positions of the requested columns
    positions = [i for i, col in enumerate(all_cols) if col in requested_cols]

    return positions


def find_row_positions(df, row_name: str, lvl = None):
    return find_column_positions(df.T, row_name, lvl)


def find_columns_like(df, substrings: str, lvl=None):
    """
    Find columns in a DataFrame that contain the given substring(s).

    Args:
        df (pandas.DataFrame): The DataFrame to search.
        substrings (str or list): A substring or a list of substrings to search for in column names.
        lvl (int or None, optional): The level of the MultiIndex to search. If None, search all levels.

    Returns:
        list: A list of column names (tuples) that contain the substring(s).
    """
    # validate
    validate_dataframe_not_empty(df)
    validate_value_is_string(substrings)

    # Ensure substrings is a list for consistent processing
    if isinstance(substrings, str):
        substrings = [substrings]

    # Initialize a list to store columns that match the substrings
    all_cols = []

    # Iterate over each column in the DataFrame
    for col in df.columns:
        # Check if the column is a tuple (MultiIndex)
        if isinstance(col, tuple):
            # Join the tuple levels into a single string and check for substrings
            if any(substring in ''.join(str(level) for level in col) for substring in substrings):
                all_cols.append(col)
        else:
            # Check for substrings in a single-level column
            if any(substring in str(col) for substring in substrings):
                all_cols.append(col)

    # If a specific level is provided, filter columns based on that level
    if lvl is not None:
        lvls = df.columns.get_level_values(lvl)
        in_lvls = [any(substring in str(x) for substring in substrings) for x in lvls]
        specific_cols = [col for col, match in zip(df.columns, in_lvls) if match]
        return specific_cols

    return all_cols


def find_rows_like(df, substrings: str, lvl = None):
    return find_columns_like(df = df.T, substrings = substrings, lvl = lvl)


def find_common_columns(df, *column_strings):
    """
    Identify common columns in a multi-index DataFrame where specified strings appear at the highest level.

    This function searches for columns in a multi-index DataFrame where the highest level of the column index
    contains all specified strings. It returns a list of tuples, each representing a column multi-index where
    these conditions are met.

    Args:
        df (pandas.DataFrame): The input DataFrame with a multi-index for columns. The function assumes that
                               the DataFrame's columns are structured as a multi-index.
        *column_strings (str): One or more strings to search for in the highest level of the column multi-index.
                               Each string provided must be present in the highest level of the column index
                               for the columns to be considered common.

    Returns:
        list: A list of tuples, where each tuple represents the multi-index of a column that satisfies the
              specified conditions. Each tuple corresponds to a column in the DataFrame where all the given
              strings are found at the highest level of the column index.

    Example:
        Suppose you have a DataFrame `df` with a multi-index for columns structured as follows:

        | ('A', 'x') | ('A', 'y') | ('B', 'x') | ('B', 'y') |
        |------------|------------|------------|------------|
        |    ...     |    ...     |    ...     |    ...     |

        Calling `find_common_columns(df, 'x', 'y')` will return:
        [('A', 'x'), ('A', 'y'), ('B', 'x'), ('B', 'y')]

    Note:
        - The function only works with DataFrames that have a multi-index for columns.
        - The strings provided in `column_strings` must be present in the highest level of the column index.
        - The function groups columns by their lower levels and checks if all specified strings are present
          in the highest level for each group of columns.
    """
    # Validate the DataFrame
    validate_dataframe_not_empty(df)
    validate_columns_multiindex(df)

    # Validate each column string
    for string in column_strings:
        validate_value_is_string(string)

    # Get the multi-index column names as a flat index
    column_names = df.columns.to_flat_index()

    # Define a filter function to check if a column contains any of the given strings at the highest level
    def filter_by(x):
        return any(string == x[-1] or str(string) in str(x[-1]) for string in column_strings)

    # Filter columns that match the criteria
    filtered_columns = list(filter(filter_by, column_names))

    # Group columns by their lower levels (all levels except the last one)
    grouped_columns = {}
    for col in filtered_columns:
        lower_levels = col[:-1]
        grouped_columns.setdefault(lower_levels, []).append(col)

    # Find common columns where all strings are present for each combination of lower levels
    common_columns = []
    for lower_levels, columns in grouped_columns.items():
        # Check if all column strings are present in the highest level for each group
        column_sets = [set(col[-1] for col in columns)]
        if all(set(column_strings).issubset(col_set) for col_set in column_sets):
            common_columns.extend(columns)

    return common_columns
