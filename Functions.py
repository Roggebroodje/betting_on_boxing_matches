# Function name_matching. Version 4 (20 january 2022), made by Rogier Hetem.
# 
# A function to check whether two strings (a and b) contain equal enough content. 
# The function is meant to compare (both) names of competing boxers between two different betting websites.
# 
# Different betting websites write names differently in regard to:
# abbreviation(s)
# order of first and last name
# usage of dots and commas (. ,)
# usage of special letters (e.g. é, ó OR  e, o)
# spelling errors
#
# two name examples:
# Josh Taylor -OR- Taylor Josh, 
# Chris Eubank Jnr -OR- Chris Eubank Jr.
#
# In general names are written with correct use of capitalization
#
# How does the function work?
# 1. removes all dots, commas, white spaces and 'or' symbols.
#
# 2. creates: 
# 'point' counter, 
# a divider based on average word length, so that we end up with a score between 0 and about 1.
# an empty string.
#
# 3. Checks per letter from string a if also present in string b, capitalization matters.
# when a capital letter from sting a matches a capital letter from string b, 1 point is added to our 'point' counter.
# when a (first) letter matches it is saved in our empty string, the following letter from string a is added.
# when a letter does not match it is not added and our temporary word string is emptied again.
# every time when two or more letters combined match, 1 point is added to 'point' counter.
#
# 4. points are divided by the 'diveder value'. This will give a 'score' between 0 and about 1.3.
# if the score higher than the set accuracy level 'True' is returned, else 'False' is returned.
#
# Testing:
# With real data from different betting websites I found that:
# If there is no real match between string a and b the highest value I seen is .38, but mostly the value stays below .25
# If there is a real match between string a and b the lowest value I seen is .86, but mostly the value stays above .95
#
# With selfmade data, with many on purpose added errors and differences I found that:
# If there is no real match between string a and b the highest value I seen is .48
# If there is a real match between string a and b the lowest value I seen is .52
#
# The function will fail when:
# both competing boxers got relatively short last names compared to their first name(s) (less than 50% letters than first name)
# both boxers first names are relatively long (more than 50% letters than last name)
# when this is the case AND
# one website uses abbreviations (always the first name(s) is shortened) and another website does not abbreviate
# in this case the function will not give enough points to the to matching names and will not detect the match.
# 
# *
# To minimaze the chance of failing, points for single matching capital letters is added. 
# As always first letters of names are written with capital letters (with or without abbreviation)
# this adds some points that can make the difference between passing the threshold for matching strings. 
# while not adding much for non-matching strings.

def name_matching(a, b, accuracy = 0.5):
    """ Both a and b must be a single string object.
    a = names of both competing boxers from website X.
    b = names of both competing boxers from website Y. 
    accuracy = threshold value (between 0 and about 1.3), to decide whether a and b contain the same names. A higher value means more overlap between strings.
    Return value is either 'True' or 'False', based on the accuracy level."""
    # 1.
    names = [a.replace('.','').replace(' ','').replace(',','').replace('|','').strip(), 
             b.replace('.','').replace(' ','').replace(',','').replace('|','').strip()]
    # 2.
    points = 0 
    divider = (len(names[0]) + len(names[1])) / 2 # average length is used as divider to get a score between 0 and 1* 
    word = ''
    # 3.
    for letter in names[0]: 
        word += letter

        if letter.isupper() and letter in names[1]: # point is given when a single cappital letter matches
            points += 1
        
        while len(word) > 1: # point is given when a combination of letters matches 
            if word in names[1]:
                points += 1
                break
            else: # if no combination is found, the first letter of word is removed and checked again for a match
                word = word[1:]
    # 4.
    return((points / divider) >= accuracy)

# Function box_joining. Version 3 (21 january 2022), made by Rogier Hetem
#
# A function to create a new data frame, using the input data frame 
# The input data frame contains the information from different betting websites
# and this function 'joins' similar rows (based on the names of the competing boxers) from the different websites 
# by putting them in the same row
#
# example:
# input data frame:
# date        , A_boxers                     , A_website,  A_boxer_1_wins, A_draw, A_boxer_2_wins  
# '16/01/2022', 'Smit Joe Jr.|Johnson Callum', 'betcity',  1,              2,      3   
# '16/01/2022', 'Johnson Callum |Smit Joe Jr ',  '365bet', 6,              5,      4 
#
# output data fame:
# date         , A_boxers                     , A_website, A_boxer_1_wins, A_draw, A_boxer_2_wins, B_website, B_boxer_1_wins, B_draw, B_boxer_2_wins
# '16/01/2022', 'Smit Joe Jr.|Johnson Callum', 'betcity',  1,              2,      3,             '365bet'    4.0             5.0     6.0   
#
# How does the function work?
# 0. importing package
#
# 1. Creating:
# variable (all_websites) containing all the unique websites names
# empty dataframe (joined_df) containing the column date, used to form a new joined dataframe
# a list (alphabet) to identify the different websites columns
#
# 2. Filling the new dataframe (joined_df)
# 2.a adding new columns to the new dataframe (joined_df) while adding a letter at the start of the column name.
# 2.b creating a new temporary data frame (temp_df) cointaining only the rows from 1 website
# 2.c adding all rows from (only) the first website, now stored in the temporary data frame (temp_df), into the new data frame (joined_df)
# 2.d adding all rows from the other websites to the new data frame.
# if there is a boxers name match the data is added into the same row as the matching boxers name.
# if there is no match the data will be added in a regular fashion as a new row 
#
# 3. the blank ('') cells are replaced in the new data frame (joined_df) by a 0 
#
# 4. checked if the order of the names is equal between websites
# 4.a if not equal the betting odds from that particular website are switched places
# 
# 5. dropping all 'boxer' columns except the first boxers column (A_boxers)
#
# 6. the new data frame (joined_df) is returned

def box_joining(data_frame):   
    """" The input data frame contains information from up to 7 different betting websites.
    The input data frame must have the following 6 columns:
    date (string), A_webiste (string), A_boxers (string), A_boxer_1_win (float),A_draw (float), A_boxer_2_win (float).
    These specific column names are used in this function to locate specific cells"""
    # 0
    import pandas as pd
    
    # 1.
    all_websites = pd.unique(data_frame['A_website']) 
    joined_df = pd.DataFrame(columns= ['date'])
    alphabet = list('ABCDEFG')
    # 2.
    for website in range(len(all_websites)):
        # 2.a
        joined_df[[f'{alphabet[website]}_boxers',
                  f'{alphabet[website]}_website',
                  f'{alphabet[website]}_boxer_1_wins',
                  f'{alphabet[website]}_draw',
                  f'{alphabet[website]}_boxer_2_wins']] = ''
        # 2.b
        temp_df = data_frame.loc[data_frame['A_website'] == all_websites[website]].reset_index(drop=True)
        # 2.c
        len_joined_df = len(joined_df)
        if len_joined_df == 0:
            for r_temp in range(len(temp_df)):
                joined_df = joined_df.append(temp_df.iloc[r_temp])
        # 2.d
        else:
            for r_temp in range(len(temp_df)):
                temp_match = []
                for r_total in range(len_joined_df):
                    temp_match.append(name_matching(joined_df['A_boxers'][r_total],temp_df['A_boxers'][r_temp]))
                    if name_matching(joined_df['A_boxers'][r_total],temp_df['A_boxers'][r_temp]):
                        joined_df.at[r_total,f'{alphabet[website]}_boxers'] = temp_df['A_boxers'][r_temp]
                        joined_df.at[r_total,f'{alphabet[website]}_website'] = temp_df['A_website'][r_temp]
                        joined_df.at[r_total,f'{alphabet[website]}_boxer_1_wins'] = temp_df['A_boxer_1_wins'][r_temp]
                        joined_df.at[r_total,f'{alphabet[website]}_draw'] = temp_df['A_draw'][r_temp]
                        joined_df.at[r_total,f'{alphabet[website]}_boxer_2_wins'] = temp_df['A_boxer_2_wins'][r_temp]
                        break
                        

                if not any(temp_match):
                    joined_df = joined_df.append(temp_df.loc[r_temp]).fillna('').reset_index(drop=True)
    # 3.
    joined_df = joined_df.replace('',0)
    # 4.
    for t_row in range(len(joined_df)):
        boxer_1, boxer_2 = joined_df.iloc[t_row]['A_boxers'].split('|')
        for column in range(1,len(all_websites)):
            if not joined_df.iloc[t_row][(column * 5 + 1)] == 0:
                temp_boxer_1, temp_boxer_2 = joined_df.iloc[t_row][(column * 5 + 1)].split('|')
                temp_list = [name_matching(boxer_1,temp_boxer_1),name_matching(boxer_2,temp_boxer_2)]
                # 4.a
                if not any(temp_list):
                    temp_win_1 = joined_df.iloc[t_row][(column * 5 + 3)]
                    temp_win_2 = joined_df.iloc[t_row][(column * 5 + 5)]
                    joined_df.iloc[t_row,(column * 5 + 3)] = temp_win_2
                    joined_df.iloc[t_row,(column * 5 + 5)] = temp_win_1           
    # 5.
    for website in range(1, len(all_websites)):
        joined_df = joined_df.drop(f'{alphabet[website]}_boxers', axis = 1)
    # 6.
    return(joined_df)

# Function box_betting. Version 2 (22 january 2022), made by Rogier Hetem
#
# The box_joining function (see one above) created a data frame containing the information from different betting
# websites. Per row one specific boxing match is displayed with all the different betting odds from the different
# betting websites. 
#
# This function box_betting seeks the highest odds for the particular matches and returns a new data frame
# containing only the highest betting odds with the accompanied website were you can get those odds.
#
# example:
# input data frame:
# date        , A_boxers                     , A_website,  A_boxer_1_wins, A_draw, A_boxer_2_wins  
# '16/01/2022', 'Smit Joe Jr.|Johnson Callum', 'betcity',  1,              5,      2  
# '16/01/2022', 'Johnson Callum |Smit Joe Jr ',  '365bet', 1,              4,      2 
#
# box_joining output (incorporated in this function):
# date         , A_boxers                     , A_website, A_boxer_1_wins, A_draw, A_boxer_2_wins, B_website, B_boxer_1_wins, B_draw, B_boxer_2_wins
# '16/01/2022', 'Smit Joe Jr.|Johnson Callum', 'betcity',  1,              5,      2,             '365bet'    2,              4,      1   
#
# output data frame:
# date,         boxer_1,        boxer_2,              website_boxer_1_wins,  boxer_1_best_odds  website_draw, best_draw_odds, website_boxer_2_wins, boxer_2_best_odds
# '16/01/2022'  'Smit Joe Jr.', 'Johnson Callum'     '365bet'                2,                 'betcity,     5,              'betcity',            2
#
# How does it work?
# 0. importing packages
#
# 1. the input data frame is 'joined' using the box_joining function and an empty output data frame is created
#
# 2. calculated:
# index locations within the joined_df data frame, from all the odds from the different betting websites: 
# boxer 1 wins, 
# a draw,
# boxer 2 wins
#
# 3. calculated:
# the index locations within the joined_df data frame, from only the highest odds given and their respected website
# this is done separately for:
# boxer 1 wins, 
# a draw,
# boxer 2 wins
#
# 4. the date, names, highest odds and their respected website are added one by one to the new output data frame (output_df)
# 
# 5. the output_df is returned

def box_betting(data_frame):
    """  The input data frame contains information from up to 7 different betting websites.
    The input data frame must have the following 6 columns:
    date (string), A_webiste (string), A_boxers (string), A_boxer_1_win (float),A_draw (float), A_boxer_2_win (float).
    These specific column names are used in this function to locate specific cells"""
    # 0.
    import pandas as pd
    import numpy as np
    # 1.
    joined_df = box_joining(data_frame)
    output_df = pd.DataFrame(columns= ['Date',
                                       'Boxer 1','Boxer 2',
                                       'Best odds boxer 1', 'Odds 1 at',
                                       'website_draw', 'best_draw_odds', 
                                       'Best odds boxer 2','Odds 2 at'])
    # 2.
    nr_columns_joined_df = len(joined_df.columns)
    columns_win_1 = range(3, nr_columns_joined_df, 4)
    columns_draw = range(4, nr_columns_joined_df, 4)
    columns_win_2 = range(5, nr_columns_joined_df, 4)
    
    for row in range(len(joined_df)):
        # 3.
        temp_win1, loc_1 = np.max(joined_df.iloc[row,columns_win_1]), np.argmax(joined_df.iloc[row,columns_win_1])
        temp_draw, loc_draw = np.max(joined_df.iloc[row,columns_draw]),np.argmax(joined_df.iloc[row,columns_draw])
        temp_win2, loc_2 = np.max(joined_df.iloc[row,columns_win_2]), np.argmax(joined_df.iloc[row,columns_win_2])   
        web_loc_1 = 2 + (4 * loc_1) 
        web_draw = 2 + (4 * loc_draw) 
        web_loc_2 = 2 + (4 * loc_2) 
        #4.
        output_df.at[row,'Date'] = joined_df['date'][row]
        output_df.at[row,'Boxer 1'], output_df.at[row,'Boxer 2'] =  joined_df['A_boxers'][row].split('|')
        
        output_df.at[row,'Odds 1 at'] = joined_df.iloc[row][web_loc_1]
        output_df.at[row,'Best odds boxer 1'] = temp_win1
        
        output_df.at[row,'website_draw'] = joined_df.iloc[row][web_draw]
        output_df.at[row,'best_draw_odds'] = temp_draw
        
        output_df.at[row,'Odds 2 at'] = joined_df.iloc[row][web_loc_2]
        output_df.at[row,'Best odds boxer 2'] = temp_win2
    # 5.   
    # for simplicity I took out the draw odds
    output_df = output_df.drop('website_draw',axis=1)
    output_df = output_df.drop('best_draw_odds',axis=1)
    return(output_df)