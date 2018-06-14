import pandas as pd
import csv
import bokeh
from bokeh.io import output_file, show
from bokeh.plotting import figure

def main():
    df = pd.read_csv('stripped2_guns.csv')
    months = datum_prep(df)
    bar(months)
    # line(months)

def datum_prep(df):
    # convert date to right format
    df['date'] =  pd.to_datetime(df['date'], yearfirst= True )

    # group n_killed by year and compute sum, mean and maximum
    months = df.groupby(df['date'].dt.month)['n_killed'].agg(['sum'])
    list_months = months.values.tolist()
    print(list_months)
    return(list_months)

def line(months):
    x = months["date"]
    y = months["sum"]

    # Prepare the output file
    f = output_file("Line_from_csv.html")

    # Create a figure object
    f = figure()

    # Create line plot
    f.line(x,y)

    ## Add some axis information (after all, a plot without axis descriptions is nothing more than abstract art)
    f.xaxis.axis_label="Date"
    f.yaxis.axis_label="Killed"    aangepast

    show(f)

def bar(values):
    output_file("bars.html")

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    p = figure(x_range=months, plot_height=250, title="Deaths per month")
    p.vbar(x=months, top=values, width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    show(p)




if __name__ == "__main__":
    main()
