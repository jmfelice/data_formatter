import unittest
import pandas as pd
from src.data_formatter.pivot_tables import pivot_to


class TestPivotTo(unittest.TestCase):

    def setUp(self):
        # Sample DataFrame for testing
        self.df = pd.DataFrame({
            'Year': [2020, 2020, 2021, 2021],
            'Region': ['North', 'South', 'North', 'South'],
            'Product': ['A', 'B', 'A', 'B'],
            'Sales': [100, 150, 200, 250],
            'Profit': [20, 30, 40, 50]
        })

    def test_pivot_with_title(self):
        # Test pivoting with a title
        result = pivot_to(self.df, values=['Profit', 'Sales'], columns=['Region'], title='Testing Data')
        expected_index = pd.MultiIndex.from_tuples(
            [(2020, 'A'), (2020, 'B'), (2021, 'A'), (2021, 'B')],
            names=['Year', 'Product']
        )
        expected = pd.DataFrame({
            ('Testing Data', 'Sales', 'North'): [100, 0, 200, 0],
            ('Testing Data', 'Sales', 'South'): [0, 150, 0, 250],
            ('Testing Data', 'Profit', 'North'): [20, 0, 40, 0],
            ('Testing Data', 'Profit', 'South'): [0, 30, 0, 50]
        }, index=expected_index)
        expected.columns.names = ['Testing Data', None, 'Region']
        pd.testing.assert_frame_equal(result, expected)

    def test_pivot_without_title(self):
        # Test pivoting without a title
        result = pivot_to(self.df, values=['Sales', 'Profit'], columns=['Region'])
        expected_index = pd.MultiIndex.from_tuples(
            [(2020, 'A'), (2020, 'B'), (2021, 'A'), (2021, 'B')],
            names=['Year', 'Product']
        )
        expected = pd.DataFrame({
            ('Sales', 'North'): [100, 0, 200, 0],
            ('Sales', 'South'): [0, 150, 0, 250],
            ('Profit', 'North'): [20, 0, 40, 0],
            ('Profit', 'South'): [0, 30, 0, 50]
        }, index=expected_index)
        expected.columns.names = [None, 'Region']
        pd.testing.assert_frame_equal(result, expected)

    def test_pivot_with_margins_and_one_value(self):
        # Test pivoting with margins
        result = pivot_to(self.df, values=['Sales'], columns=['Region'], margins=True, margins_name='Total')
        expected_index = pd.MultiIndex.from_tuples(
            [(2020, 'A', 20), (2020, 'B', 30), (2021, 'A', 40), (2021, 'B', 50), ('Total', '', '')],
            names = ['Year', 'Product', 'Profit']
        )
        expected = pd.DataFrame({
            ('Sales', 'North'): [100, 0, 200, 0, 300],
            ('Sales', 'South'): [0, 150, 0, 250, 400],
            ('Sales', 'Total'): [100, 150, 200, 250, 700]
        }, index=expected_index)
        expected.columns.names = [None, 'Region']
        pd.testing.assert_frame_equal(result, expected)

    def test_pivot_multiple_values(self):
        # Test pivoting with multiple values
        result = pivot_to(self.df, values=['Sales', 'Profit'], columns=['Region'])
        expected_index = pd.MultiIndex.from_tuples(
            [(2020, 'A'), (2020, 'B'), (2021, 'A'), (2021, 'B')],
            names=['Year', 'Product']
        )
        expected = pd.DataFrame({
            ('Sales', 'North'): [100, 0, 200, 0],
            ('Sales', 'South'): [0, 150, 0, 250],
            ('Profit', 'North'): [20, 0, 40, 0],
            ('Profit', 'South'): [0, 30, 0, 50]
        }, index=expected_index)
        expected.columns.names = [None, 'Region']
        pd.testing.assert_frame_equal(result, expected)


if __name__ == '__main__':
    unittest.main()
