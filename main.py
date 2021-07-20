from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import sys
import time

#keywords to look for
keywords = ['Anime', 'Otaku', 'Weeb', 'Gaming', 'Discord', 'Weeaboo', 'Games', 'Japan', 'Japanese', 'Japanisch', 'Nerd']

#webdriver settings
PATH = "msedgedriver.exe"
driver = webdriver.Edge(PATH)
driver.maximize_window()

#function to clear console
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#function to set console font color
def SetConsoleColor(Color):
    if Color.lower() == 'green':
        sys.stdout.write("\033[0;32m")
    elif Color.lower() == 'red':
        sys.stdout.write("\033[1;31m")
    elif Color.lower() == 'reset':
        sys.stdout.write("\033[0;0m")

#main swipe function
def Swipe():

    bioElem = '//*[@id="q633216204"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[3]/div[3]'  
    popup1 = '//*[@id="q-1095164872"]/div/div/div[2]/button[2]'

    try:
        while(True):

            #create key action
            action = ActionChains(driver)

            #kill popups if there are any
            try:
                driver.find_element_by_xpath(popup1).click()
            except:
                None
            
            #get current time for timestamp
            time.sleep(1.5)
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)

            #get biography text
            hit = False
            hitWord = ''
            bioText = driver.find_element_by_xpath(bioElem).text

            #check if one of the keywords exists in the biography
            for keyword in keywords:
                if keyword in bioText or keyword.lower() in bioText or keyword.upper() in bioText:
                    hit = True
                    hitWord = keyword
                    break
            
            #if keyword exists wait for input
            if hit:
                SetConsoleColor('Green')
                print('[{}] Found profile with keyword "{}".\nLike? (Y/N)\n'.format(current_time, hitWord))
                SetConsoleColor('Reset')
                x = input('')
                if x.lower() == 'y':
                    action.send_keys(Keys.ARROW_RIGHT)
                    action.perform()
                else:
                    action.send_keys(Keys.ARROW_LEFT)
                    action.perform()
            else:
                SetConsoleColor('Red')
                print('[{}] Criteria not matched\n'.format(current_time))
                SetConsoleColor('Reset')
                action.send_keys(Keys.ARROW_LEFT)
                action.perform()
    except:
        print('[{}] No profiles left to swipe (or other exception).\nRetry? (Y/N)'.format(time.strftime("%H:%M:%S", time.localtime())))
        x = input('')

        if x.lower() == 'y':
            Swipe()
        else:
            driver.close()

#initial start actions
def init():
    driver.get("https://tinder.com/app/recs")

    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="q633216204"]/div/div[2]/div/div/div[1]/button').click()
    driver.find_element_by_xpath('//*[@id="q633216204"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]').click()
    cls()

    SetConsoleColor('Green')
    print('Please sign in and wait for the next page to load.\nContinue? (Y/N)\n')
    SetConsoleColor('Reset')
    x = input('')
    if x.lower() == 'y':
        cls()
        Swipe()
    else:
        driver.close()

#startup
cls()
SetConsoleColor('Green')
print('Welcome to Tin Bot ©2021, Rene Huber')
print('Current keywords: {}\nStart? (Y/N)\n'.format(keywords))
SetConsoleColor('Reset')
x = input('')
if x.lower() == 'y':
    init()
else:
    driver.close()