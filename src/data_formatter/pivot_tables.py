def pivot_to_standard_format(df, title = None):
    data_vales = ['amount']
    data_cols = ['duration', 'annum']

    if title is not None:
        df[title] = title
        data_cols = [title] + data_cols

    data_index = [x for x in df.columns if x not in data_vales + data_cols]

    df = df.pivot_table(
        index = data_index,
        columns = data_cols,
        values = data_vales[0],
        fill_value = 0
        )

    return df


def pivot_to_series_format(df, title = None):
    data_vales = ['amount']
    data_cols = ['duration', 'period_ending']

    if title is not None:
        df[title] = title
        data_cols = [title] + data_cols

    data_index = [x for x in df.columns if x not in data_vales + data_cols]

    df = df.pivot_table(
        index = data_index,
        columns = data_cols,
        values = data_vales[0],
        fill_value = 0
        )

    return df
