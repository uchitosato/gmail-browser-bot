import time

from seleniumwire import webdriver
from src.utilities.constants import MY_CONSTANT, PASSWORD, GMAIL_ADDRESS
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

def main():
    driver.get("https://www.google.com/accounts/Login")
    email_input = driver.find_element(by=By.NAME, value="identifier")
    time.sleep(0.5)
    email_input.send_keys(GMAIL_ADDRESS)
    time.sleep(0.5)
    next_button = driver.find_element(by=By.ID, value="identifierNext")
    time.sleep(0.5)
    next_button.click()
    time.sleep(0.5)
    passord_input = driver.find_element(by=By.NAME, value="Password")
    time.sleep(0.5)
    passord_input.send_keys(PASSWORD)
    password_next = driver.find_element(by=By.ID, value="passwordNext")
    password_next.click()


if __name__ == '__main__':
    main()
