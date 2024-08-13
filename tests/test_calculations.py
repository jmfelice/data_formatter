import unittest
import numpy as np
import pandas as pd
from src.data_formatter.calculations import (
    growth,
    make_commonsize_vertical,
    make_commonsize_horizontal
)


class TestGrowthFunction(unittest.TestCase):

    def test_basic_functionality(self):
        x = np.array([10, 20, 30])
        y = np.array([2, 5, 0])
        expected = np.array([5, 4, 0])
        result = growth(x, y)
        np.testing.assert_array_equal(result, expected)

    def test_zero_division(self):
        x = np.array([1, 2, 3])
        y = np.array([0, 0, 0])
        expected = np.array([0, 0, 0])
        result = growth(x, y)
        np.testing.assert_array_equal(result, expected)

    def test_scalar_input(self):
        x = 10.0
        y = 2.0
        expected = np.array(5.0)
        result = growth(x, y)
        np.testing.assert_array_equal(result, expected)

    def test_broadcasting(self):
        x = np.array([10, 20, 30])
        y = 2.0
        expected = np.array([5, 10, 15])
        result = growth(x, y)
        np.testing.assert_array_equal(result, expected)


class TestMakeCommonSizeVertical(unittest.TestCase):

    def setUp(self):
        # Regular DataFrame setup
        self.df_regular = pd.DataFrame({
            'category': ['Revenue', 'Cost', 'Profit'],
            'value1'  : [100, 50, 50],
            'value2'  : [200, 100, 100]
        })

        # MultiIndex DataFrame setup
        arrays = [
            ['A', 'A', 'A', 'B', 'B', 'B'],
            ['Revenue', 'Cost', 'Profit', 'Revenue', 'Cost', 'Profit']
        ]
        index = pd.MultiIndex.from_arrays(arrays, names = ('group', 'category'))
        self.df_multi = pd.DataFrame({
            'value1': [200, 100, 100, 300, 150, 150],
            'value2': [400, 200, 200, 600, 300, 300]
        }, index = index)

        # MultiIndex for both rows and columns
        row_arrays = [
            ['X', 'X', 'Y', 'Y'],
            ['Revenue', 'Cost', 'Revenue', 'Cost']
        ]
        col_arrays = [
            ['value1', 'value1', 'value2', 'value2'],
            ['A', 'B', 'A', 'B']
        ]
        row_index = pd.MultiIndex.from_arrays(row_arrays, names = ('group', 'category'))
        col_index = pd.MultiIndex.from_arrays(col_arrays, names = ('type', 'subtype'))
        self.df_multi_row_col = pd.DataFrame([
            [100, 200, 150, 300],
            [50, 100, 75, 150],
            [200, 400, 300, 600],
            [100, 200, 150, 300]
        ], index = row_index, columns = col_index)

    def test_regular_dataframe(self):
        result = make_commonsize_vertical(self.df_regular, 'category', 'Revenue', ['value1', 'value2'])
        expected = pd.DataFrame({
            'category': ['Revenue', 'Cost', 'Profit'],
            'value1'  : [1.0, 0.5, 0.5],
            'value2'  : [1.0, 0.5, 0.5]
        })
        pd.testing.assert_frame_equal(result, expected)

    def test_multiindex_dataframe(self):
        result = make_commonsize_vertical(self.df_multi, 'category', 'Revenue', ['value1', 'value2'])
        expected_values1 = np.array([1.0, 0.5, 0.5, 1.0, 0.5, 0.5])
        expected_values2 = np.array([1.0, 0.5, 0.5, 1.0, 0.5, 0.5])
        np.testing.assert_array_almost_equal(result['value1'].values, expected_values1)
        np.testing.assert_array_almost_equal(result['value2'].values, expected_values2)

    def test_multiindex_row_col_dataframe(self):
        result = make_commonsize_vertical(self.df_multi_row_col, 'category', 'Revenue',
                                          [('value1', 'A'), ('value2', 'B')])
        expected_values1_A = np.array([1.0, 0.5, 1.0, 0.5])
        expected_values2_B = np.array([0.5, 0.25, 0.5, 0.25])
        np.testing.assert_array_almost_equal(result[('value1', 'A')].values, expected_values1_A)
        np.testing.assert_array_almost_equal(result[('value2', 'B')].values, expected_values2_B)

    def test_empty_dataframe(self):
        df_empty = pd.DataFrame(columns = ['category', 'value1', 'value2'])
        with self.assertRaises(ValueError):
            make_commonsize_vertical(df_empty, 'category', 'Revenue', ['value1', 'value2'])

    def test_missing_category_column(self):
        df_missing_category = pd.DataFrame({
            'value1': [100, 50, 50],
            'value2': [200, 100, 100]
        })
        with self.assertRaises(KeyError):
            make_commonsize_vertical(df_missing_category, 'category', 'Revenue', ['value1', 'value2'])

    def test_missing_value_column(self):
        with self.assertRaises(KeyError):
            make_commonsize_vertical(self.df_regular, 'category', 'Revenue', ['value1', 'missing_value'])

    def test_different_level_indexes(self):
        # MultiIndex with different levels
        arrays = [
            ['A', 'A', 'B', 'B'],
            ['X', 'Y', 'X', 'Y'],
            ['Revenue', 'Cost', 'Revenue', 'Cost']
        ]
        index = pd.MultiIndex.from_arrays(arrays, names = ('group', 'subgroup', 'category'))
        df_different_levels = pd.DataFrame({
            'value1': [200, 100, 300, 150],
            'value2': [400, 200, 600, 300]
        }, index = index)

        result = make_commonsize_vertical(df_different_levels, 'category', 'Revenue', ['value1', 'value2'])
        expected_values1 = np.array([1.0, 0.5, 1.0, 0.5])
        expected_values2 = np.array([1.0, 0.5, 1.0, 0.5])
        np.testing.assert_array_almost_equal(result['value1'].values, expected_values1)
        np.testing.assert_array_almost_equal(result['value2'].values, expected_values2)


if __name__ == '__main__':
    unittest.main()
