from .dataframe_find import find_common_columns
from .validate import *


def add_calculated_column(
    df: pd.DataFrame,
    func: Callable,
    *column_names: Union[str | tuple],
    new_column_name: Optional[str | tuple] = None
) -> pd.DataFrame:
    """
    Add a new column to the DataFrame by applying a function to one or more existing columns.

    The new column is inserted directly after the last column in the list of provided column names.

    Args:
        df (pandas.DataFrame): The input DataFrame.
        func (Callable): The function to apply to the columns.
        *column_names (str): One or more column names to use as input for the function.
        new_column_name (Optional[str]): Name of the new column. If None, a default name is generated.

    Returns:
        pandas.DataFrame: The modified DataFrame with the new column added.

    Raises:
        ValueError: If the DataFrame is empty or a specified column does not exist.
        TypeError: If the provided function is not callable or a column name is not a string.

    Example:
        If columns 'A' and 'C' are specified, and 'C' is the 12th column in the DataFrame,
        the new column will be inserted as the 13th column.
    """
    # Validate inputs
    validate_dataframe_not_empty(df)
    validate_callable(func)
    for col_name in column_names:
        validate_value_is_string_or_tuple(col_name)
        validate_column_exists(df, col_name)

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


def add_calculated_row(
    df: pd.DataFrame,
    func: Callable,
    *row_names: str,
    new_row_name: Optional[str] = None
) -> pd.DataFrame:
    """
    Add a calculated row to the DataFrame by applying a function to one or more existing rows.

    This function transposes the DataFrame, applies the `add_calculated_column` function,
    and then transposes it back to add a new calculated row.

    Args:
        df (pandas.DataFrame): The input DataFrame with multi-index columns.
        func (Callable): The function to apply to the rows.
        *row_names (str): One or more row names to use as input for the function.
        new_row_name (Optional[str]): Name of the new row. If None, a default name is generated.

    Returns:
        pandas.DataFrame: The modified DataFrame with the new row added.

    Raises:
        ValueError: If the DataFrame is empty.
        TypeError: If any of the row names are not strings.

    Example:
        If rows 'R1' and 'R2' are specified, the function adds a new row that is the result
        of applying the function to these rows.
    """
    # Validate inputs
    validate_dataframe_not_empty(df)
    for row_name in row_names:
        validate_value_is_string(row_name)

    # Transpose the DataFrame, apply the column function, and transpose back
    transposed_df = df.T
    transposed_result = add_calculated_column(transposed_df, func, *row_names, new_column_name = new_row_name)
    return transposed_result.T


def add_calculated_columns_by_group(
    df: pd.DataFrame,
    func: Callable,
    *column_names: str,
    new_column_suffix: Optional[str] = 'calculated'
) -> pd.DataFrame:
    """
    Add calculated columns to groups of common columns in a multi-index DataFrame.

    This function finds common columns based on the provided column names at the highest level,
    groups them by their lower levels, and applies a calculation to each group. The result is added
    as a new column in each group.

    Args:
        df (pandas.DataFrame): The input DataFrame with multi-index columns.
        func (Callable): The function to apply to each group of common columns.
        *column_names (str): Column names at the highest level to identify common columns.
        new_column_suffix (Optional[str]): Suffix for the new column name. Defaults to 'calculated'.

    Returns:
        pandas.DataFrame: The modified DataFrame with the new calculated columns added.

    Raises:
        ValueError: If the DataFrame's columns are not a MultiIndex.
        TypeError: If any of the column names are not strings.

    Example:
        If columns 'x' and 'y' are specified, the function finds all common columns with these names,
        groups them by lower levels, applies the calculation, and adds the result as a new column.
    """
    # Validate inputs
    validate_columns_multiindex(df)

    for col_name in column_names:
        validate_value_is_string(col_name)
        validate_string_in_any_column_tuple(df.columns, col_name)

    # Get the multi-index column names as a flat index
    column_names_index = df.columns.to_flat_index()

    # Filter columns that match the criteria
    filtered_columns = [col for col in column_names_index if col[-1] in column_names]

    # Group columns by their lower levels (all levels except the last one)
    grouped_columns = {}
    for col in filtered_columns:
        lower_levels = col[:-1]
        grouped_columns.setdefault(lower_levels, []).append(col)

    # Apply the function to each group and add the result as a new column
    for lower_levels, columns in grouped_columns.items():
        if len(columns) == len(column_names):  # Ensure all specified columns are present
            # column_data = [df[col] for col in columns]
            # new_column = func(*column_data)
            new_column_name = lower_levels + (new_column_suffix,)
            # df[new_column_name] = new_column
            df = add_calculated_column(df, func, *columns, new_column_name = new_column_name)

    return df


def add_calculated_rows_by_group(
    df: pd.DataFrame,
    func: Callable,
    *row_names: str,
    new_row_suffix: Optional[str] = 'calculated'
) -> pd.DataFrame:
    """
    Add calculated rows to groups of common rows in a DataFrame.

    This function transposes the DataFrame, applies the `add_calculated_columns_by_group`
    function to specified rows (treated as columns), and then transposes it back to add
    new calculated rows.

    Args:
        df (pandas.DataFrame): The input DataFrame.
        func (Callable): The function to apply to each group of common rows.
        *row_names (str): One or more row names to identify common rows.
        new_row_suffix (Optional[str]): Suffix for the new row name. Defaults to 'calculated'.

    Returns:
        pd.DataFrame: The modified DataFrame with the new calculated rows added.

    Raises:
        ValueError: If the DataFrame is empty or if any specified row does not exist.
        TypeError: If any of the row names are not strings.

    Example:
        If rows 'R1' and 'R2' are specified, the function adds a new row that is the result
        of applying the function to these rows.
    """
    validate_rows_multiindex(df)

    # Transpose the DataFrame, apply the column function, and transpose back
    transposed_df = df.T
    transposed_result = add_calculated_columns_by_group(
        transposed_df,
        func,
        *row_names,
        new_column_suffix = new_row_suffix
    )
    return transposed_result.T
