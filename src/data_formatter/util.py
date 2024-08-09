from itertools import repeat
import pandas as pd
from typing import List, Union
from src.data_formatter.validate import *


def get_even_numbers(x):
    df_row_count = list(range(0, len(x)))
    return [num for num in df_row_count if num % 2 == 0]


def replace_list_element(lst, old, new):
    """
    Returns a list where elements at specified indices are kept,
    and other elements are replaced with 'Total *', where * is the original value.

    Parameters:
    lst (list): The original list from which to extract elements.
    indices (list of int): The indices of elements to extract.

    Returns:
    list: A list with elements at specified indices kept and others replaced with 'Total *'.
    """
    result = [new if x == old else x for x in lst]
    return result


def proper_case(obj):
    """
    Converts strings to uppercase in the given object.
    If the object is a string, it converts it to uppercase.
    If the object is a list or an object with a length greater than 1,
    it recursively iterates through its elements and converts strings to uppercase.
    """
    if isinstance(obj, str):
        return obj.replace('_', ' ').title()
    elif hasattr(obj, '__iter__') and len(obj) > 1:
        return [proper_case(item) for item in obj]
    else:
        return obj


def sort_dataframe_by_custom_order(
    df: pd.DataFrame,
    desired_order: List[Union[str, int]],
    axis: int = 0,
    level: int = 0
) -> pd.DataFrame:
    """
    Sort a DataFrame based on a custom order for a specified index or column level,
    while preserving the order of the lower levels.

    This function sorts the DataFrame by rearranging the specified axis (rows or columns)
    according to a given sequence for a particular level of a MultiIndex. The order of
    the lower levels is preserved.

    Args:
        df (pandas.DataFrame): The DataFrame to sort.
        desired_order (List[Union[str, int]]): The desired order for the specified level.
        axis (int): The axis to sort (0 for index, 1 for columns). Defaults to 0.
        level (int): The level of the MultiIndex to sort by. Defaults to 0.

    Returns:
        pd.DataFrame: The sorted DataFrame.

    Raises:
        ValueError: If any element in desired_order is not found in the specified level.

    Example:
        If a DataFrame has columns [('One', 'A', 1), ('One', 'A', 2), ('Two', 'B', 1)]
        and you supply an order of ['Two', 'One'] for axis=1, level=0,
        the columns will be reordered to [('Two', 'B', 1), ('One', 'A', 1), ('One', 'A', 2)].
    """
    def sort_key(index):
        # Create a key based on the desired order for the specified level
        level_key = desired_order.index(index[level]) if index[level] in desired_order else len(desired_order)
        # Create a tuple that maintains the order of all preceding levels
        return tuple(list(index[:level]) + [level_key] + list(index[level + 1:]))

    # Extract the MultiIndex
    idx = df.columns if axis == 1 else df.index

    # Validate that all elements in desired_order are present in the specified level
    level_values = idx.get_level_values(level)
    for item in desired_order:
        if item not in level_values:
            raise ValueError(f"'{item}' not found in level {level} of the {'columns' if axis == 1 else 'index'}.")

    # Sort the index using the custom sort key
    sorted_idx = sorted(idx, key=sort_key)

    # Reindex the DataFrame based on the sorted index
    if axis == 1:
        df = df.loc[:, sorted_idx]
    else:
        df = df.loc[sorted_idx]

    return df


def table_level_values(df, axis = 0, level = 0, unique = True):
    if axis == 1:
        res = df.columns.get_level_values(level)
    else:
        res = df.index.get_level_values(level)

    if unique:
        return list(res.unique())
    else:
        return list(res)


def only_one(iterable):
    i = iter(iterable)
    return any(i) and not any(i)


def not_in(x, lst):
    if isinstance(x, str):
        # return list(set(lst) - set([x]))
        return list(set(lst) - {x})
    elif hasattr(x, '__iter__') and len(x) > 1:
        return list(set(lst) - set(x))
    else:
        return x


def row_count(df):
    return len(df.index)


def column_count(df):
    return len(df.columns)


def column_level_count(df):
    return len(df.columns.names)


def row_level_count(df):
    return len(df.index.names)


def unique_string(string, string_list):
    if string not in string_list:
        return string

    counter = 1
    while True:
        new_string = f"{string}_{counter}"
        if new_string not in string_list:
            return new_string
        counter += 1


def index_to_dict(x):
    return {key: x.get_level_values(i) for i, key in enumerate(x.names)}


def repeat_c(obj, times):
    result = [x for x in list(repeat(obj, times))]
    return f"{''.join(result)}"


def move_df_level_to_front(
    df: pd.DataFrame,
    level_to_move: Union[str, None],
    axis: int = 0
) -> pd.DataFrame:
    """
    Move a specified level to the front of a MultiIndex in a DataFrame.

    This function rearranges the levels of a MultiIndex in either the index or columns
    of a DataFrame, placing the specified level first.

    Args:
        df (pd.DataFrame): The input DataFrame with a MultiIndex.
        level_to_move (Union[str, None]): The name of the level to move to the front.
        axis (int): The axis to modify (0 for index, 1 for columns). Defaults to 0.

    Returns:
        pd.DataFrame: The DataFrame with the specified level moved to the front.

    Raises:
        ValueError: If the specified level is not found in the MultiIndex.

    Example:
        move_df_level_to_front(df, level_to_move='numbers', axis=0)
    """
    if axis == 0:
        current_order = list(df.index.names)
    else:
        current_order = list(df.columns.names)

    if level_to_move not in current_order:
        raise ValueError(f"The level '{level_to_move}' is not found in the MultiIndex.")

    # Create a new order with the specified level first
    new_order = [level_to_move] + [name for name in current_order if name != level_to_move]

    if axis == 0:
        df_reordered = df.reorder_levels(order=new_order, axis=0)
    else:
        df_reordered = df.reorder_levels(order=new_order, axis=1)

    return df_reordered
