import time
import xlrd

from seleniumwire import webdriver
from src.utilities.constants import MY_CONSTANT, PASSWORD, GMAIL_ADDRESS
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# driver = webdriver.Chrome()

sender = []
senders_file = xlrd.open_workbook("./assets/xls/50-pcs-2020-16.6.xlsx") 
senders_list = senders_file.sheet_by_index(0)
number_of_senders = senders_list.nrows
options = Options

def login_to_google(email, password, recovery_email):
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/accounts/Login")
    time.sleep(1)
    email_input = driver.find_element(by=By.NAME, value="identifier")
    time.sleep(1)
    email_input.send_keys(email)
    time.sleep(1)
    next_button = driver.find_element(by=By.ID, value="identifierNext")
    next_button.click()

    time.sleep(0.5)
    passord_input = driver.find_element(by=By.NAME, value="Password")
    time.sleep(0.5)
    passord_input.send_keys(PASSWORD)
    password_next = driver.find_element(by=By.ID, value="passwordNext")
    password_next.click()

def main():
    for i in range(0, number_of_senders):
        email = senders_list.cell_value(i, 0)
        password = senders_list.cell_value(i, 1)
        recovery_email = senders_list.cell_value(i,2)
        login_to_google(email, password, recovery_email)
    

if __name__ == '__main__':
    main()

