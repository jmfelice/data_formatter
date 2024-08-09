from pandas.io.formats.excel import ExcelFormatter
import pandas as pd
from .util import get_even_numbers
from itertools import repeat


def new_default_header_style():
    return {
        "font": {"bold": True, "sz": "12", "name": "Garamond"},
        "alignment": {"horizontal": "center", "vertical": "center"}
        }


def set_new_default_header_style():
    ExcelFormatter.header_style = new_default_header_style()


def format_category_level(levels):
    lvls = [int(x) for x in levels]
    lvls = [x - min(lvls) for x in lvls]
    lvl_format = [f"number-format: {('--' * x)}@" for x in lvls]
    return lvl_format


def index_format_standard(s):
    return ["text-align: left;vertical-align: middle;font-size: 12pt; font-family: Garamond;" for
            _ in s]


def column_format_standard(s):
    return ["text-align: center;vertical-align: middle;font-size: 12pt; font-family: Garamond;" for
            _ in s]


def column_format_header_0(s):
    return [("background-color: #DCE6F0; font-weight: bold; text-decoration: underline; border: "
             "1.5pt double; white-space:wrap; font-size: 18pt;") for _ in s]


def column_format_header_1(s):
    return [("background-color: #FABE8C; font-weight: bold; font-style: italic; border-bottom: "
             "1.5pt solid; white-space:wrap;") for _ in s]


def data_format_standard(s):
    return ["border: .5pt solid" for _ in s]


def data_format_dollars(s):
    return ["number-format: $#,##0.00" for _ in s]


def data_format_percent(s):
    return ["number-format: 0.0%" for _ in s]


def data_format_totals(s):
    return ["border-top: 2pt solid;" for _ in s]


def alternate_color_rows(s, dd, color = '#DCE6F0'):
    even_rows = get_even_numbers(dd.index)
    even_index = dd.index[even_rows]
    x = pd.Series(f'background-color: {color};', index = even_index)
    return x


def alternate_color_cols(s, dd, color = '#B8CCE4'):
    even_cols = get_even_numbers(dd.columns)
    even_col_values = dd.columns[even_cols]
    x = pd.Series(f'background-color: {color};', index = even_col_values)
    return x


def format_hyperlink(s):
    return [("font-weight: bold; font-style: italic; text-decoration: underline; text-align: "
             "right; color: #C00000") for _ in s]
