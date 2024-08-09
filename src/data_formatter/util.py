from itertools import repeat


def get_even_numbers(x):
    df_row_count = list(range(0, len(x)))
    even_row_count = [num for num in df_row_count if num % 2 == 0]
    return even_row_count


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


def sort_dataframe(df, desired_order, axis = 0, level = 0):
    def sort_key(index):
        # Create a key based on the desired order for the specified level
        level_key = desired_order.index(index[level]) if index[level] in desired_order else len(
            desired_order
            )
        # Create a tuple that maintains the order of all preceding levels
        return tuple(list(index[:level]) + [level_key] + list(index[level + 1:]))

    # Extract the MultiIndex
    if axis == 1:
        idx = df.columns
    else:
        idx = df.index

    sorted_idx = sorted(idx, key = sort_key)
    df = df.loc[:, sorted_idx]
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
