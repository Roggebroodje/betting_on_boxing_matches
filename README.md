## Project 1: Finding our best odds
#### Let’s find the best betting odds for every upcoming boxing match
Many betting websites offer the thrill to bet on your favourite boxer, claiming they provide the best betting odds. But only one can be the best. This web scraping project collects betting information about upcoming boxing matches, from 4 major websites. It joins corresponding matches, compares the betting odds and selects the highest odds per match. Finally returning all this information in a simple and neat table. So that you know where you should place your next bet.

All of this is done using the _Python_ programming language and some of its powerful packages, such as BeautifulSoup4, Selenium, Pandas and a few others.

#### My personal goal
My overall goal was to learn about web scraping. I believe that web scraping is a very powerful tool for a data analyst. Acquiring this skill taught me how to collect information from the web and how to create my own datasets in an automated fashion. This can be used in a variety of settings. So I know this skill will absolutely come in handy in my data journey. 

#### What did I do?
First I chose 4 betting websites which I liked and wanted to use. For simplicity and to minimaze traffic on the websites, I used one page per website. Because most betting websites do not allow direct downloads of their html code, I used the package Selenium to control the page, select the necessary information and save the html code. 

Next I had to write individual code per website to filter out the correct information. For this I used the package BeautifulSoup4. Because the websites are not static I had to change my code several times before reaching a somewhat robust result. 

Every websites offers a different set of boxing events. The way names of the boxers are written differs in order, abbreviations, use of punctuations and sometimes spelling. Because of these differences I created a function to check which boxing matches correspond over the different websites. By saving the boxer names in a text string I could compare them, while keeping in mind all the possible differences. If the text strings were equal enough to be an actually corresponding boxing match, the function returns the statement ‘True’. Using this ‘string matching’ function I could join corresponding boxing events from the different websites. 

After correctly joining the matches, I compared the betting odds per match. Saving the highest odds per match, joined with their respected website in a final outcome table. Which is returned at the end of the code. 

**Files**: <br>
**README.md** is this current file you are in, it contains written explanations about the project and the code. **Function.py** file contains three functions necessary to match corresponding matches and creates the outcome table. **Betting.py**, is the ‘running-file’. It contains the web scraping code and uses the functions from the Function.py file. It returns the outcome table.

**Packages used**: <br>
bs4, selenium, webdriver_manager.chrome, pandas, numpy, pyautogui and datetime.

**Webpages used**: 
1. https://sports.bwin.com/en/sports/boxing-24
2. https://jacks.nl/sports?gclid=Cj0KCQiA8vSOBhCkARIsAGdp6RTD2gZe5vGv-keHZOCzae5eNw86uxCmmZytPFaYbzW0yRCntiHpxL0aAsLnEALw_wcB#sports-hub/boxing
3. https://www.bet365.nl/#/AC/B9/C20007979/D1/E148/F2/
4. https://www.wallacebet.com/pre-match#/Boxing/World/13301/19256588

**Functions used**: <br>
1. _name_matching_: <br>
For mathcing strings that are kinda similar. I use this for pairing/matching corresponding boxing events from the four different websites. As every website writes names differently.

2. _box_joining_: <br>
For creating a data frame in which the corresponding boxing events from the four different websites are correctly gathered together (also using the name_matching function).

3. _box_betting_: <br>
To find the highest odds on a specific boxing event and returning a new data frame with the output.

4. _next_weekday_: <br>
To find the next date (in numbers) given today in a weekday written way (Monday, Tuesday etc.). This code was originally written by 'phidag', I edited a little bit to fit my specific needs. The credit for this goes to: https://stackoverflow.com/users/35070/phihag

**Downside of the code**: <br>
The web scraping part of the code works one day and than fails the next. This was due to webpage(s) loading extremely slow or change(s) in information display. After several updates the code seems to have reached a robust outcome. However, I understand that new changes on the webpages can and will eventually lead to new errors. I already heard about possible API's that some websites may offer, which can help in creating a much more robust code. I will look into this in later projects.
