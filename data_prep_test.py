import pandas as pd
import csv
import json
import numpy as np
import ast
import itertools 
from itertools import islice

def main():
    dtypes = {'city_or_county': object, 'participant_age': object, 'participant_gender' : object, 'participant_status' : object, 'participant_type' : object}
    # df = pd.read_csv('guns.csv')
    ndf = pd.read_csv('stripped2_guns.csv', dtype = dtypes)
    pdf = pd.read_csv('participants_untangled_v3.csv')
    # remove(ndf)
    # sufficient_data(ndf, "state")
    # string_to_int(ndf, "city_or_county")
    # string_to_int(ndf, "state")
    # dict_to_csv(ndf, "state")
    # dict_to_csv(ndf, "city_or_county")
    # header('stripped_guns.csv')
    # list = participant_untangle(ndf, 'participant_age', 'participant_gender', 'participant_type')
    # list_to_csv(list)
    # get_part_info(pdf)
    total = merge(pdf, ndf, "incident_characteristics")

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

def dict_to_csv(df, column):
    # haal correcte dict op
    with open(column+"_dict.txt") as file:
        d = file.read() 
        dict_file = json.loads(d)
    # wissel key en value 
    inv_dict_file = {v: k for k, v in dict_file.items()}    

    # voeg id voor kolom aan df toe
    df_column = pd.DataFrame.from_dict(inv_dict_file, orient = 'index')
    df_column.rename(columns = {0:column+"_id"}, inplace = True)
    df = pd.DataFrame.merge(df, df_column, how = 'left', left_on = column, right_on= None , right_index=True )
    df.to_csv("stripped2_guns.csv", index = False)

def merge(df1, df2, column):
    char_df = pd.DataFrame(df2[column])
    df = char_df.join(df1)
    keywords = ['Suicide', 'Domestic', 'School', 'Mass Shooting', 'Bar', 'House party',  'Gang', 'robbery', 'Home Invasion', 'Drive-by', 'Drug involvement']   
    total_list = []
    for word in keywords:
        df_ = df[df[column].str.contains(word, na = False)] 
        l = get_gender_info(df_)
        total_list.append(l)

    total_gender_list = []
    for i in range(len(total_list[0])):
        gender_list = []
        for l in total_list:
            gender_list.append(l[i])
        total_gender_list.append(np.sum(gender_list))
        
    for i in range(len(total_list[0])):
        for l in total_list:
            l[i] /= total_gender_list[i]
            l[i] = round(l[i], 3)
    return(total_list)
    

def list_to_csv(list):
    df = pd.DataFrame(list)
    order = []
    for i in range(103):
        i = str(i)
        order.append(i)
    df_reorder = df[order]
    df_reorder.to_csv("participants_untangled_v3.csv", index = False)

# sla dict op in apart textbestand
def save_dic(dictionary, column):
    with open(column+"_dict.txt", 'w') as file:
        file.write(json.dumps(dictionary))

def sufficient_data(df, column):
    counter_row = 0
    row_count = df.count(axis=0)
    for row in df[column]:
        counter_row += 1
    percentage = round(((row_count/counter_row)*100),2)


# alleen nuttige kollomen worden behouden
# alles wat volgens def sufficient_data onder 60% is, is verwijdert
def remove(df):
    keep_col = ['incident_id', 'date', 'state', 'city_or_county', 'n_killed', 'n_injured', 'congressional_district', 'incident_characteristics', 'latitude', 'longitude', 'n_guns_involved', 'participant_age', 'participant_gender', 'participant_type', 'state_house_district', 'state_senate_district', 'state_id', 'city_or_county_id']
    df = df[keep_col]
    df.to_csv('stripped2_guns.csv')

def participant_untangle(df, column1, column2, column3):
    list1 = []
    n = len(open("stripped2_guns.csv").readlines())
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
        else:
            h1 = {}
        if pd.notna(df[column2].iloc[i]):
            if "::" in row2:
                row2 = '{"' + row2.replace('||', '", "').replace('::', '":"') + '"}'
            else:
                row2 = '{"' + row2.replace('|', '", "').replace(':', '":"') + '"}'
            h2 = json.loads(row2)
        else:
            h2 = {}
        if pd.notna(df[column3].iloc[i]):
            if "::" in row3:
                row3 = '{"' + row3.replace('||', '", "').replace('::', '":"') + '"}'
            else:
                row3 = '{"' + row3.replace('|', '", "').replace(':', '":"') + '"}'
            h3 = json.loads(row3)
        else:
            h3 = {}

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
        if (i % 10000==0):
            print(i)
    return(list1)

def get_part_info(df):   
    age_list = []
    age_list_victim = []
    age_list_perp = []
   
    # loop door alle entries
    for index, row in islice(df.iterrows(), 0, None):
        if index % 10000 == 0:
            print(index)
        for cell in row:  
            # als Nan, volgende row 
            if pd.isna(cell):
                continue
            cell = ast.literal_eval(cell)
            try:
                age = int(cell[0])
                age_list.append(age)
                if "Victim" in cell:
                    age_list_victim.append(age)
                elif "Subject-Suspect" in cell:
                    age_list_perp.append(age)
            except:
                continue
    age_df = pd.DataFrame(age_list)
    victim_df = pd.DataFrame(age_list_victim)
    perp_df = pd.DataFrame(age_list_perp)
    age_df.to_csv("part_ages.csv")
    victim_df.to_csv("victim_ages.csv")
    perp_df.to_csv("perp_ages.csv")

def get_gender_info(df):   
    male_victim_count = 0
    female_victim_count = 0
    male_perp_count = 0
    female_perp_count = 0
    # loop door alle entries
    for index, row in islice(df.iterrows(), 0, None):
        for cell in row:  
            # als Nan, volgende row 
            if pd.isna(cell):
                break
            try:
                cell = ast.literal_eval(cell)
                if "Victim" in cell:
                    if "Male" in cell:
                        male_victim_count += 1
                    elif "Female" in cell:
                        female_victim_count += 1
                elif "Subject-Suspect" in cell:
                    if "Male" in cell:
                        male_perp_count += 1
                    elif "Female" in cell:
                        female_perp_count += 1
            except:
                continue
    type_count_list = [male_victim_count, male_perp_count, female_victim_count, female_perp_count]
    return(type_count_list)
    #victim_gender_df = pd.DataFrame(gender_list_victim)
    #perp_gender_df = pd.DataFrame(gender_list_perp)
    #victim_gender_df.to_csv("victim_gender.csv")
    #perp_gender_df.to_csv("perp_gender.csv")


if __name__ == "__main__":
    main()
