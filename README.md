# Project: On which website should you bet?

## General outline: 
Where do you get the best odds if you would bet on your favourite boxing match? <br>

In this project I compared online betting odds. I specifically looked at boxing matches.<br> 
I use four different betting websites for this comparison. <br>
I pair corresponding boxing events from the four different websites. <br>
I check which website offers the highest betting odds on a particular outcome ('boxer 1' wins or 'boxer 2' wins), on one particular boxing event. <br>
I repeat this for every single boxing event. <br>
I then return a table that displays all upcoming boxing events, with their highest odds and on which website you can find these odds. <br>

## Goal and more specifics:
The goal of this project for me was to practice webscraping and specifically bs4 (BeautifulSoup4). This is my first webscraping project. <br>

For this project I used the following Python packages:
1. bs4
2. selenium 
3. webdriver_manager.chrome 
4. pandas 
5. numpy 
6. pyautogui
7. datetime

I gather information from the following webpages.
1. https://sports.bwin.com/en/sports/boxing-24
2. https://jacks.nl/sports?gclid=Cj0KCQiA8vSOBhCkARIsAGdp6RTD2gZe5vGv-keHZOCzae5eNw86uxCmmZytPFaYbzW0yRCntiHpxL0aAsLnEALw_wcB#sports-hub/boxing
3. https://www.bet365.nl/#/AC/B9/C20007979/D1/E148/F2/
4. https://www.wallacebet.com/pre-match#/Boxing/World/13301/19256588

Functions I use: <br>
1. name_matching: <br>
For mathcing strings that are kinda similar. I use this for pairing/matching corresponding boxing events from the four different websites. As every website writes names differently.

2. box_joining: <br>
For creating a data frame in which the corresponding boxing events from the four different websites are correctly gathered together (also using the name_matching function).

3. box_betting: <br>
To find the highest odds on a specific boxing event and returning a new data frame with the output.

4. next_weekday: <br>
To find the next date (in numbers) given today in a weekday written way (Monday, Tuesday etc.). This code was originally written by 'phidag', i edited a little bit to fit my specific needs. The credit for this goes to: https://stackoverflow.com/users/35070/phihag

## Downside of the code:
After finishing my code, I already had to update it several times to keep it working. <br>
I realized that using bs4 for webscraping on continuesly changing websites is not such a robust way.<br>

I already heard about possible API's that some websites may offer, which will lead to a more robust code. For now I have not looked into that. I might for later projects though.
