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
#automatically like profiles that meet the criteria
autolike = False

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

def likeDislike(dislike, current_time, hitWord):
    action = ActionChains(driver)
    if dislike:
        action.send_keys(Keys.ARROW_LEFT)
        action.perform()
        return
    if autolike:
        SetConsoleColor('Green')
        print('[{}] Autoliked a profile with keyword "{}"\n'.format(current_time, hitWord))
        SetConsoleColor('Reset')
        action.send_keys(Keys.ARROW_RIGHT)
        action.perform()
    else:
        SetConsoleColor('Green')
        print('[{}] Found profile with keyword "{}"\n           Like? (Y/N)'.format(current_time, hitWord))
        x = input('           ')
        print()
        SetConsoleColor('Reset')
        if x.lower() == 'y':
            action.send_keys(Keys.ARROW_RIGHT)
            action.perform()
        else:
            action.send_keys(Keys.ARROW_LEFT)
            action.perform()
        
def Swipe():

    bioElem = '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[3]/div[3]'  
    popup1 = '/html/body/div[2]/div/div/div[2]/button[2]'

    try:
        while(True):
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
                likeDislike(False, current_time, hitWord)
            else:
                SetConsoleColor('Red')
                if redFlagHit:
                    print('[{}] Criteria not matched -> Redflag: {}\n'.format(current_time, redFlagWord))
                else:
                    print('[{}] Criteria not matched\n'.format(current_time))
                SetConsoleColor('Reset')
                likeDislike(True, current_time, hitWord)
    except:
        while True:
            cls()
            SetConsoleColor('Green')
            print('[{}] No profiles left to swipe (or other exception).\n[ R = Retry | C = Config | X = Exit ]'.format(time.strftime("%H:%M:%S", time.localtime())))
            x = input('')
            SetConsoleColor('Reset')
            if x.lower() == 'r':
                cls()
                Swipe()
            if x.lower() == 'c':
                printConfig()
            if x.lower() == 'x':
                SetConsoleColor('Red')
                print('Shutting down...')
                SetConsoleColor('Reset')
                try:
                    driver.close()
                except:
                    None
                exit()

#print config
def printConfig():
    while True:
        cls()
        global autolike
        SetConsoleColor('Green')
        print('Current Tin Bot configuration:\n')
        print('Keywords: {}\n'.format(keywords))
        print('Redflags: {}\n'.format(redFlags))
        print('Autolike: {}\n'.format(autolike))
        print('[ T = Toggle Autolike | B = Back ]')
        x = input('')
        SetConsoleColor('Reset')
        if x.lower() == 't':
            autolike = not autolike
        if x.lower() == 'b':
            return

#initial start actions
def init():
    driver.get("https://tinder.com/app/recs")

    time.sleep(0.5)
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div/div[1]/button').click() #cookies
    driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a').click() #log in
    time.sleep(0.5)
    driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/div[3]/span/div[3]/button').click() #log in method
    cls()

    SetConsoleColor('Green')
    print('Please sign in and wait for the next page to load.\nContinue? (Y/N)\n')
    x = input('')
    SetConsoleColor('Reset')
    if x.lower() == 'y':
        cls()
        Swipe()
    else:
        driver.close()

#program loop
while True:
    cls()
    SetConsoleColor('Green')
    print('Welcome to Tin Bot ©2021, Rene Huber')
    print('[ S = Start | C = Config | X = Exit ]')
    x = input('')
    SetConsoleColor('Reset')
    if x.lower() == 's':
        init()
    if x.lower() == 'c':
        printConfig()
    if x.lower() == 'x':
        SetConsoleColor('Red')
        print('Shutting down...')
        SetConsoleColor('Reset')
        try:
            driver.close()
        except:
            None
        exit()
    