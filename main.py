from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from msedge.selenium_tools import EdgeOptions, Edge
import os
import sys
import time

#keywords to look for
keywords = ['Anime', 'Otaku', 'Weeb', 'Gaming', 'Discord', 'Weeaboo', 'Games', 'Japan', 'Japanese', 'Japanisch', 'Nerd', 'Asia', 'アニメ']
#red flags which will not trigger an input prompt
redFlags = ['Pronouns', 'She/they', 'Asexual', 'Vaxx', 'Vaccinated', 'Impf']

#webdriver settings
PATH = "msedgedriver.exe"
opt = EdgeOptions()
opt.use_chromium = True
opt.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = Edge(executable_path=PATH, options=opt)
driver.maximize_window()

#function to clear console
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def SetConsoleColor(Color):
    if Color.lower() == 'green':
        sys.stdout.write("\033[0;32m")
    elif Color.lower() == 'red':
        sys.stdout.write("\033[1;31m")
    elif Color.lower() == 'reset':
        sys.stdout.write("\033[0;0m")

def Swipe():

    bioElem = '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[3]/div[3]'  
    popup1 = '/html/body/div[2]/div/div/div[2]/button[2]'

    try:
        while(True):

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
            redFlagHit = False
            hitWord = ''
            redFlagWord = ''
            bioText = driver.find_element_by_xpath(bioElem).text

            #check if one of the keywords exists in the biography
            for keyword in keywords:
                if keyword in bioText or keyword.lower() in bioText or keyword.upper() in bioText:
                    hit = True
                    hitWord = keyword
                    break
            
            #check if one of the red flags exists in the biography
            for redFlag in redFlags:
                if redFlag in bioText or redFlag.lower() in bioText or redFlag.upper() in bioText:
                    redFlagHit = True
                    redFlagWord = redFlag
                    break

            #if keyword exists and no red flag was found wait for input
            if hit and not redFlagHit:
                SetConsoleColor('Green')
                print('[{}] Found profile with keyword "{}".\n           Like? (Y/N)'.format(current_time, hitWord))
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
                if redFlagHit:
                    print('[{}] Criteria not matched -> Red flag: {}\n'.format(current_time, redFlagWord))
                else:
                    print('[{}] Criteria not matched\n'.format(current_time))
                SetConsoleColor('Reset')
                action.send_keys(Keys.ARROW_LEFT)
                action.perform()
    except:
        SetConsoleColor('Green')
        print('[{}] No profiles left to swipe (or other exception).\nRetry? (Y/N)'.format(time.strftime("%H:%M:%S", time.localtime())))
        SetConsoleColor('Reset')
        x = input('')

        if x.lower() == 'y':
            Swipe()
        else:
            driver.close()

#initial start actions
def init():
    driver.get("https://tinder.com/app/recs")

    time.sleep(0.5)
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div/div[1]/button').click() #cookies
    driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a').click() #log in
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