def set_chart_size_and_position(chart):
    chart.set_size({'width': 1600, 'height': 600})  # Doubled the width
    chart.set_plotarea(
        {
            'layout': {
                'x'     : 0.05,
                'y'     : 0.1,
                'width' : 0.9,
                'height': 0.7
                },
            'border': {'color': '#D9D9D9', 'width': 1},
            'fill'  : {'color': '#F2F2F2'}
            }
        )


def set_chart_title(chart, title):
    chart.set_title(
        {
            'name'     : title,
            'name_font': {
                'name' : 'Calibri',
                'color': '#262626',
                'size' : 18,
                'bold' : True
                },
            'overlay'  : False
            }
        )


def set_axis_as_date(chart, axis, title):
    attrs = {
        'name'           : title if title else None,
        'name_font'      : {
            'name' : 'Calibri',
            'size' : 12,
            'color': '#595959',
            'bold' : True
            },
        'num_font'       : {'name': 'Calibri', 'size': 10, 'color': '#595959'},
        'line'           : {'color': '#D9D9D9', 'width': 1.25},
        'major_gridlines': {'visible': True, 'line': {'color': '#D9D9D9'}},
        'minor_gridlines': {'visible': False},
        'major_tick_mark': 'outside',
        'minor_tick_mark': 'none',
        'text_rotation'  : 90,
        'position_axis'  : 'on_tick',
        'crossing'       : 'min',
        'date_axis'      : True,
        'num_format'     : '[$-en-US]mmm-yyyy;@',
        'label_position' : 'nextTo',
        'visible'        : True
        }

    if axis == "x":
        chart.set_x_axis(attrs)
    else:
        chart.set_y_axis(attrs)


def get_unit_format(units):
    if units == "dollars":
        return '\\$#,##0.00'

    if units == "thousands":
        return '\\$#,##0,.0'

    if units == "millions":
        return '\\$#,##0,,.00'


def set_axis_as_dollars(chart, axis, title, units = "thousands"):
    fmt = get_unit_format(units)

    attrs = {
        'name'           : title if title else None,
        'name_font'      : {
            'name' : 'Calibri',
            'size' : 12,
            'color': '#595959',
            'bold' : True
            },
        'num_font'       : {'name': 'Calibri', 'size': 10, 'color': '#595959'},
        'line'           : {'color': '#D9D9D9', 'width': 1.25},
        'major_gridlines': {'visible': True, 'line': {'color': '#D9D9D9'}},
        'minor_gridlines': {'visible': False},
        'num_format'     : fmt,
        'major_tick_mark': 'outside',
        'minor_tick_mark': 'none',
        'crossing'       : 'min',
        'visible'        : True  # Explicitly set axis visibility
        }

    if axis == "x":
        chart.set_x_axis(attrs)
    else:
        chart.set_y_axis(attrs)


def set_legend_style(chart):
    chart.set_legend(
        {
            'position': 'bottom',
            'font'    : {'name': 'Calibri', 'size': 10, 'color': '#595959'},
            'layout'  : {'x': 0.1, 'y': 0.85, 'width': 0.8, 'height': 0.1},
            'border'  : {'none': True}
            }
        )


def set_chart_area_style(chart):
    chart.set_chartarea(
        {
            'border': {'color': '#D9D9D9', 'width': 1},
            'fill'  : {'color': '#FFFFFF'}
            }
        )
