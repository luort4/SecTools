import pandas as pd
import creds
import time
import os
import string
import random
import pyperclip
from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

def steam_automate(driver, df1):
    addUser_url = 'https://dvmms.com/steam/admin.aspx?screen_ID=130&ACTION=ADD&Main_Field=538&ret=https%3a%2f%2fdvmms.com%2fsteam%2fadmin.aspx%3fscreen_id%3d101'
    #login and then
    print("Current Dataframe, to be entered: \n", df1)
    driver.get("https://dvmms.com/steam/login.aspx")
    driver.find_element(By.XPATH, '//*[@id="ContentPH_LoginTbl_txtUser"]').send_keys(creds.usernamePD)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="ContentPH_LoginTbl_txtPWD"]').send_keys(creds.passwordPD + Keys.RETURN)
    # driver.find_element(By.XPATH, '//*[@id="ContentPH_LoginTbl_btnLogin"]').click()
    print("Press Enter to start inputing users: ")
    input()
    #
    try:
        driver.get(addUser_url)
    except Exception as e:
        driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder_lblContent"]/table[2]/tbody/tr[1]/td/div/div/a[2]').click()
    for i, j in enumerate(df1['userName']):
        time.sleep(1)
        print(f"Inputing data for {df1['fullName'][i]}")
        driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder_ctl00_UserTbl_Name"]').send_keys(df1['fullName'][i])
        driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder_ctl00_UserTbl_Email"]').send_keys(df1['email'][i])
        driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder_ctl00_UserTbl_UserName"]').send_keys(j)
        driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder_ctl00_UserTbl_Password1"]').send_keys(df1['password'][i])
        driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder_ctl00_UserTbl_Password2"]').send_keys(df1['password'][i])
        Select(driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder_ctl00_UserTbl_RoleId"]')).select_by_visible_text("Technical Service")
        email_template(df1, i, j)
        input()
        driver.get(addUser_url)

# generate a random password
def ran_pass(df1):
    ch = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    random.shuffle(ch)
    user_pass = []
    for i in df1['userName']:
        temp_pass = []
        for j in range(12):
            temp_pass.append(random.choice(ch))
        random.shuffle(temp_pass)
        user_pass.append("".join(temp_pass) + "5jJ*")
    df1['password'] = user_pass
    return df1

# perform the ops managements
def ops_onboard(df, df1, driver):
    userName = []
    fullName = []
    email = []
    for i, j in enumerate(df['Department']):
        if j == "Operations Team" and df['Home Base'][i] == 'Orlando':
            print(df1)
            userName.append((df['Email Address Gsuite Primary'][i]).split("@")[0] + "PD")
            eph_fullName = df['First Name'][i] + " " + df['Last Name'][i]
            fullName.append(eph_fullName)
            email.append(df['Email Address Gsuite Primary'][i])
        else:
            fullName.append("Nothing")
            userName.append("Nothing")
            email.append("Nothing")

    df1['userName'] = userName
    df1['fullName'] = fullName
    df1['email'] = email
    ran_pass(df1)
    steam_automate(driver, df1)

def email_template(df1, i, j):
    template = f'''
Hello {df1['fullName'][i]},
Here is your access for Dejavoo/DVMSS PD:
Username: {j}
Password: {df1['password'][i]}'''
    with open(f"temp/{j}.txt", "w+") as f:
        f.write(template)
        pyperclip.copy(template)
        print(f"{df1['fullName'][i]} copied to clipboard")


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
    df1 = pd.DataFrame(columns=['fullName', 'userName', 'password', 'email'])
    # start the function
    ops_onboard(df, df1, driver)
    os.system("pyclean . -q")

main()
