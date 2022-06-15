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
    login_url = 'https://paymentdepot.transactiongateway.com/resellers/login.php?cookie_check=1'
    print("Current Dataframe, to be entered: \n", df1)
    driver.get(login_url)
    driver.find_element(By.XPATH, '//*[@id="affiliate-login-username"]').send_keys(creds.usernameNMIpd)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="affiliate-login-password"]').send_keys(creds.passwordNMIpd + Keys.RETURN)
    input("Press Enter after MFA: ") #
    time.sleep(1)
    tid = (driver.current_url).split("tid=")
    addUser_url = f'https://paymentdepot.transactiongateway.com/resellers/options.php?Action=AddAccount&tid={tid[1]}'
    driver.get(addUser_url)
    input("Press Enter to start entering users: \n")
    for i, j in enumerate(df1['userName']):
        # put words on the screen
        time.sleep(1)
        print(f"Inputing data for {j}")
        driver.find_element(By.XPATH, '//*[@id="firstname"]').send_keys(df1['firstName'][i])
        driver.find_element(By.XPATH, '//*[@id="lastname"]').send_keys(df1['lastName'][i])
        driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(df1['email'][i])
        driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(j)
        time.sleep(1)

        # set the permissions for MTLRDH
        driver.find_element(By.XPATH, '//*[@id="perm_managemerchants"]').click()
        driver.find_element(By.XPATH, '//*[@id="perm_transactions"]').click()
        driver.find_element(By.XPATH, '//*[@id="perm_login"]').click()
        driver.find_element(By.XPATH, '//*[@id="perm_device_orders"]').click()
        driver.find_element(By.XPATH, '//*[@id="perm_device_order_history"]').click()
        driver.find_element(By.XPATH, '//*[@id="perm_view_release_notes"]').click()
        input("[+]Hit Enter for Next User\n")
        driver.get(addUser_url)

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
    df = pd.read_csv("../../Onboarding/db/empemails.csv")
    df1 = pd.DataFrame(columns=['firstName', 'lastName', 'userName', 'password', 'email'])

    # start the function
    ops_onboard(df, df1, driver)
    os.system("pyclean . -q")

main()
