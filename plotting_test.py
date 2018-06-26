import pandas as pd
import numpy as np
import csv
import json
import ast
import bokeh
from bokeh.palettes import Viridis256 as palette
from bokeh.io import output_file, show
from bokeh.plotting import figure, ColumnDataSource
from bokeh.sampledata.us_states import data as us_states
from bokeh.core.properties import value
from random import randint
from bokeh.models import LinearColorMapper, ColorBar, HoverTool
import itertools
from itertools import islice



def main():
    df = pd.read_csv('stripped2_guns.csv')
    pdf = pd.read_csv('participants_untangled_v3.csv')
    states_df = pd.read_csv('populations_stats.csv')
    #scatter_prep(pdf)
    #deaths_per_month = datum_prep(df)
    # bar(months)
    killed_per_state = states_data(df, states_df, 'state', 'n_killed')
    plot_states(killed_per_state)
    #killed = killed_prep(df)
    #histogram(killed)
    #types, total_month_list_p = death_types(df, "date", "incident_characteristics")
    #types, death_type_state = death_types(df, "state", "incident_characteristics")        
    #ages_df = pd.read_csv('part_ages.csv')
    #stacked_chart(types, total_month_list_p)

def datum_prep(df):
    # convert date to right format
    df['date'] =  pd.to_datetime(df['date'], yearfirst= True )
    # group n_killed by year and compute sum, mean and maximum
    time_period = df.groupby(df['date'].dt.month)['n_killed'].agg(['sum'])
    list_time_period = [item for value in time_period.values for item in value]
    return(list_time_period)

def bar(values):
    output_file("bars_years.html")

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    years = ['2013', '2014','2015', '2016', '2017', '2018']
    p = figure(x_range=months, plot_height=250, title="Deaths per year")
    p.vbar(x=years, top=values, width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    show(p)

def states_data(df, df_states, column, column1):
    states = df.groupby(df[column])[column1].agg(['sum'])
    state_names = states.index.values
    # get n_killed
    values = [item for value in states.values for item in value]
    # create dict met state name, n_killed
    states_dict = dict(zip(state_names, values))

    relative_list = []
    for state in state_names:
        pop = df_states.loc[df_states["GEO.display-label"] == state]["respop72017"].values
        pop = int(pop[0])    
        relative_n_killed = float(100000/(pop/states_dict[state]))
        relative_n_killed = round(relative_n_killed, 3)
        relative_list.append(relative_n_killed)
    relative_state_dict = dict(zip(state_names, relative_list))
    


    # relatieve waarde
    return(relative_state_dict)


def plot_states(state_dict):
    palette.reverse()
    output_file("fatalities_per_state_rel.html")
    # hawaii en alaska weggehaald want dat fockte mn kaart op
    del us_states["HI"]
    del us_states["AK"]
    # vind long/lat van staten
    state_lons = [us_states[code]["lons"] for code in us_states]
    state_lats = [us_states[code]["lats"] for code in us_states]
    state_names = [us_states[code]["name"] for code in us_states]
    state_fatalities = []
    for state_name in state_names:
        amount = state_dict[state_name]
        state_fatalities.append(amount)
    color_mapper = {}
    color_mapper = LinearColorMapper(palette=palette, low = 5, high = 50)

    t = sorted(zip(state_fatalities, state_lons, state_lats, state_names))

    state_lons = [x for _, x, _, _ in t]
    state_lats = [x for _, _, x, _ in t]
    state_names = [x for _, _, _, x in t]
    state_fatalities = [x for x, _, _, _ in t]

    data = dict(
        x = state_lons,
        y = state_lats,
        name = state_names,
        rate = state_fatalities
    )

    color_mapper.low_color = 'blue'
    color_mapper.high_color = 'red'

    TOOLS = "pan,wheel_zoom,reset,hover,save"

    p = figure(
        title="Fatalities per 100.000 inhabitants",
        tools=TOOLS, 
        toolbar_location="left", x_axis_location = None, 
        y_axis_location = None,
        )

    p.grid.grid_line_color = None
    #p.hover.point_policy = "follow_mouse"   

    color_bar = ColorBar(color_mapper=color_mapper, location=(0,0))
    p.add_layout(color_bar, 'right')

    p.grid.grid_line_color = None

    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [("State", "@name"), ("Gun deaths per 100k", "@rate"), ("(Long, Lat)", "($x, $y)")]
    hover.point_policy = "follow_mouse"
    p.patches(
        'x', 'y', 
        source = data, 
        fill_color={'field' : 'rate', 'transform' : color_mapper},
        fill_alpha=0.7,
        line_color="white", line_width=0.5, line_alpha=0.3,
        )
    

    show(p)

def killed_prep(df):
    killed = df['n_killed'].value_counts()
    dictionary = dict(zip(killed.index.values, killed.values))
    print(dictionary)
    count = 0
    killed = df['n_killed'].value_counts()
    for key, value in dictionary.items():
        if key >= 5:
            count += value * key
    dict_new = {key: key*value for key, value in dictionary.items() if key > 0 and key <= 4}
    dict_new['5_and_up'] = count
    print(dict_new)
    return dict_new
    
def histogram(killed):
    output_file("histogram.html")

    numbers = ['1','2','3','4','5+']
    y = list(killed.values())

    p = figure(x_range=numbers, plot_height=250, title="Total deaths per death toll", x_axis_label = "Fatalities per incident",
        y_axis_label = "Total fatalities")
    
    p.vbar(x=numbers, top=y, width=0.9)


    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    show(p)

def death_types(df, gb_column, column1): 
    states = {}
    keywords = ['Suicide', 'Domestic', 'Bar', 'Mass Shooting', 'Gang', 'robbery', 'School', 'Home Invasion', 'Drive-by', 'Drug involvement', 'House party']
    death_type_list = []
    if gb_column == 'date':
        df[gb_column] =  pd.to_datetime(df[gb_column], yearfirst= True)
    for word in keywords:
        # zoek keywords
        df_ = df[df[column1].str.contains(word, na = False)] 
        # voor maand/jaar indeling 
        if gb_column == 'date':
            deaths_per_type = df_.groupby(df_[gb_column].dt.month)['n_killed'].agg('sum')
            death_type_list.append(deaths_per_type.values)
            
        # voor staten
        elif gb_column == 'state':
            deaths_per_type = df_.groupby(df_[gb_column])['n_killed'].agg('sum')

            # dictionary met staten en nested dictionary met types per staat
            for state in deaths_per_type.index.values:
                if state not in states:
                    states[state] = {}
                    states[state][word] = deaths_per_type.loc[state]
                else:
                    states[state][word] = deaths_per_type.loc[state]

    # percentages van type per staat
    for state, death_types in states.items():
        total_per_state = sum(death_types.values())
        for key, value in states[state].items():
            value /= float(total_per_state)
            states[state][key] = round(value, 3)


    if gb_column == 'date':
        total_month_list = []
        # per maand
        for i in range(len(deaths_per_type.values)):
            death_list_month = []
            for death_type in death_type_list:
                death_list_month.append(death_type[i])
            total_month_list.append(np.sum(death_list_month))
        
        total_month_list_percentage = []
        for k in range(11):
            month_list_percentage = []
            for i in range(len(deaths_per_type.values)):
                percentage = float(death_type_list[k][i]/total_month_list[i])
                month_list_percentage.append(round(percentage, 3))
            total_month_list_percentage.append(month_list_percentage)
        
        # returned lijst van lijsten, elke lijst is het percentage van het totaal aantal doden per type per maand
        return(keywords, total_month_list_percentage)
    else:
        print(states)
        return(keywords, states)



def stacked_chart(death_types, death_list):
    output_file("stacked_years.html")

    if len(death_list[0]) > 6:
        x_axis_labels = ['Jan', 'Feb', 'Mrt', 'Apr', 'Mei', 'Juni', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dec']
        output_file("stacked_months.html")
    else:
        output_file("stacked_years.html")
        x_axis_labels = ['2013', '2014', '2015', '2016', '2017', '2018']

    colors = ["#c9d9d3", "#718dbf", "#e84d60", "#e60000", "#7FFF00", "#0000FF", "#FF8C00", "#9400D3", "#ffd633", "#ffff66", "#ff8c1a"]


    data = {'Months' : x_axis_labels,
            death_types[0]   : death_list[0],
            death_types[1]   : death_list[1],
            death_types[2]   : death_list[2],
            death_types[3]   : death_list[3],
            death_types[4]   : death_list[4],
            death_types[5]   : death_list[5],
            death_types[6]   : death_list[6],
            death_types[7]   : death_list[7],
            death_types[8]   : death_list[8],
            death_types[9]   : death_list[9],
            death_types[10]  : death_list[10]}
    
    source = ColumnDataSource(data=data)

    p = figure(x_range=x_axis_labels, plot_height=400, title="Causes of deaths",
            toolbar_location=None, tools="")

    rs = p.vbar_stack(death_types, x='Months', width=0.9, color=colors, source=source)
                    #legend=[value(x) for x in death_types])



    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    #p.legend.location = "top_right"
    #p.legend.orientation = "horizontal"

    legend = Legend(items=[(death, [r]) for (death, r) in zip(death_types, rs)], location=(0, 30))
    p.add_layout(legend, 'right')

    show(p)

def plot_scatter(p, x, y):
    p.scatter(x, y, size=2, line_color="navy", fill_color="orange", alpha=0.5)
    
def scatter_prep(df):
    
    # lijst voor alle victim/perp paren
    all_pairs = []
    # iterate through incidents
    for index, row in islice(df.iterrows(), 0, None):
        # nieuwe victim/perp lijsten voor elk incident
        age_list_victim = []
        age_list_perp = []
        #iterate through participants
        for cell in row:  
            if pd.isna(cell):
                for victim_age in age_list_victim:
                    for perp_age in age_list_perp:
                        # koppel victim_age aan perp_age voor alle deelnemers van incident
                        pair = [victim_age, perp_age]
                        all_pairs.append(pair)
                # volgende incident
                break
            else:    
                cell = ast.literal_eval(cell)
                try:
                    age = int(cell[0])
                    if "Victim" in cell:
                        age_list_victim.append(age)
                    elif "Subject-Suspect" in cell:
                        age_list_perp.append(age)
                except:
                    continue

    p = figure(title="Age victim against age perpetrator", toolbar_location=None, x_axis_label='Age victim', y_axis_label='Age perpetrator')
    p.grid.grid_line_color = None
    p.background_fill_color = "#eeeeee"
    for i in range(500):
        random = randint(0, 49511)
        plot_scatter(p, all_pairs[random][0], all_pairs[random][1])
    show(p)
    output_file("scatterplot.html")

if __name__ == "__main__":
    main()