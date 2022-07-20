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

def swipe_automate(driver, df1):
    addUser_url = 'https://swipesimple.com/resellers/6/users/new'
    #login and then
    print("Current Dataframe, to be entered: \n", df1)
    driver.get("https://swipesimple.com/sign_in")
    driver.find_element(By.XPATH, '//*[@id="login-username"]').send_keys(creds.usernameSwipePD)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="login-password"]').send_keys(creds.passwordSwipePD + Keys.RETURN)
    input("Press Enter to start inputing users: ")
    driver.get(addUser_url)
    for i, j in enumerate(df1['fullName']):
        time.sleep(1)
        print(f"Inputing data for {df1['fullName'][i]}")
        driver.find_element(By.XPATH, '/html/body/content/main/section[2]/form/div/div/div[1]/div/input').send_keys(df1['fullName'][i])
        driver.find_element(By.XPATH, '/html/body/content/main/section[2]/form/div/div/div[2]/div/input').send_keys(df1['email'][i])
        driver.find_element(By.XPATH, '//*[@id="user-form"]/div/div/div[3]/div/fieldset/label[2]/input').click()
        driver.find_element(By.XPATH, '//*[@id="act-as"]').click()
        input()
        driver.get(addUser_url)

# perform the ops managements
def ops_onboard(df, df1, driver):
    fullName = []
    email = []
    for i, j in enumerate(df['Department']):
        if j == "Operations Team" and df['Home Base'][i] == 'Orlando':
            print(df1)
            eph_fullName = df['First Name'][i] + " " + df['Last Name'][i]
            fullName.append(eph_fullName)
            eph_email = (df['Email Address Gsuite Primary'][i]).split("@")
            email.append(eph_email[0] + "@staxpayments.com")
        else:
            fullName.append("Nothing")
            email.append("Nothing")

    df1['fullName'] = fullName
    df1['email'] = email
    swipe_automate(driver, df1)

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
