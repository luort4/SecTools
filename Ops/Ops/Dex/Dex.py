import pandas as pd
import creds
import time
import os
from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

def dex_automate(driver, df1):
    addUser_url = 'https://console.forte.net/users'
    #login and then
    print("Current Dataframe, to be entered: \n", df1)
    driver.get("https://console.forte.net/login")
    driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(creds.usernameDex)
    time.sleep(1)
    driver.find_element(By.XPATH, '/html/body/co-root/div/div/main/co-signin/div/div/div[2]/fo-login/div[1]/div/form/div[2]/span/input').send_keys(creds.passwordDex + Keys.RETURN)
    input("Press Enter after MFA: ")
    driver.get(addUser_url)
    input("Press Enter to start inputing users: ")
    for i, j in enumerate(df1['fullName']):
        time.sleep(1)
        print(f"Inputing data for {df1['fullName'][i]}")
        driver.find_element(By.XPATH, '/html/body/co-root/div/div/main/co-users/co-user-list/header/div/div[2]/button[1]').click()
        input("Waiting for form to load, press enter when open: ")
        driver.find_element(By.XPATH, '//*[@id="user-invite-selection-modal"]/div/co-user-invite/form/div[1]/div[2]/div/div[1]/textarea').send_keys(df1['email'][i])
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="role"]/div/co-dropdown/div/co-dropdown-button/button').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '/html/body/co-dropdown-menu[3]/div[1]/div/ul/ul/li[4]/co-menu-item/div/co-role/span/span').click()
        input("[+] Press Enter for the next User")
        driver.get(addUser_url)

# perform the ops managements
def ops_onboard(df, df1, driver):
    fullName = []
    email = []
    for i, j in enumerate(df['Department']):
        if j == "Operations Team" and df['Home Base'][i] == 'Orlando':
            eph_fullName = df['First Name'][i] + " " + df['Last Name'][i]
            fullName.append(eph_fullName)
            email.append(df['Email Address Gsuite Primary'][i])
        else:
            fullName.append("Nothing")
            email.append("Nothing")

    df1['fullName'] = fullName
    df1['email'] = email
    dex_automate(driver, df1)

def main():
    # setting options for the webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('disable-infobars')
    options.add_argument('start-maximized')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('no-sandbox')
    options.add_argument("--remote-debugging-port=9230")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches', ["enable-automation"])
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("disable-blink-features=AutomationControlled")

    # assign the driver
    s = Service(ChromeDriverManager().install())
    driver = Chrome(service=s, options=options)

    # set the dataframes
    df = pd.read_csv("Onboarding/db/empemails.csv")
    df1 = pd.DataFrame(columns=['fullName', 'email'])
    # start the function
    ops_onboard(df, df1, driver)
    os.system("pyclean . -q")

#main()
