import pandas as pd
from typing import Union, List, Tuple


def calculate_relative_to_reference(
    df: pd.DataFrame,
    reference_row: Union[str, int, Tuple],
    value_cols: Union[str, List[str], Tuple, List[Tuple]]
) -> pd.DataFrame:
    """
    Calculate values relative to a reference row for specified value columns.

    Parameters:
    df (pd.DataFrame): Input DataFrame, can be regular or with MultiIndex for rows/columns.
    reference_row (Union[str, int, Tuple]): Identifier for the reference row.
    value_cols (Union[str, List[str], Tuple, List[Tuple]]): Column(s) to perform calculations on.

    Returns:
    pd.DataFrame: A new DataFrame with the same structure as the input, but with specified
                  value columns divided by the reference row values.

    Raises:
    KeyError: If the reference row or value columns are not found in the DataFrame.
    """
    # Ensure value_cols is a list
    if isinstance(value_cols, (str, tuple)):
        value_cols = [value_cols]

    # Create a copy of the original DataFrame
    result_df = df.copy()

    # Locate the reference row
    try:
        if isinstance(df.index, pd.MultiIndex):
            reference_values = df.loc[reference_row]
        else:
            reference_values = df.loc[reference_row]
    except KeyError:
        raise KeyError(f"Reference row '{reference_row}' not found in the DataFrame.")

    # Perform calculations for each value column
    for col in value_cols:
        try:
            result_df[col] = df[col] / reference_values[col]
        except KeyError:
            raise KeyError(f"Value column '{col}' not found in the DataFrame.")

    return result_df

# Example usage and tests
if __name__ == "__main__":
    # Regular DataFrame
    df_regular = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6],
        'C': [7, 8, 9]
    }, index=['X', 'Y', 'Z'])

    # MultiIndex DataFrame (rows and columns)
    index = pd.MultiIndex.from_tuples([('I', 'X'), ('I', 'Y'), ('II', 'Z')], names=['group', 'subgroup'])
    columns = pd.MultiIndex.from_tuples([('val', 'A'), ('val', 'B'), ('info', 'C')], names=['category', 'subcategory'])
    df_multi = pd.DataFrame({
        ('val', 'A'): [1, 2, 3],
        ('val', 'B'): [4, 5, 6],
        ('info', 'C'): [7, 8, 9]
    }, index=index, columns=columns)

    # Test with regular DataFrame
    result_regular = calculate_relative_to_reference(df_regular, 'X', ['A', 'B'])
    print("Regular DataFrame Result:")
    print(result_regular)
    print()

    # Test with MultiIndex DataFrame
    result_multi = calculate_relative_to_reference(df_multi, ('I', 'X'), [('val', 'A'), ('val', 'B')])
    print("MultiIndex DataFrame Result:")
    print(result_multi)
