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

def nmi_automate(driver, df1):
    # login and then make the dataframe
    login_url = 'https://mxconnect.com/#/login'
    print("Current Dataframe to be entered: ", df1)
    driver.get(login_url)
    driver.find_element(By.XPATH, '//*[@id="signinform"]/div[1]/input').send_keys(creds.mxusername)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="signinform"]/div[2]/input').send_keys(creds.mxpassword + Keys.RETURN)
    input("Press Enter after Login: ") #
    time.sleep(1)
    addUser_url = 'https://mxconnect.com/#/security/users?globalData=%7B%22timeRange%22%3A%7B%22value%22%3A%7B%22type%22%3A%22q%22%2C%22quick%22%3A%22allOfTime%22%7D%2C%22isVisible%22%3Afalse%7D%2C%22timeRangeGrouping%22%3A%7B%22value%22%3A%7B%22type%22%3A%22abs%22%2C%22absolute%22%3A%7B%22from%22%3A%222022-06-01T00%3A00%3A00-04%3A00%22%2C%22to%22%3A%222022-06-30T23%3A59%3A59-04%3A00%22%7D%7D%2C%22isVisible%22%3Afalse%2C%22menuHidden%22%3Afalse%2C%22mode%22%3A%22local%22%7D%2C%22timeInterval%22%3A%7B%22value%22%3A%220%22%2C%22isVisible%22%3Afalse%7D%2C%22globalActivePane%22%3A%7B%22pane%22%3A%22%22%2C%22visible%22%3Afalse%7D%2C%22filters%22%3A%5B%5D%2C%22timeRangeInitialized%22%3Atrue%2C%22timeIntervalInitialized%22%3Afalse%2C%22filtersInitialized%22%3Atrue%2C%22newFilter%22%3A%22%22%2C%22searchTypesSelected%22%3A%5B%22partner%22%2C%22merchant%22%2C%22label%22%2C%22user%22%2C%22product%22%5D%2C%22loading%22%3Afalse%7D&query=%7B%22search%22%3A%22%22%2C%22page%22%3A0%2C%22sort%22%3A%22modified%3Adesc%22%2C%22size%22%3A10%2C%22filter%22%3A%5B%5D%7D'

    # go to the site to set up to press the green "add user" button
    driver.get(addUser_url)
    input("Press Enter to start entering users: \n")
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/section/div/div/div[1]/button').click()

    # start looking through the prompt and inputting user information
    for i, j in enumerate(df1['userName']):
        # put words on the screen
        input("Press Enter after Green [+] Button is pressed")
        time.sleep(1)
        print(f"Inputing data for {j}")
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/span/div/div/div/div/div[2]/form/div[2]/div/div/div/div[1]/div[2]/div[2]/input').send_keys(df1['email'][i])
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/span/div/div/div/div/div[2]/form/div[2]/div/div/div/div[3]/div[2]/div[2]/div/div[1]/input').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/span/div/div/div/div/div[2]/form/div[2]/div/div/div/div[3]/div[2]/div[2]/div/div[2]/div[11]').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/span/div/div/div/div/div[2]/form/div[2]/div/div/div/div[4]/div[2]/div[2]/input').send_keys(df1['firstName'][i])
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/span/div/div/div/div/div[2]/form/div[2]/div/div/div/div[5]/div[2]/div[2]/input').send_keys(df1['lastName'][i])
        time.sleep(1)
        input("[+]Hit Enter for Next User\n")

        # in the event the user does not need to be added
        try:
            driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/span/div/div/div/div/div[2]/form/div[1]/div/button').click()
            time.sleep(1)
            driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div[3]/button[1]').click()
            time.sleep(1)
        except:
            pass

        # get the process ready again
        driver.get(addUser_url)
        time.sleep(4)
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/section/div/div/div[1]/button').click()
        time.sleep(1)


# perform the ops managements
def ops_onboard(df, df1, driver):
    userName = []
    firstName = []
    lastName = []
    email = []
    for i, j in enumerate(df['Department']):
        if j == "Operations Team" and df['Home Base'][i] == 'Orlando':
            userName.append((df['Email Address Gsuite Primary'][i]).split("@")[0] + "PD")
            firstName.append(df['First Name'][i])
            lastName.append(df['Last Name'][i])
            email.append(df['Email Address Gsuite Primary'][i])
        else:
            firstName.append("Nothing")
            lastName.append("Nothing")
            userName.append("Nothing")
            email.append("Nothing")

    df1['userName'] = userName
    df1['firstName'] = firstName
    df1['lastName'] = lastName
    df1['email'] = email
    nmi_automate(driver, df1)

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
    df1 = pd.DataFrame(columns=['firstName', 'lastName', 'userName', 'email'])

    # start the function
    ops_onboard(df, df1, driver)
    os.system("pyclean . -q")

#main()
