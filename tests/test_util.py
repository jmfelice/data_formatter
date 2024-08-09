import unittest
import pandas as pd
from src.data_formatter.util import (
    sort_dataframe_by_custom_order,
    move_df_level_to_front
)


class TestSortDataFrameByCustomOrder(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame with MultiIndex columns for testing
        self.df_columns = pd.DataFrame({
            ('One', 'A', 1): [1, 2],
            ('One', 'A', 2): [3, 4],
            ('One', 'B', 1): [5, 6],
            ('One', 'B', 2): [7, 8],
            ('Two', 'A', 1): [9, 10],
            ('Two', 'A', 2): [11, 12]
        })
        self.df_columns.columns = pd.MultiIndex.from_tuples(self.df_columns.columns)

        # Create a sample DataFrame with MultiIndex index for testing
        self.df_index = self.df_columns.T
        self.df_index.index = pd.MultiIndex.from_tuples(self.df_index.index)

    def test_sort_columns_by_level(self):
        # Test sorting columns by a specified level
        result = sort_dataframe_by_custom_order(self.df_columns, ['Two', 'One'], axis = 1, level = 0)
        expected_columns = [
            ('Two', 'A', 1), ('Two', 'A', 2),
            ('One', 'A', 1), ('One', 'A', 2), ('One', 'B', 1), ('One', 'B', 2)
        ]
        self.assertEqual(result.columns.tolist(), expected_columns)

    def test_sort_index_by_level(self):
        # Test sorting index by a specified level
        result = sort_dataframe_by_custom_order(self.df_index, ['Two', 'One'], axis = 0, level = 0)
        expected_index = [
            ('Two', 'A', 1), ('Two', 'A', 2),
            ('One', 'A', 1), ('One', 'A', 2), ('One', 'B', 1), ('One', 'B', 2)
        ]
        self.assertEqual(result.index.tolist(), expected_index)

    def test_invalid_order(self):
        # Test when an element in the desired order is not found
        with self.assertRaises(ValueError) as context:
            sort_dataframe_by_custom_order(self.df_columns, ['Three'], axis = 1, level = 0)
        self.assertIn("'Three' not found in level 0 of the columns.", str(context.exception))

    def test_preserve_lower_levels(self):
        # Test preserving the order of lower levels
        result = sort_dataframe_by_custom_order(self.df_columns, [2, 1], axis = 1, level = 2)
        expected_columns = [
            ('One', 'A', 2),
            ('One', 'A', 1),
            ('One', 'B', 2),
            ('One', 'B', 1),
            ('Two', 'A', 2),
            ('Two', 'A', 1)
        ]
        self.assertEqual(result.columns.tolist(), expected_columns)

    def test_preserve_lower_levels_2(self):
        # Test preserving the order of lower levels
        result = sort_dataframe_by_custom_order(self.df_columns, ['B', 'A'], axis = 1, level = 1)
        expected_columns = [
            ('One', 'B', 1),
            ('One', 'B', 2),
            ('One', 'A', 1),
            ('One', 'A', 2),
            ('Two', 'A', 1),
            ('Two', 'A', 2)
        ]
        self.assertEqual(result.columns.tolist(), expected_columns)


class TestMoveDfLevelToFront(unittest.TestCase):

    def setUp(self):
        # Sample DataFrame with MultiIndex for testing
        arrays_index = [
            ['A', 'A', 'B', 'B'],
            ['one', 'two', 'one', 'two'],
            [1, 2, 1, 2]
        ]
        expected_index = pd.MultiIndex.from_arrays(arrays_index,names = ('letters', 'numbers', 'values'))
        self.df_index = pd.DataFrame(
            {'data': [10, 20, 30, 40]},
            index = expected_index
        )

        arrays_columns = [
            ['X', 'X', 'Y', 'Y'],
            ['alpha', 'beta', 'alpha', 'beta'],
            [10, 20, 10, 20]
        ]
        expected_columns = pd.MultiIndex.from_arrays(arrays_columns, names=('letters', 'types', 'numbers'))
        self.df_columns = pd.DataFrame(
            [[1, 2, 3, 4], [5, 6, 7, 8]],
            columns = expected_columns
        )

    def test_move_level_to_front_index(self):
        # Test moving a level to the front of the index
        df_reordered = move_df_level_to_front(self.df_index, level_to_move = 'numbers', axis = 0)
        expected_index = pd.MultiIndex.from_arrays(
            [['one', 'two', 'one', 'two'], ['A', 'A', 'B', 'B'], [1, 2, 1, 2]],
            names = ('numbers', 'letters', 'values')
        )
        pd.testing.assert_index_equal(df_reordered.index, expected_index)

    def test_move_level_to_front_columns(self):
        # Test moving a level to the front of the columns
        df_reordered = move_df_level_to_front(self.df_columns, level_to_move = 'types', axis = 1)
        expected_columns = pd.MultiIndex.from_arrays(
            [['alpha', 'beta', 'alpha', 'beta'], ['X', 'X', 'Y', 'Y'], [10, 20, 10, 20]],
            names = ('types', 'letters', 'numbers')
        )
        pd.testing.assert_index_equal(df_reordered.columns, expected_columns)

    def test_invalid_level(self):
        # Test with an invalid level name
        with self.assertRaises(ValueError) as context:
            move_df_level_to_front(self.df_index, level_to_move = 'invalid', axis = 0)
        self.assertIn("The level 'invalid' is not found in the MultiIndex.", str(context.exception))


if __name__ == '__main__':
    unittest.main()
