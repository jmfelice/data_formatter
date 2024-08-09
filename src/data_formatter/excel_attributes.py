import pandas as pd
from xlsxwriter.utility import xl_rowcol_to_cell, xl_cell_to_rowcol


def set_cell_dimensions(w, sheet_name, row_height, column_width):
    w.sheets[sheet_name].set_column_pixels(0, 1000, column_width)
    for i in range(1000):
        w.sheets['charts'].set_row_pixels(i, row_height)


def remove_absolute_notation(cell_ref):
    return cell_ref.replace('$', '')


def add_absolute_notation(cell_ref):
    if '$' in cell_ref:
        return cell_ref
    col, row = cell_ref[0], cell_ref[1:]
    return f'${col}${row}'


def get_chart_attributes(
        startcol = 0,
        startrow = 0,
        chart_height = 600,
        chart_width = 1600,
        row_height = 24,
        column_width = 80
        ):
    endcol = round(startcol + (chart_width / column_width)) - 1
    endrow = round(startrow + (chart_height / row_height)) - 1

    chart_attrs = {
        'startcol'  : startcol,
        'startrow'  : startrow,
        'endcol'    : endcol,
        'endrow'    : endrow,
        'start_cell': xl_rowcol_to_cell(
            startrow,
            startcol,
            row_abs = True,
            col_abs = True
            ),
        'end_cell'  : xl_rowcol_to_cell(endrow, endcol, row_abs = True, col_abs = True),
        'cell_range': get_cell_range(startrow, endrow, startcol, endcol)
        }

    return chart_attrs


def get_dataframe_attributes(df, startcol, startrow):
    if isinstance(df, pd.io.formats.style.Styler):
        df = df.data

    table_attrs = {}

    # Check if index and columns are MultiIndex
    index_is_multi = isinstance(df.index, pd.MultiIndex)
    columns_is_multi = isinstance(df.columns, pd.MultiIndex)

    # Number of levels in index and columns
    index_levels = df.index.nlevels - 1
    col_levels = df.columns.nlevels - 1

    # End column and row calculations
    endcol = startcol + df.shape[1] + index_levels
    endrow = startrow + df.shape[0] + col_levels

    # there is a blank space added to pivot tables between the column headers and the data
    if columns_is_multi:
        endrow = endrow + 1

    # Index and columns start and end positions
    index_startcol = startcol
    index_startrow = startrow + col_levels + 2 if columns_is_multi else startrow + col_levels
    index_endcol = startcol + index_levels
    index_endrow = endrow

    columns_startcol = startcol + index_levels + 1
    columns_startrow = startrow
    columns_endcol = endcol + index_levels
    columns_endrow = startrow + col_levels

    # Names of each level for index and columns
    index_level_names = df.index.names if index_is_multi else [df.index.name]
    columns_level_names = df.columns.names if columns_is_multi else [df.columns.name]

    # Adding attributes to the dictionary
    table_attrs['startcol'] = startcol
    table_attrs['startrow'] = startrow
    table_attrs['endcol'] = endcol
    table_attrs['endrow'] = endrow
    table_attrs['start_cell'] = xl_rowcol_to_cell(
        startrow,
        startcol,
        row_abs = True,
        col_abs = True
        )
    table_attrs['end_cell'] = xl_rowcol_to_cell(endrow, endcol, row_abs = True, col_abs = True)
    table_attrs['cell_range'] = get_cell_range(startrow, endrow, startcol, endcol)

    table_attrs['index_is_multi'] = index_is_multi
    table_attrs['index_level_names'] = index_level_names
    table_attrs['index_levels'] = index_levels + 1
    table_attrs['index_startcol'] = index_startcol
    table_attrs['index_startrow'] = index_startrow
    table_attrs['index_endcol'] = index_endcol
    table_attrs['index_endrow'] = index_endrow
    table_attrs['index_start_cell'] = xl_rowcol_to_cell(
        index_startrow,
        index_startcol,
        row_abs = True,
        col_abs = True
        )
    table_attrs['index_end_cell'] = xl_rowcol_to_cell(
        index_endrow,
        index_endcol,
        row_abs = True,
        col_abs = True
        )
    table_attrs['index_cell_range'] = get_cell_range(
        index_startrow,
        index_endrow,
        index_startcol,
        index_endcol
        )

    table_attrs['columns_is_multi'] = columns_is_multi
    table_attrs['columns_level_names'] = columns_level_names
    table_attrs['columns_levels'] = col_levels + 1
    table_attrs['columns_startcol'] = columns_startcol
    table_attrs['columns_startrow'] = columns_startrow
    table_attrs['columns_endcol'] = columns_endcol
    table_attrs['columns_endrow'] = columns_endrow
    table_attrs['columns_start_cell'] = xl_rowcol_to_cell(
        columns_startrow,
        columns_startcol,
        row_abs = True,
        col_abs = True
        )
    table_attrs['columns_end_cell'] = xl_rowcol_to_cell(
        columns_endrow,
        columns_endcol,
        row_abs = True,
        col_abs = True
        )
    table_attrs['columns_cell_range'] = get_cell_range(
        columns_startrow,
        columns_endrow,
        columns_startcol,
        columns_endcol
        )

    table_attrs['data_startcol'] = columns_startcol
    table_attrs['data_startrow'] = index_startrow
    table_attrs['data_endcol'] = columns_endcol
    table_attrs['data_endrow'] = index_endrow
    table_attrs['data_start_cell'] = xl_rowcol_to_cell(
        index_startrow,
        columns_startcol,
        row_abs = True,
        col_abs = True
        )
    table_attrs['data_end_cell'] = xl_rowcol_to_cell(
        index_endrow,
        columns_endcol,
        row_abs = True,
        col_abs = True
        )
    table_attrs['data_cell_range'] = get_cell_range(
        index_startrow,
        index_endrow,
        columns_startcol,
        columns_endcol
        )

    return table_attrs


def generate_cell_series_from_range(range_string, horizontal = True, absolute = True):
    if '!' in range_string:
        range_string = range_string.split('!')[1]

    start, end = range_string.split(':')
    start_row, start_col = xl_cell_to_rowcol(start)
    end_row, end_col = xl_cell_to_rowcol(end)

    # Generate the series
    series = []

    if not horizontal:
        for col in range(start_col, end_col + 1):
            if absolute:
                start_cell = xl_rowcol_to_cell(start_row, col, row_abs = True, col_abs = True)
                end_cell = xl_rowcol_to_cell(end_row, col, row_abs = True, col_abs = True)
            else:
                start_cell = xl_rowcol_to_cell(start_row, col)
                end_cell = xl_rowcol_to_cell(end_row, col)
            series.append(f"{start_cell}:{end_cell}")
    else:
        for row in range(start_row, end_row + 1):
            if absolute:
                start_cell = xl_rowcol_to_cell(row, start_col, row_abs = True, col_abs = True)
                end_cell = xl_rowcol_to_cell(row, end_col, row_abs = True, col_abs = True)
            else:
                start_cell = xl_rowcol_to_cell(row, start_col)
                end_cell = xl_rowcol_to_cell(row, end_col)
            series.append(f"{start_cell}:{end_cell}")

    return series


def generate_specific_range(range_string, row = None, col = None, absolute = True):
    range_string = remove_absolute_notation(range_string)

    # Split the range into sheet name and cell range
    if '!' in range_string:
        sheet_name, cell_range = range_string.split('!')
        sheet_name = sheet_name.strip("'")
    else:
        cell_range = range_string

    # Split the cell range into start and end cells
    start, end = cell_range.split(':')

    # Convert start and end cells to row and column indices
    start_row, start_col = xl_cell_to_rowcol(start)
    end_row, end_col = xl_cell_to_rowcol(end)

    # Generate the new range based on the specified row or column
    if row is not None:
        if row < 0 or row > (end_row - start_row):
            raise ValueError("Row index out of range")
        new_start_cell = xl_rowcol_to_cell(
            start_row + row,
            start_col,
            row_abs = True,
            col_abs = True
            )
        new_end_cell = xl_rowcol_to_cell(start_row + row, end_col, row_abs = True, col_abs = True)
    elif col is not None:
        if col < 0 or col > (end_col - start_col):
            raise ValueError("Column index out of range")
        new_start_cell = xl_rowcol_to_cell(
            start_row,
            start_col + col,
            row_abs = True,
            col_abs = True
            )
        new_end_cell = xl_rowcol_to_cell(end_row, start_col + col, row_abs = True, col_abs = True)
    else:
        raise ValueError("Either row or col must be specified")

    if absolute:
        new_start_cell = add_absolute_notation(new_start_cell)
        new_end_cell = add_absolute_notation(new_end_cell)

    # Return the new range with the sheet name
    if '!' in range_string:
        result = f"'{sheet_name}'!{new_start_cell}:{new_end_cell}"
    else:
        result = f"{new_start_cell}:{new_end_cell}"

    return result


def get_cell_range(startrow, endrow, startcol, endcol, absolute = True):
    start_cell = xl_rowcol_to_cell(startrow, startcol, row_abs = absolute, col_abs = absolute)
    end_cell = xl_rowcol_to_cell(endrow, endcol, row_abs = absolute, col_abs = absolute)
    return f'{start_cell}:{end_cell}'


def get_dataframe_cell_range(df, startrow, startcol, absolute = True):
    if isinstance(df, pd.io.formats.style.Styler):
        df = df.data
    no_of_rows = df.shape[0]
    no_of_cols = df.shape[1]
    no_of_index_levels = 0 if len(df.index.names) <= 1 else len(df.index.names)
    no_of_column_levels = 0 if len(df.columns.names) <= 1 else len(df.columns.names)
    endcol = startcol + no_of_cols + no_of_index_levels
    endrow = startrow + no_of_rows + no_of_column_levels
    return get_cell_range(startrow, endrow, startcol, endcol, absolute = absolute)
