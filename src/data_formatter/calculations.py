import numpy as np
from typing import Union, List
import pandas as pd
from src.data_formatter.validate import *


def growth(x: Union[np.ndarray, float], y: Union[np.ndarray, float]) -> np.ndarray:
    """
    Calculate the element-wise growth rate by dividing `x` by `y`.

    Parameters:
    x (Union[np.ndarray, float]): The numerator, can be a NumPy array or a float.
    y (Union[np.ndarray, float]): The denominator, can be a NumPy array or a float.
                                  Division by zero is handled by returning zero for those elements.

    Returns:
    np.ndarray: An array containing the element-wise division results. Elements where `y` is zero are set to zero.

    Raises:
    ValueError: If `x` and `y` have different shapes and are not broadcastable.
    """
    # Ensure the output array is of a floating-point type
    return np.divide(x, y, out=np.zeros_like(x, dtype=np.float64), where=y != 0.0)


def make_commonsize_vertical(df, category_col, category_val, group_cols):
    calc = lambda x: x / x.loc[x.index.get_level_values(category_col) == category_val].values
    result = df.groupby(group_cols, group_keys = False).apply(calc)
    return result


def make_commonsize_horizontal(df):
    df = df.apply(lambda x: x / x.shift(1), axis = 1)
    df = df.drop(df.columns.values[0], axis = 1)
    return df
