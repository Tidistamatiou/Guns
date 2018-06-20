from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

output_file("stacked.html")

deaths = ["Suicide", "Homicide", "Accident"]
months = ['Jan', 'Feb', 'Mrt', 'Apr', 'Mei', 'Juni', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dec']
colors = ["#c9d9d3", "#718dbf", "#e84d60"]

data = {'Months' : months,
        'Suicide'   : [2, 1, 4, 3, 2, 4, 8, 2, 3, 4, 5, 4],
        'Homicide'   : [5, 3, 4, 2, 4, 6, 4, 2, 8, 1, 3, 5],
        'Accident'   : [3, 2, 4, 4, 5, 3, 9, 7, 4, 2, 1, 4]}

source = ColumnDataSource(data=data)

p = figure(x_range=months, plot_height=250, title="Causes of deaths",
           toolbar_location=None, tools="")

p.vbar_stack(deaths, x='Months', width=0.9, color=colors, source=source,
             legend=[value(x) for x in deaths])

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "horizontal"

show(p)
