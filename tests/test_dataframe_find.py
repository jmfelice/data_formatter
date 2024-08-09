import unittest
import pandas as pd
from src.data_formatter.dataframe_find import (
    find_columns,
    find_column_positions,
    find_columns_like,
    find_common_columns
)


class TestFindColumns(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame with MultiIndex columns for testing
        self.multiindex_df = pd.DataFrame({
            ('A', 'foo'): [1, 2],
            ('B', 'bar'): [3, 4],
            ('C', 'baz'): [5, 6]
        })
        self.multiindex_df.columns = pd.MultiIndex.from_tuples(self.multiindex_df.columns)

        # Create a sample DataFrame with single-level columns for testing
        self.singleindex_df = pd.DataFrame({
            'A': [1, 2],
            'B': [3, 4],
            'C': [5, 6]
        })

    def test_find_columns_no_lvl_multiindex(self):
        # Test without specifying a level on a MultiIndex DataFrame
        result = find_columns(self.multiindex_df, 'foo')
        self.assertEqual(result, [('A', 'foo')])

    def test_find_columns_with_lvl_multiindex(self):
        # Test with specifying a level on a MultiIndex DataFrame
        result = find_columns(self.multiindex_df, 'A', lvl=0)
        self.assertEqual(result, [('A', 'foo')])

    def test_find_columns_no_match_multiindex(self):
        # Test with a column name that doesn't match on a MultiIndex DataFrame
        result = find_columns(self.multiindex_df, 'nonexistent')
        self.assertEqual(result, [])

    def test_find_columns_lvl_no_match_multiindex(self):
        # Test with a level that doesn't match on a MultiIndex DataFrame
        result = find_columns(self.multiindex_df, 'nonexistent', lvl=0)
        self.assertEqual(result, [])

    def test_find_columns_singleindex(self):
        # Test finding columns on a single-level DataFrame
        result = find_columns(self.singleindex_df, 'A')
        self.assertEqual(result, ['A'])

    def test_find_columns_no_match_singleindex(self):
        # Test with a column name that doesn't match on a single-level DataFrame
        result = find_columns(self.singleindex_df, 'nonexistent')
        self.assertEqual(result, [])


class TestFindColumnPositions(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame with MultiIndex columns for testing
        self.multiindex_df = pd.DataFrame({
            ('A', 'foo'): [1, 2],
            ('B', 'bar'): [3, 4],
            ('C', 'baz'): [5, 6]
        })
        self.multiindex_df.columns = pd.MultiIndex.from_tuples(self.multiindex_df.columns)

        # Create a sample DataFrame with single-level columns for testing
        self.singleindex_df = pd.DataFrame({
            'A': [1, 2],
            'B': [3, 4],
            'C': [5, 6]
        })

    def test_find_column_positions_multiindex(self):
        # Test finding column positions in a MultiIndex DataFrame
        result = find_column_positions(self.multiindex_df, 'foo')
        self.assertEqual(result, [0])

    def test_find_column_positions_with_lvl_multiindex(self):
        # Test finding column positions with a specified level in a MultiIndex DataFrame
        result = find_column_positions(self.multiindex_df, 'A', lvl=0)
        self.assertEqual(result, [0])

    def test_find_column_positions_no_match_multiindex(self):
        # Test with a column name that doesn't match in a MultiIndex DataFrame
        result = find_column_positions(self.multiindex_df, 'nonexistent')
        self.assertEqual(result, [])

    def test_find_column_positions_singleindex(self):
        # Test finding column positions in a single-level DataFrame
        result = find_column_positions(self.singleindex_df, 'A')
        self.assertEqual(result, [0])

    def test_find_column_positions_no_match_singleindex(self):
        # Test with a column name that doesn't match in a single-level DataFrame
        result = find_column_positions(self.singleindex_df, 'nonexistent')
        self.assertEqual(result, [])


class TestFindColumnsLike(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame with MultiIndex columns for testing
        self.multiindex_df = pd.DataFrame({
            ('A', 'foo', 'alpha'): [1, 2],
            ('B', 'bar', 'beta'): [3, 4],
            ('C', 'baz', 'gamma'): [5, 6],
            ('D', 'qux', 'delta space'): [7, 8]
        })
        self.multiindex_df.columns = pd.MultiIndex.from_tuples(self.multiindex_df.columns)

        # Create a sample DataFrame with single-level columns for testing
        self.singleindex_df = pd.DataFrame({
            'Column One': [1, 2],
            'Column Two': [3, 4],
            'Another Column': [5, 6]
        })

    def test_find_columns_like_multiindex(self):
        # Test finding columns with substrings in a MultiIndex DataFrame
        result = find_columns_like(self.multiindex_df, 'fo')
        self.assertEqual(result, [('A', 'foo', 'alpha')])

    def test_find_columns_like_with_lvl_multiindex(self):
        # Test finding columns with substrings at a specific level in a MultiIndex DataFrame
        result = find_columns_like(self.multiindex_df, 'ba', lvl=1)
        self.assertEqual(result, [('B', 'bar', 'beta'), ('C', 'baz', 'gamma')])

    def test_find_columns_like_with_spaces_multiindex(self):
        # Test finding columns with substrings that include spaces in a MultiIndex DataFrame
        result = find_columns_like(self.multiindex_df, 'delta sp', lvl=2)
        self.assertEqual(result, [('D', 'qux', 'delta space')])

    def test_find_columns_like_no_match_multiindex(self):
        # Test with substrings that don't match any columns in a MultiIndex DataFrame
        result = find_columns_like(self.multiindex_df, 'nonexistent')
        self.assertEqual(result, [])

    def test_find_columns_like_singleindex(self):
        # Test finding columns with substrings in a single-level DataFrame
        result = find_columns_like(self.singleindex_df, 'Colu')
        self.assertEqual(result, ['Column One', 'Column Two', 'Another Column'])

    def test_find_columns_like_partial_singleindex(self):
        # Test finding columns with a partial substring in a single-level DataFrame
        result = find_columns_like(self.singleindex_df, 'On')
        self.assertEqual(result, ['Column One'])

    def test_find_columns_like_no_match_singleindex(self):
        # Test with substrings that don't match any columns in a single-level DataFrame
        result = find_columns_like(self.singleindex_df, 'nonexistent')
        self.assertEqual(result, [])


class TestFindCommonColumns(unittest.TestCase):

    def setUp(self):
        # Create sample multi-index DataFrames for testing with three levels
        self.df1 = pd.DataFrame(
            {
                ('A', '1', 'x'): [1, 2],
                ('A', '1', 'y'): [3, 4],
                ('B', '2', 'x'): [5, 6],
                ('B', '2', 'y'): [7, 8]
            }
        )

        self.df2 = pd.DataFrame(
            {
                ('A', '1', 'x'): [1, 2],
                ('A', '1', 'z'): [3, 4],
                ('B', '2', 'x'): [5, 6],
                ('C', '3', 'y'): [7, 8]
            }
        )

        self.df3 = pd.DataFrame(
            {
                ('A', '1', 'x'): [1, 2],
                ('A', '1', 'x'): [3, 4],
                ('B', '2', 'x'): [5, 6],
                ('B', '2', 'x'): [7, 8]
            }
        )

        self.df_empty = pd.DataFrame()

    def test_common_columns_present(self):
        # Test with common columns present
        result = find_common_columns(self.df1, 'x', 'y')
        expected = [('A', '1', 'x'), ('A', '1', 'y'), ('B', '2', 'x'), ('B', '2', 'y')]
        self.assertEqual(result, expected)

    def test_partial_match(self):
        # Test with partial matches
        result = find_common_columns(self.df2, 'x', 'y')
        expected = []
        self.assertEqual(result, expected)

    def test_no_match(self):
        # Test with no matches
        result = find_common_columns(self.df1, 'z')
        expected = []
        self.assertEqual(result, expected)

    def test_empty_dataframe(self):
        # Test with an empty DataFrame
        with self.assertRaises(ValueError):
            find_common_columns(self.df_empty, 'x', 'y')

    def test_single_string(self):
        # Test with a single string
        result = find_common_columns(self.df1, 'x')
        expected = [('A', '1', 'x'), ('B', '2', 'x')]
        self.assertEqual(result, expected)

    def test_duplicate_columns(self):
        # Test with duplicate columns
        result = find_common_columns(self.df3, 'x')
        expected = [('A', '1', 'x'), ('B', '2', 'x')]
        self.assertEqual(result, expected)

    def test_non_string_input(self):
        # Test with non-string input (should raise an error)
        with self.assertRaises(TypeError):
            find_common_columns(self.df1, 1)

    def test_no_column_strings(self):
        # Test with no column strings provided
        result = find_common_columns(self.df1)
        expected = []
        self.assertEqual(result, expected)

    def test_non_multiindex_dataframe(self):
        # Test with a non-multi-index DataFrame
        df_single_index = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        with self.assertRaises(ValueError):
            find_common_columns(df_single_index, 'A')


if __name__ == '__main__':
    unittest.main()
