import pandas as pd
import csv
import json
import numpy as np


def main():
    dtypes = {'city_or_county': object, 'participant_age': object, 'participant_gender' : object, 'participant_status' : object, 'participant_type' : object}
    df = pd.read_csv('guns.csv')
    ndf = pd.read_csv('stripped2_guns.csv', dtype = dtypes)
    # remove(ndf)
    # sufficient_data(ndf, "state")
    # string_to_int(ndf, "city_or_county")
    # string_to_int(ndf, "state")
    # edit_csv(ndf, "state")
    # edit_csv(ndf, "city_or_county")
    # header('stripped2_guns.csv')
    list_of_dict = participant_untangle(ndf, 'participant_age', 'participant_gender', 'participant_type')
    write_to_csv(list_of_dict)
    
    

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

def write_to_csv(list):
    df = pd.DataFrame(list)
    df.to_csv("participants_untangled.csv", index = False)

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



def participant_untangle(df, column1, column2, column3):
    list1 = []
    n = len(open("stripped2_guns.csv").readlines())
    print(n)
    for i in range(n-1):
        row1 = df[column1][i]
        row2 = df[column2][i]
        row3 = df[column3][i]
        # check of waarde niet NaN is en zo nee; verander syntax van de inhoud
        if pd.notna(df[column1].iloc[i]):
            if "::" in row1:
                row1 = '{"' + row1.replace('||', '", "').replace('::', '":"') + '"}'
            else:
                row1 = '{"' + row1.replace('|', '", "').replace(':', '":"') + '"}'
            h1 = json.loads(row1)
        if pd.notna(df[column2].iloc[i]):
            if "::" in row2:
                row2 = '{"' + row2.replace('||', '", "').replace('::', '":"') + '"}'
            else:
                row2 = '{"' + row2.replace('|', '", "').replace(':', '":"') + '"}'
            h2 = json.loads(row2)
        if pd.notna(df[column3].iloc[i]):
            if "::" in row3:
                row3 = '{"' + row3.replace('||', '", "').replace('::', '":"') + '"}'
            else:
                row3 = '{"' + row3.replace('|', '", "').replace(':', '":"') + '"}'
            h3 = json.loads(row3)
        #else:
            #if pd.notna(df[column1].iloc[i]):
                #row1 = '{"' + row1.replace('|', '", "').replace(':', '":"') + '"}'
                #h1 = json.loads(row1)
            #if pd.notna(df[column2].iloc[i]):
                #row2 = '{"' + row2.replace('|', '", "').replace(':', '":"') + '"}'
                #h2 = json.loads(row2)
            #if pd.notna(df[column3].iloc[i]):
                #row3 = '{"' + row3.replace('|', '", "').replace(':', '":"') + '"}'
                #h3 = json.loads(row3)

        merged_dict = {}

        # kijk hoe lang de langste lijst is zodat je langs alle keys gaat
        for key in set(list(h1.keys()) + list(h2.keys()) + list(h3.keys())):
            try:
                merged_dict.setdefault(key,[]).append(h1[key])        
            except KeyError:
                pass
            try:
                merged_dict.setdefault(key,[]).append(h2[key])          
            except KeyError:
                pass
            try:
                merged_dict.setdefault(key,[]).append(h3[key])          
            except KeyError:
                pass
        list1.append(merged_dict)
        if (i % 1000==0):
            print(i)
    return(list1)
        
    

if __name__ == "__main__":
    main()
