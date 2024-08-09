def find_columns(df, column_name: str, lvl = None):
    in_any_cols = [column_name in x for x in df.columns]
    all_cols = list(df.columns[in_any_cols])

    if lvl is None:
        return all_cols

    lvls = df.columns.get_level_values(lvl)
    in_lvls = [column_name == x for x in lvls]
    specific_cols = list(df.columns[in_lvls])
    return specific_cols


def find_rows(df, row_name: str, lvl = None):
    return find_columns(df.T, row_name, lvl)


def find_column_positions(df, column_name: str, lvl = None):
    requested_cols = find_columns(df, column_name, lvl)
    all_cols = df.columns.tolist()

    lst = []
    for i in requested_cols:
        lst.append([x for x, y in enumerate(all_cols) if y == i][0])

    return lst


def find_row_positions(df, row_name: str, lvl = None):
    return find_column_positions(df.T, row_name, lvl)


def find_columns_like(df, substrings, lvl = None):
    """
    Find columns in a DataFrame that contain the given substring(s).

    Args: df (pandas.DataFrame): The DataFrame to search. substrings (str or list): A substring
    or a list of substrings to search for in column names. lvl (int or None, optional): The level
    of the MultiIndex to search. If None, search all levels.

    Returns:
        list: A list of column names (tuples) that contain the substring(s).
    """
    if isinstance(substrings, str):
        substrings = [substrings]

    all_cols = []
    for col in df.columns:
        if isinstance(col, tuple):
            if any(substring in ''.join(str(level) for level in col) for substring in substrings):
                all_cols.append(col)
        else:
            if any(substring in str(col) for substring in substrings):
                all_cols.append(col)

    if lvl is not None:
        lvls = df.columns.get_level_values(lvl)
        in_lvls = [any(substring in str(x) for substring in substrings) for x in lvls]
        specific_cols = [col for col, match in zip(df.columns, in_lvls) if match]
        return specific_cols

    return all_cols


def find_rows_like(df, substrings, lvl = None):
    return find_columns_like(df = df.T, substrings = substrings, lvl = lvl)


def find_common_columns(df, *column_strings):
    """
    Find all columns in a multi-index DataFrame that contain the given strings at the highest level,
    and where all the strings are present for each combination of lower levels.

    Args: df (pandas.DataFrame): The input multi-index DataFrame. *column_strings (str): One or
    more strings to search for in the highest level of the column multi-index.

    Returns:
        list: A list of tuples representing the common column multi-indexes.
    """
    # Get the multi-index column names
    column_names = df.columns.to_flat_index()

    # Filter columns that contain all the given strings at the highest level
    def filter_by(x): any(string == x[-1] or str(string) in str(x[-1]) for string in column_strings)
    filtered_columns = list(filter(filter_by, column_names))

    # Group columns by lower levels
    grouped_columns = {}
    for col in filtered_columns:
        lower_levels = col[:-1]
        grouped_columns.setdefault(lower_levels, []).append(col)

    # Find common columns where all strings are present for each combination of lower levels
    common_columns = []
    for lower_levels, columns in grouped_columns.items():
        column_sets = [set(col[-1] for col in columns) for _ in zip(*columns)]
        if all(set(column_strings).issubset(col_set) for col_set in column_sets):
            common_columns.extend(columns)

    return common_columns
