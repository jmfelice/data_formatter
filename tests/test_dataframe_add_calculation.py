import unittest
import pandas as pd
import numpy as np
from src.data_formatter.dataframe_add_calculation import (
    add_calculated_column,
    add_calculated_columns_by_group,
    add_calculated_row,
    add_calculated_rows_by_group
)


class TestAddCalculatedColumn(unittest.TestCase):

    def setUp(self):
        # Sample DataFrames for testing
        self.df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6],
            'C': [7, 8, 9],
            'D': [10, 11, 12]
        })

        # Multi-index columns DataFrame
        self.multiindex_columns_df = pd.DataFrame(
            {
                ('A', 'x'): [1, 2, 3],
                ('A', 'y'): [4, 5, 6],
                ('B', 'x'): [7, 8, 9],
                ('B', 'y'): [10, 11, 12]
            }
        )

        # Multi-index rows DataFrame
        index = pd.MultiIndex.from_tuples([('a', 1), ('a', 2), ('b', 1)])
        self.multiindex_rows_df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        }, index = index)

    def test_add_column_with_valid_inputs(self):
        # Test adding a column with valid inputs
        result = add_calculated_column(self.df, np.add, 'A', 'C', new_column_name = 'E')
        expected = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6],
            'C': [7, 8, 9],
            'E': [8, 10, 12],
            'D': [10, 11, 12]
        })
        pd.testing.assert_frame_equal(result, expected)

    def test_add_column_without_new_column_name(self):
        # Test adding a column without specifying a new column name
        result = add_calculated_column(self.df, np.add, 'A', 'B')
        self.assertIn('new_column_4', result.columns)

    def test_empty_dataframe(self):
        # Test with an empty DataFrame
        empty_df = pd.DataFrame()
        with self.assertRaises(ValueError) as context:
            add_calculated_column(empty_df, np.add, 'A', 'B')
        self.assertEqual(str(context.exception), "The DataFrame is empty.")

    def test_non_existent_column(self):
        # Test with a non-existent column
        with self.assertRaises(ValueError) as context:
            add_calculated_column(self.df, np.add, 'A', 'Z')
        self.assertEqual(str(context.exception), "Column 'Z' does not exist in the DataFrame.")

    def test_non_callable_function(self):
        # Test with a non-callable function
        with self.assertRaises(TypeError) as context:
            add_calculated_column(self.df, "not_a_function", 'A', 'B')
        self.assertEqual(str(context.exception), "The provided function is not callable.")

    def test_non_string_or_tuple_column_name(self):
        # Test with a non-string column name
        with self.assertRaises(TypeError) as context:
            add_calculated_column(self.df, np.add, 'A', 1)
        self.assertEqual(str(context.exception), "The value '1' is not a string or a tuple.")

    def test_function_applies_correctly(self):
        # Test if the function applies correctly
        result = add_calculated_column(self.df, lambda x, y: x * y, 'A', 'B', new_column_name = 'AB')
        expected = pd.DataFrame({
            'A' : [1, 2, 3],
            'B' : [4, 5, 6],
            'AB': [4, 10, 18],
            'C' : [7, 8, 9],
            'D' : [10, 11, 12]
        })
        pd.testing.assert_frame_equal(result, expected)

    def test_insert_position(self):
        # Test if the new column is inserted directly after the last column in the list
        result = add_calculated_column(self.df, np.add, 'A', 'C', new_column_name = 'E')
        self.assertEqual(result.columns.get_loc('E'), 3)

    def test_multiindex_columns(self):
        # Test with a DataFrame having multi-index columns
        result = add_calculated_column(
            self.multiindex_columns_df,
            np.add,
            ('A', 'x'), ('A', 'y'),
            new_column_name = ('A', 'z')
        )

        expected = pd.DataFrame(
            {
                ('A', 'x'): [1, 2, 3],
                ('A', 'y'): [4, 5, 6],
                ('A', 'z'): [5, 7, 9],
                ('B', 'x'): [7, 8, 9],
                ('B', 'y'): [10, 11, 12]
            }
        )
        pd.testing.assert_frame_equal(result, expected)

    def test_multiindex_rows(self):
        # Test with a DataFrame having multi-index rows
        result = add_calculated_column(self.multiindex_rows_df, np.add, 'A', 'B', new_column_name = 'C')
        expected = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6],
            'C': [5, 7, 9]
        }, index = self.multiindex_rows_df.index)
        pd.testing.assert_frame_equal(result, expected)


class TestAddCalculatedColumnsByGroup(unittest.TestCase):

    def setUp(self):
        # Multi-index columns DataFrame
        self.multiindex_columns_df = pd.DataFrame(
            {
                ('A', 'x'): [1, 2, 3],
                ('A', 'y'): [4, 5, 6],
                ('B', 'x'): [7, 8, 9],
                ('B', 'y'): [10, 11, 12]
            }
        )

    def test_add_calculated_columns_by_group(self):
        # Test adding calculated columns with valid inputs
        result = add_calculated_columns_by_group(
            self.multiindex_columns_df,
            np.add,
            'x', 'y',
            new_column_suffix='sum'
        )
        expected = pd.DataFrame(
            {
                ('A', 'x'): [1, 2, 3],
                ('A', 'y'): [4, 5, 6],
                ('A', 'sum'): [5, 7, 9],
                ('B', 'x'): [7, 8, 9],
                ('B', 'y'): [10, 11, 12],
                ('B', 'sum'): [17, 19, 21]
            }
        )
        pd.testing.assert_frame_equal(result, expected)

    def test_invalid_column_names(self):
        # Test with invalid column names
        with self.assertRaises(TypeError):
            add_calculated_columns_by_group(self.multiindex_columns_df, np.add, 1)

    def test_non_multiindex_dataframe(self):
        # Test with a non-multi-index DataFrame
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        with self.assertRaises(ValueError):
            add_calculated_columns_by_group(df, np.add, 'A')


class TestAddCalculatedRow(unittest.TestCase):

    def setUp(self):
        # Sample DataFrame for testing
        self.df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6],
            'C': [7, 8, 9]
        }, index = ['R1', 'R2', 'R3'])

    def test_add_calculated_row(self):
        # Test adding a calculated row with valid inputs
        result = add_calculated_row(self.df, np.add, 'R1', 'R2', new_row_name = 'R_sum')
        expected = pd.DataFrame({
            'A': [1, 2, 3, 3],
            'B': [4, 5, 9, 6],
            'C': [7, 8, 15, 9]
        }, index = ['R1', 'R2', 'R_sum', 'R3'])
        pd.testing.assert_frame_equal(result, expected)

    def test_invalid_row_names(self):
        # Test with invalid row names
        with self.assertRaises(TypeError):
            add_calculated_row(self.df, np.add, 1)

    def test_empty_dataframe(self):
        # Test with an empty DataFrame
        empty_df = pd.DataFrame()
        with self.assertRaises(ValueError):
            add_calculated_row(empty_df, np.add, 'R1', 'R2')


class TestAddCalculatedRowsByGroup(unittest.TestCase):

    def setUp(self):
        # Sample DataFrame with MultiIndex rows for testing
        index = pd.MultiIndex.from_tuples([('R1', 'A'), ('R2', 'A'), ('R2', 'B')])
        self.df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6],
            'C': [7, 8, 9]
        }, index=index)

    def test_add_calculated_rows(self):
        # Test adding calculated rows with valid inputs
        result = add_calculated_rows_by_group(self.df, np.add, 'A', 'B', new_row_suffix='sum')
        expected_index = pd.MultiIndex.from_tuples([('R1', 'A'), ('R2', 'A'), ('R2', 'B'), ('R2', 'sum')])
        expected = pd.DataFrame({
            'A': [1, 2, 3, 5],
            'B': [4, 5, 6, 11],
            'C': [7, 8, 9, 17]
        }, index=expected_index)
        pd.testing.assert_frame_equal(result, expected)

    def test_invalid_row_names(self):
        # Test with invalid row names
        with self.assertRaises(ValueError):
            add_calculated_rows_by_group(self.df, np.add, 'C', 'Z')

    def test_empty_dataframe(self):
        # Test with an empty DataFrame
        empty_df = pd.DataFrame()
        with self.assertRaises(ValueError):
            add_calculated_rows_by_group(empty_df, np.add, 'A', 'B')

    def test_non_multiindex_dataframe(self):
        # Test with a DataFrame that does not have MultiIndex rows
        df_single_index = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6],
            'C': [7, 8, 9]
        }, index=['R1', 'R2', 'R3'])
        with self.assertRaises(ValueError):
            add_calculated_rows_by_group(df_single_index, np.add, 'R1', 'R2')


if __name__ == '__main__':
    unittest.main()
