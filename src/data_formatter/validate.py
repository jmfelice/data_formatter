import pandas as pd
import numpy as np
from typing import Callable, Optional, Union, Tuple


def validate_dataframe_not_empty(df: pd.DataFrame) -> None:
    """Check if a DataFrame is not empty."""
    if df.empty:
        raise ValueError("The DataFrame is empty.")


def validate_column_exists(df: pd.DataFrame, column_name: str) -> None:
    """Check if a column exists in the DataFrame."""
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")


def validate_callable(func: Callable) -> None:
    """Check if the provided function is callable."""
    if not callable(func):
        raise TypeError("The provided function is not callable.")


def validate_columns_multiindex(df):
    """Check if the DataFrame's columns are a MultiIndex."""
    if not isinstance(df.columns, pd.MultiIndex):
        raise ValueError("The DataFrame's columns are not a MultiIndex.")
    return True


def validate_rows_multiindex(df):
    """Check if the DataFrame's rows (index) are a MultiIndex."""
    if not isinstance(df.index, pd.MultiIndex):
        raise ValueError("The DataFrame's rows (index) are not a MultiIndex.")
    return True


def validate_string_in_column_tuple(column_tuple, string):
    """Check if a string is in a column tuple."""
    if string not in column_tuple:
        raise ValueError(f"The string '{string}' is not in the column tuple {column_tuple}.")
    return True


def validate_string_in_any_column_tuple(columns: pd.Index, string: str) -> bool:
    """
    Check if a string is present in any of the column tuples of a DataFrame.

    Args:
        columns (pd.Index): The columns of the DataFrame, expected to be a MultiIndex.
        string (str): The string to search for in the column tuples.

    Returns:
        bool: True if the string is found in any of the column tuples, otherwise raises a ValueError.

    Raises:
        ValueError: If the string is not found in any of the column tuples.
    """
    for column_tuple in columns:
        if string in column_tuple:
            return True
    raise ValueError(f"The string '{string}' is not in any of the column tuples.")


def validate_value_is_string(value: str) -> None:
    """Check if a value is a string."""
    if not isinstance(value, str):
        raise TypeError(f"The value '{value}' is not a string.")


def validate_value_is_an_int(value):
    """Check if a value is a string."""
    if not isinstance(value, int):
        raise TypeError(f"The value '{value}' is not an integer.")
    return True


def validate_value_is_string_or_tuple(value: Union[str, Tuple]) -> None:
    """Check if a value is a string or a tuple."""
    if not isinstance(value, (str, tuple)):
        raise TypeError(f"The value '{value}' is not a string or a tuple.")

def validate_string_in_highest_level(column_tuple, string):
    """Check if a string is in the highest level of a column tuple."""
    if string != column_tuple[-1]:
        raise ValueError(f"The string '{string}' is not in the highest level of the column tuple {column_tuple}.")
    return True


def validate_string_in_specified_level(column_tuple, string, level):
    """Check if a string is in a specified level of a column tuple."""
    if level < 0 or level >= len(column_tuple):
        raise IndexError("Specified level is out of range for the column tuple.")
    if string != column_tuple[level]:
        raise ValueError(f"The string '{string}' is not in level {level} of the column tuple {column_tuple}.")
    return True


def validate_string_in_specified_level_row(row_tuple, string, level):
    """Check if a string is in a specified level of a row index tuple."""
    if level < 0 or level >= len(row_tuple):
        raise IndexError("Specified level is out of range for the row index tuple.")
    if string != row_tuple[level]:
        raise ValueError(f"The string '{string}' is not in level {level} of the row index tuple {row_tuple}.")
    return True
