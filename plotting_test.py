import pandas as pd
import csv
import json
import bokeh
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.sampledata.us_states import data as us_states

def main():
    df = pd.read_csv('stripped2_guns.csv')
    pdf = pd.read_csv('participants_untangled_v3.csv')
    states_df = pd.read_csv('populations_stats.csv')
    #months = datum_prep(df)
    #bar(months)
    #killed_per_state = states_data(df, states_df, 'state', 'n_killed')
    #plot_states(killed_per_state)
    #killed = killed_prep(df)
    #histogram(killed)
    suicides(df, "date", "incident_characteristics")
    #ages_df = pd.read_csv('part_ages.csv')
    #boxplot(ages_df)
    

def datum_prep(df):
    # convert date to right format
    df['date'] =  pd.to_datetime(df['date'], yearfirst= True )

    # group n_killed by year and compute sum, mean and maximum
    years = df.groupby(df['date'].dt.year)['n_killed'].agg(['sum'])
    list_years = years.values.tolist()
    print(list_years)
    return(list_years)

def bar(values):
    output_file("bars_years.html")

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    years = ['2013', '2014','2015', '2016', '2017', '2018']
    p = figure(x_range=years, plot_height=250, title="Deaths per year")
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
        pop = int(pop)    
        relative_n_killed = int(pop/states_dict[state])
        relative_list.append(relative_n_killed)
    relative_state_dict = dict(zip(state_names, relative_list))
        # state_population = df_states["GEO.display-label" == state]["respop72017"]
        # print (state, row)
    # vind state + population in states_df
        # relatieve waarde
    return(relative_state_dict)


def plot_states(state_dict):
    output_file("fatalities_per_state_rel.html")
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
        if fatalities <= 2500:
            color = "#e60000"
            state_color.append(color)
            print (fatalities, state_name)
        elif fatalities <= 5000:
            color = "#ff3333"
            state_color.append(color)
        elif fatalities <= 7500:
            color = "#ff6600"
            state_color.append(color)
        elif fatalities <= 10000:
            color = "#ff8c1a"
            state_color.append(color)
        elif fatalities <= 15000:
            color = "#ffd633"
            state_color.append(color)
        else:
            color = "#ffff66"
            
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

def suicides(df, column, column1):
    # alle key words nog in loop
    
    death_type_month = []
    df['date'] =  pd.to_datetime(df['date'], yearfirst= True)    
    key_words = ['Mass Shooting', 'Gang', 'robbery', 'Domestic', 'Home Invasion', 'Drive-by', 'Suicide']
    for word in key_words:
        df_ = df[df[column1].str.contains(word, na = False)]
        deaths_per_type = df_.groupby(df_['date'].dt.month)['n_killed'].agg('sum') #.count()
        death_type_list.append(deaths_per_type.values)
    # returned lijst van lijsten, elke lijst aantal doden per maand voor type ongeval
    return(death_type_month)

    






if __name__ == "__main__":
    main()