import pandas as pd
import csv
import json
import ast
import bokeh
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.sampledata.us_states import data as us_states
import time
start_time = time.time()

def main():
    df = pd.read_csv('stripped2_guns.csv')
    pdf = pd.read_csv('participants_untangled.csv')
    #months = datum_prep(df)
    #bar(months)
    #killed_per_state = states_data(df, 'state', 'n_killed')
    #plot_states(killed_per_state)
    #killed = killed_prep(df)
    #histogram(killed)
    #ages_df = pd.read_csv('part_ages.csv')
    #boxplot(ages_df)
    suicide_data = suicide_prep(df)
    #suicide(suicide_data)


def datum_prep(df):
    # convert date to right format
    df['date'] =  pd.to_datetime(df['date'], yearfirst= True )

    # group n_killed by year and compute sum, mean and maximum
    months = df.groupby(df['date'].dt.month)['n_killed'].agg(['sum'])
    list_months = months.values.tolist()
    print(list_months)
    return(list_months)

def bar(values):
    output_file("bars.html")

    months = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

    p = figure(x_range=months, plot_height=250, title="Deaths per month")
    p.vbar(x=months, top=values, width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    show(p)

def states_data(df, column, column1):
    states = df.groupby(df[column])[column1].agg(['sum'])
    state_names = states.index.values
    # get n_killed
    values = [item for value in states.values for item in value]
    # create dict met state name, n_killed
    states_dict = dict(zip(state_names, values))
    return(states_dict)

def plot_states(state_dict):
    output_file("fatalities_per_state.html")
    # hawaii en alaska weggehaald want dat fockte mn kaart op
    del us_states["HI"]
    del us_states["AK"]

    # vind long/lat van staten
    state_lon = [us_states[code]["lons"] for code in us_states]
    state_lat = [us_states[code]["lats"] for code in us_states]
    
    # koppel state_name uit bokeh aan n_killed
    state_color = []
    for state_id in us_states:
        state_name = us_states[state_id]["name"]
        fatalities = state_dict[state_name]
        if fatalities <= 100:
            color = "#ffff66"
            state_color.append(color)
        elif fatalities <= 1000:
            color = "#ffd633"
            state_color.append(color)
        elif fatalities <= 2000:
            color = "#ff8c1a"
            state_color.append(color)
        elif fatalities <= 3000:
            color = "#ff6600"
            state_color.append(color)
        elif fatalities <= 4000:
            color = "#ff3333"
            state_color.append(color)
        else:
            color = "#e60000"
            state_color.append(color)           

    map = figure(title="Fatalities per state", toolbar_location="left",
        plot_width=1000, plot_height=800)

    map.patches(state_lon, state_lat, fill_alpha=0.7, fill_color=state_color, 
        line_color="#884444", line_width=2, line_alpha=0.3)

    show(map)

def killed_prep(df):
    killed = df['n_killed'].value_counts()
    dictionary = dict(zip(killed.index.values, killed.values))
    print(dictionary)
    count = 0
    killed = df['n_killed'].value_counts()
    for key, value in dictionary.items():
        if key >= 5:
            count += value
    dict_new = {key: value for key, value in dictionary.items() if key <= 4}
    dict_new['5_and_up'] = count
    print(dict_new)
    return dict_new
    
def histogram(killed):
    output_file("histogram.html")

    y = list(killed.values())
    numbers = ['0','1','2','3','4','5+']

    p = figure(x_range=numbers, plot_height=250, title="Deaths per incident")
    p.vbar(x=numbers, top=y, width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    show(p)

def boxplot(df):
    cats = list("a")

    # find quartiles
    quartiles = df.quantile([0.25, .5, .75])
    q_list = []
    for quartile in quartiles.values:
        value = quartile[0]
        q_list.append(value)
    
    # define quartiles, iqr, upper/lower
    q1, q2, q3 = q_list[0], q_list[1], q_list[2]
    iqr = q3 - q1
    upper, lower = q3 + 1.5*iqr, q1 - 1.5*iqr
    print(q1)
    print(q2)
    print(q3)
    print(upper)
    print(lower)
    outliers = []
    for row in df["0"]:
       if row > upper or  row < lower:
            outliers.append(row)
    
    p = figure(tools="save", background_fill_color="#EFE8E2", title="Average age of all participants", x_range=cats)
    
    # stems
    p.segment(cats, upper, cats, q3, line_color="black")
    p.segment(cats, lower, cats, q1, line_color="black")

    # boxes     
    p.vbar(cats, 0.7, q2, q3, fill_color="#E08E79", line_color="black")
    p.vbar(cats, 0.7, q1, q2, fill_color="#3B8686", line_color="black")

    # whiskers (almost-0 height rects simpler than segments)
    p.rect(cats, lower, 0.2, 0.01, line_color="black")
    p.rect(cats, upper, 0.2, 0.01, line_color="black")

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = "white"
    p.grid.grid_line_width = 2
    p.xaxis.major_label_text_font_size="12pt"

    output_file("boxplot.html", title="boxplot.py example")

    show(p)

def suicide_prep(df):
    # convert date to right format
    df['date'] =  pd.to_datetime(df['date'], yearfirst= True )

    # group n_killed by year and compute sum, mean and maximum
    for row in df['incident_characteristics']:
        if 'Suicide' or 'suicide' in row:
            months = df.groupby(df['date'].dt.month)['incident_characteristics'].agg(['sum'])
    list_months = months.values.tolist()
    print(list_months)
    return(list_months)
        

#def suicide(df):




if __name__ == "__main__":
    main()