import time
import xlrd

from selenium import webdriver
from src.utilities.constants import MY_CONSTANT, PASSWORD, GMAIL_ADDRESS
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

sender = []

def select_sender(index):
    senders_file = xlrd.open_workbook("./assets/xls/50-pcs-2020-16.6.xlsx"); 
    senders_list = senders_file.sheet_by_index(0)
    for i in range(0,3):
        sender.append(senders_list.cell_value(index-1, i))

def main():
    select_sender(1)
    driver.get("https://www.google.com/accounts/Login")
    email_input = driver.find_element(by=By.NAME, value="identifier")
    email_input.send_keys(sender[0])
    time.sleep(1)
    email_input.send_keys(Keys.ENTER)
    time.sleep(100)

if __name__ == '__main__':
    main()
