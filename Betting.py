# code created by Rogier Hetem (last update 31-01-2021)
#
# importing packages (they need to be installed before you can run this part)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import pyautogui
import pandas as pd
import datetime
import numpy as np

# importing the 3 self-made functions from Function.py file (only works when file is .py extension)
from Functions import name_matching, box_joining, box_betting

# Initial settings (and opening a chrome webbrower)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(30) # 'driver' will wait a maximum of 30 seconds for pages to load.

# Importing the information
#
# 4 different betting website are used.
# only 1 page per website is accessed (for minimal traffic)
#
# although the driver has an implicit waiting time,
# I found that even when a page is loaded does not (always) mean that all the content is loaded as well.
# therefor an extra explicit waiting time is incorporated using the pyautogui.sleep function
# most errors accured with wallacebet and the jacks website.

# import from https://sports.bwin.com
driver.get("https://sports.bwin.com/en/sports/boxing-24")
pyautogui.sleep(10)
element_bwin = driver.find_element(By.CSS_SELECTOR, "ms-event-group.event-group")
response_bwin = element_bwin.get_attribute('innerHTML')

# import from https://jacks.nl
driver.get("https://jacks.nl/sports?gclid=Cj0KCQiA8vSOBhCkARIsAGdp6RTD2gZe5vGv-keHZOCzae5eNw86uxCmmZytPFaYbzW0yRCntiHpxL0aAsLnEALw_wcB#sports-hub/boxing")
pyautogui.sleep(15)
element_jacks = driver.find_element(By.CSS_SELECTOR, "ul.KambiBC-sandwich-filter__list")
response_jacks = element_jacks.get_attribute('innerHTML')

# import from https://www.bet365.nl
driver.get("https://www.bet365.nl/#/AC/B9/C20007979/D1/E148/F2/")
pyautogui.sleep(10)
element_bet365 = driver.find_element(By.CSS_SELECTOR, "div.wcl-CommonElementStyle_PrematchCenter ")
response_bet365 = element_bet365.get_attribute('innerHTML')

# import from https://www.wallacebet.com
driver.get("https://www.wallacebet.com/pre-match#/Boxing/World/13301/19256588")
pyautogui.sleep(15)
element_wallacebet = driver.find_element(By.ID, "eventListBody")   
response_wallacebet = element_wallacebet.get_attribute('innerHTML')

# driver closing
driver.close() # closing the chrome webbrowser 

# transforming the imported information into a 'Beautiful Soup' object
bet365_soup = bs(response_bet365)
bwin_soup = bs(response_bwin)
jacks_soup = bs(response_jacks)
wallacebet_soup = bs(response_wallacebet)

# creating temporary empty lists to store the specific information from the websites
# if the temporary lists are 'valid', meaning they are equal in size the information 
# will be added to the lists used to create a our output data frame  
date = []
boxers = []
websites = []
win_1 = []
draw = []
win_2 = []

temp_dates = []
temp_boxers = []
temp_websites = []
temp_win_1 = []
temp_draw = []
temp_win_2 = []

# Below four separate loops are created with their own unique code.
# all codes use BeautifulSoup4 to extract HTML information from the specific pages (now saved as an object)
# it was not possible to create one general function that could be used on all four different websites.

# (31-01-2021)
# I ran into continues trouble with the wallacebet websites. 
# Very long loading times, changes in displaying their information and or not complete information.
# because of this I changed the code to less extracting using BeautifulSoup and more a 'string based' approach,
# which ended up looking a bit 'funky', but was less prone to changes on their website.

# extracting information from https://sports.bwin.com BeautifulSoup object
for i in range(len(bwin_soup.find_all('ms-event',class_ = "grid-event ms-active-highlight"))):

    li = bwin_soup.find_all('ms-event',class_ = "grid-event ms-active-highlight")[i]
    #date
    temp_dates.append(li.find("ms-prematch-timer", class_ = "starting-time timer-badge").get_text().split(' ')[0])
    #boxers    
    name_1 = ''
    name_2 = ''
    names = li.find_all('div', class_ = "participant")
    name_1 = str(names[0]).split('<span')[0]
    name_1 = name_1.split('>')[1]
    name_2 = str(names[1]).split('<span')[0]
    name_2 = name_2.split('>')[1]
    temp_boxers.append(name_1 + ' | ' + name_2)
    # website
    temp_websites.append('bwin')
    #odds
    odds = li.find_all("div", class_ = "option option-value")
    temp_win_1.append(float(odds[0].get_text()))
    temp_draw.append(float(odds[1].get_text()))
    temp_win_2.append(float(odds[2].get_text()))

# check on whether lenghts of lists are still equal if not something went wrong
# possibly with loading in the page fully,
# possibly the website changed its HTML code.
if (len(temp_dates) == len(temp_boxers) == len(temp_websites) == len(temp_win_1) == len(temp_win_2) == len(temp_draw)):
    for i in range(len(temp_dates)):
        date.append(temp_dates[i])
        boxers.append(temp_boxers[i])
        websites.append(temp_websites[i])
        win_1.append(temp_win_1[i])
        draw.append(temp_draw[i])
        win_2.append(temp_win_2[i])
    temp_dates = []
    temp_boxers = []
    temp_websites = []
    temp_win_1 = []
    temp_draw = []
    temp_win_2 = []
else:
    print('Something went wrong at/with https://sports.bwin.com')
    print(len(temp_dates), len(temp_boxers), len(temp_websites), len(temp_win_1), len(temp_win_2), len(temp_draw))
    temp_dates = []
    temp_boxers = []
    temp_websites = []
    temp_win_1 = []
    temp_draw = []
    temp_win_2 = []
    
# extracting information from https://jacks.nl BeautifulSoup object

# extra function used to calculate upcoming dates
def next_day(given_date, weekday):
    day_shift = (weekday - given_date.weekday()) % 7
    return given_date + datetime.timedelta(days=day_shift)
now = datetime.datetime.today().date()

for i in range(len(jacks_soup.find_all('li',class_ = "KambiBC-sandwich-filter__event-list-item"))):

    li = jacks_soup.find_all('li',class_ = "KambiBC-sandwich-filter__event-list-item")[i]
    # date
    temp_date = (li.find('span', class_ = 'KambiBC-event-item__start-time--date').get_text())
    
    if temp_date in ['ma','di','wo','do','vr','za','zo']:
        temp_date = temp_date.replace('ma','0').replace('di','1').replace('wo','2').replace('do','3').replace('vr','4').replace('za','5').replace('zo','6')
        temp_date = float(temp_date)
        temp_date = str(next_day(now, temp_date))
    else:
        temp_date = temp_date.replace(' jan.','/01').replace(' feb.','/02').replace(' mrt.','/03').replace(' apr.','/04').replace(' mei','/05').replace(' jun.','/06')
        temp_date = temp_date.replace(' jul.','/07').replace(' aug.','/08').replace(' sep.','09').replace(' okt.','/10').replace(' nov','/11').replace(' dec.','/12')
        temp_date = temp_date + '/' + str(datetime.date.today().year)
        
    temp_dates.append(temp_date)
    # boxers
    name_1 = ''
    name_2 = ''
    names = li.find_all('div', class_ = "KambiBC-event-participants__name")
    name_1 = name_1.join([letter for letter in names[0].get_text() if letter.isalnum() or letter.isspace()])
    name_2 = name_2.join([letter for letter in names[1].get_text() if letter.isalnum() or letter.isspace()])
    temp_boxers.append(name_1 + ' | ' + name_2)
    # websites
    temp_websites.append('jacks')
    # odds
    odds = li.select("div[class^=OutcomeButton__Odds-sc-]")
    if len(odds) == 3:
        temp_win_1.append(float(odds[0].get_text()))
        temp_draw.append(float(odds[1].get_text()))
        temp_win_2.append(float(odds[2].get_text()))
    elif len(odds) == 2:
        temp_win_1.append(float(odds[0].get_text()))
        temp_draw.append(0)
        temp_win_2.append(float(odds[1].get_text()))
        
# check on whether lenghts of lists are still equal if not something went wrong
# possibly with loading in the page fully,
# possibly the website changed its HTML code.
# check on whether lenghts of lists are still equal if not something went wrong
# possibly with loading in the page fully,
# possibly the website changed its HTML code.
if (len(temp_dates) == len(temp_boxers) == len(temp_websites) == len(temp_win_1) == len(temp_win_2) == len(temp_draw)):
    for i in range(len(temp_dates)):
        date.append(temp_dates[i])
        boxers.append(temp_boxers[i])
        websites.append(temp_websites[i])
        win_1.append(temp_win_1[i])
        draw.append(temp_draw[i])
        win_2.append(temp_win_2[i])
    temp_dates = []
    temp_boxers = []
    temp_websites = []
    temp_win_1 = []
    temp_draw = []
    temp_win_2 = []
else:
    print('Something went wrong at/with https://jacks.nl') 
    print(len(temp_dates), len(temp_boxers), len(temp_websites), len(temp_win_1), len(temp_win_2), len(temp_draw))
    temp_dates = []
    temp_boxers = []
    temp_websites = []
    temp_win_1 = []
    temp_draw = []
    temp_win_2 = []
    
# extracting information from https://www.bet365.nl BeautifulSoup object
date_table = bet365_soup.select("div[class*=sgl-MarketFixtureDet]")[0]
stuff = ["rcl-MarketHeaderLabel rcl-MarketHeaderLabel-isdate",
         "rcl-ParticipantFixtureDetails_BookCloses",
        "rcl-MarketHeaderLabel-isdate rcl-MarketHeaderLabel"]
days_times = date_table.find_all("div", class_= stuff)

for i in range(len(days_times)):
    if len(days_times[i].get_text()) > 6:
        continue
    elif len(days_times[i - 1].get_text()) > 6:
        temp_date = days_times[i - 1].get_text().partition(" ")[2]
        temp_date = temp_date.replace(' jan','/01/').replace(' feb','/02/').replace(' mrt','/03/').replace(' apr','/04/').replace(' mei','/05/').replace(' jun','/06/')
        temp_date = temp_date.replace(' jul','/07/').replace(' aug','/08/').replace(' sep','09/').replace(' okt','/10/').replace(' nov','/11/').replace(' dec','/12/')
        temp_date = temp_date + str(datetime.date.today().year)
        temp_dates.append(temp_date)
    else:
        temp_dates.append(temp_date)
# boxers
for i in range(0,len(bet365_soup.select("div.rcl-ParticipantFixtureDetailsTeam_TeamName")),2):
    name_1 = bet365_soup.select("div.rcl-ParticipantFixtureDetailsTeam_TeamName")[i].get_text()
    name_2 = bet365_soup.select("div.rcl-ParticipantFixtureDetailsTeam_TeamName")[i + 1].get_text()
    temp_boxers.append(name_1 + ' | ' + name_2)
#website
for i in range(int(len(bet365_soup.select("div.rcl-ParticipantFixtureDetailsTeam_TeamName")) / 2)):
    temp_websites.append("bet365")
# odds
for i in range(int(len(bet365_soup.select("span.sgl-ParticipantOddsOnly80_Odds")) / 2)):
    temp_win_1.append(float(bet365_soup.select("span.sgl-ParticipantOddsOnly80_Odds")[i].get_text()))
    temp_win_2.append(float(bet365_soup.select("span.sgl-ParticipantOddsOnly80_Odds")[i + int(len(bet365_soup.select("span.sgl-ParticipantOddsOnly80_Odds")) / 2) ].get_text()))
    temp_draw.append(0)
    
# check on whether lenghts of lists are still equal if not something went wrong
# possibly with loading in the page fully,
# possibly the website changed its HTML code.
if (len(temp_dates) == len(temp_boxers) == len(temp_websites) == len(temp_win_1) == len(temp_win_2) == len(temp_draw)):
    for i in range(len(temp_dates)):
        date.append(temp_dates[i])
        boxers.append(temp_boxers[i])
        websites.append(temp_websites[i])
        win_1.append(temp_win_1[i])
        draw.append(temp_draw[i])
        win_2.append(temp_win_2[i])
    temp_dates = []
    temp_boxers = []
    temp_websites = []
    temp_win_1 = []
    temp_draw = []
    temp_win_2 = []
else:
    print('Something went wrong at/with https://www.bet365.nl')
    print(len(temp_dates), len(temp_boxers), len(temp_websites), len(temp_win_1), len(temp_win_2), len(temp_draw))
    temp_dates = []
    temp_boxers = []
    temp_websites = []
    temp_win_1 = []
    temp_draw = []
    temp_win_2 = []


# extracting information from https://www.wallacebet.nl BeautifulSoup object
# creating a temporary data frame 'test_df' to order and store the wallace data correctly
nr_events = len(wallacebet_soup.select("div[class*=sbEventsList__time]"))
categories = ['date','boxer','boxer','odds','odds']
categories = (categories * nr_events)
data = [''] * len(categories)
test_df = pd.DataFrame({
    'category':categories,
    'wallace_data':data
})

if nr_events > 0:
    # the actual data from wallace, using the complete string object
    wallace_data = []
    unwanted_symbols = [':','+']
    for text in wallacebet_soup.get_text().split("\n"):
            if not any(unw in text for unw in unwanted_symbols):
                if text.strip() != "" and (len(text.strip()) > 1):
                    wallace_data.append(text.strip())

    # categorizing the different data into 'date', 'odds' or 'boxer'
    actual_categories = []
    for text in wallace_data:
        if ',' in text and '20' in text:
            actual_categories.append('date')
        elif text.replace(".","").isdecimal() and len(text) < 7:
            actual_categories.append('odds')
        else:
            actual_categories.append('boxer')

    # putting the actual wallace data into the temporary data frame 'test_df'
    # based on their categories, if a category is missing the data holder is filled with "" (empty string)
    counter = 0
    for row in range(len(test_df)):
        if test_df['category'][row] == actual_categories[counter]:
            test_df.at[row, 'wallace_data'] = wallace_data[counter]
            counter += 1
        else:
            test_df.at[i, 'wallace_data'] = ""

    # replacing empty date places with the last findable date
    for row in range(len(test_df)):      
        if test_df['category'][row] == 'date' and test_df['wallace_data'][row] == "":
            test_df.at[row,'wallace_data'] = test_df['wallace_data'][(row - 5)]

    # replacing written dates with numbers
    temp_date = [text.split(', ')[1].replace(' January ','/01/').replace(' February ','/02/')\
       .replace(' March ','/03/').replace(' April ','/04/').replace(' May ','/05/').replace(' June ','/06/')\
        .replace(' July ','/07/').replace(' August ','/08/').replace(' September ','09/').replace(' October ','/10/')\
        .replace(' November ','/11/').replace(' December ','/12/')\
                  for text in test_df['wallace_data'].loc[test_df['category'] == 'date']]

    counter = 0        
    for row in range(len(test_df)):      
        if test_df['category'][row] == 'date':
            test_df.at[row,'wallace_data'] = temp_date[counter]
            counter += 1

    # joining both boxer names into one row
    for row in range(1,(len(test_df)),5):
        if test_df['category'][row] == 'boxer':
            temp_names = test_df['wallace_data'][row] + ' | ' + test_df['wallace_data'][row + 1]
            test_df.at[row,'wallace_data'] = temp_names

    # dropping the extra boxer name, as they are now in the same row already
    drop_list = range(2,(len(test_df)),5)
    test_df = test_df.drop(drop_list,axis=0).reset_index(drop=True)

    drop_list = []
    for row in range(1,(len(test_df)),4):
        if test_df['wallace_data'][row] == "":
            drop_list.append(row + 1)
            drop_list.append(row)
            drop_list.append(row - 1)
            drop_list.append(row - 2)

    test_df = test_df.drop(drop_list,axis=0).reset_index(drop=True)

    # adding the values to the lists
    for row in range(len(test_df)):
        if test_df['category'][row] == 'date':
            temp_dates.append(test_df['wallace_data'][row])
        elif test_df['category'][row] == 'boxer':
            temp_boxers.append(test_df['wallace_data'][row])
        elif test_df['category'][row] == 'odds' and test_df['category'][row - 1] != 'odds':
                temp_win_1.append(float(test_df['wallace_data'][row]))
        elif test_df['category'][row] == 'odds' and test_df['category'][row - 1] == 'odds':
                temp_win_2.append(float(test_df['wallace_data'][row]))

    for i in range(int((len(test_df)) / 4)):        
        temp_draw.append(0) 
        temp_websites.append('wallace')

    # check on whether lenghts of lists are still equal if not something went wrong
    # possibly with loading in the page fully,
    # possibly the website changed its HTML code.
    if (len(temp_dates) == len(temp_boxers) == len(temp_websites) == len(temp_win_1) == len(temp_win_2) == len(temp_draw)):
        for i in range(len(temp_dates)):
            date.append(temp_dates[i])
            boxers.append(temp_boxers[i])
            websites.append(temp_websites[i])
            win_1.append(temp_win_1[i])
            draw.append(temp_draw[i])
            win_2.append(temp_win_2[i])
        temp_dates = []
        temp_boxers = []
        temp_websites = []
        temp_win_1 = []
        temp_draw = []
        temp_win_2 = []
    else:
        print('Something went wrong at/with www.wallacebet.com')
        print(len(temp_dates), len(temp_boxers), len(temp_websites), len(temp_win_1), len(temp_win_2), len(temp_draw))
        temp_dates = []
        temp_boxers = []
        temp_websites = []
        temp_win_1 = []
        temp_draw = []
        temp_win_2 = []

# putting the lists into a input data frame
input_df = pd.DataFrame({
    'date':date,
    'A_boxers':boxers,
    'A_website':websites,
    'A_boxer_1_wins':win_1,
    'A_draw':draw,
    'A_boxer_2_wins':win_2
})

# using the input data frame for the box_betting input
box_betting(input_df)
