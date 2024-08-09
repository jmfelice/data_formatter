import numpy as np


def growth(x,y):
    return np.divide(x, y, out = np.zeros_like(x), where = y != 0.0)


def make_commonsize_vertical(df, category_col, category_val, group_cols):
    def calc(x):
        x / x.loc[x.index.get_level_values(category_col) == category_val].values
    result = df.groupby(group_cols, group_keys = False).apply(calc)
    return result


def make_commonsize_horizontal(df):
    df = df.apply(lambda x: x / x.shift(1), axis = 1)
    df = df.drop(df.columns.values[0], axis = 1)
    return df
