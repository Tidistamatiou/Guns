import pandas as pd
import csv
import json
import numpy as np


def main():
    dtypes = {'city_or_county': object, 'participant_age': object, 'participant_gender' : object, 'participant_status' : object, 'participant_type' : object}
    df = pd.read_csv('guns.csv')
    ndf = pd.read_csv('stripped2_guns.csv', dtype = dtypes)
    remove(ndf)
    # sufficient_data(ndf, "state")
    # string_to_int(ndf, "city_or_county")
    # string_to_int(ndf, "state")
    # edit_csv(ndf, "state")
    # edit_csv(ndf, "city_or_county")
    # header('stripped2_guns.csv')

def header(csv_file):
    headers = pd.read_csv(csv_file, nrows = 1).columns
    for i in range(20):
        print(headers[i])


def string_to_int(df, column):
    dict = {} 
    counter = 0
    # alle staten in dictionary met int key
    for row in df[column]:      
        if row not in dict.values():
            dict[counter] = row
            counter+=1
    save_dic(dict, column)

def edit_csv(df, column):
    # haal correcte dict op
    with open(column+"_dict.txt") as file:
        d = file.read() 
        dict_file = json.loads(d)
    # wissel key en value 
    inv_dict_file = {v: k for k, v in dict_file.items()}    

    # voeg id voor kolom aan df toe
    df_column = pd.DataFrame.from_dict(inv_dict_file, orient = 'index')
    df_column.rename(columns = {0:column+"_id"}, inplace = True)
    df = pd.DataFrame.merge(df, df_column, how = 'left', left_on= column, right_on= None , right_index=True )
    df.to_csv("stripped2_guns.csv", index = False)

# sla dict op in apart textbestand
def save_dic(dictionary, column):
    with open(column+"_dict.txt", 'w') as file:
        file.write(json.dumps(dictionary))

def sufficient_data(df, column):
    counter_row = 0
    row_count = df.count(axis=0)
    for row in df[column]:
        counter_row += 1
    print(counter_row)
    percentage = round(((row_count/counter_row)*100),2)
    print(percentage)

# alleen nuttige kollomen worden behouden
# alles wat volgens def sufficient_data onder 60% is, is verwijdert
def remove(df):
    keep_col = ['incident_id', 'date', 'state', 'city_or_county', 'n_killed', 'n_injured', 'congressional_district', 'incident_characteristics', 'latitude', 'longitude', 'n_guns_involved', 'participant_age', 'participant_gender', 'participant_type', 'state_house_district', 'state_senate_district', 'state_id', 'city_or_county_id']
    df = df[keep_col]
    df.to_csv('stripped2_guns.csv', index = False)

if __name__ == "__main__":
    main()
